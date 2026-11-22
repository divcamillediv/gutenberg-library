from __future__ import annotations

import json
import logging
import os
from functools import lru_cache
from pathlib import Path

from app.config import settings
from app.config.database import load_books_from_postgres

logger = logging.getLogger(__name__)


class BookNotFoundError(LookupError):
    """Identifiant de livre inconnu."""


class BookTextUnavailableError(LookupError):
    """Le livre existe mais son fichier texte est introuvable."""


class PageOutOfRangeError(LookupError):
    """Numéro de page au-delà de la dernière page du livre."""


def _split_offsets(text: str, page_size: int) -> list[tuple[int, int]]:
    """Découpe `text` en pages d'environ `page_size` caractères.

    On coupe de préférence sur un saut de ligne, sinon sur une espace,
    pour ne jamais couper un mot en deux.
    Retourne la liste des bornes (début, fin).
    """

    offsets: list[tuple[int, int]] = []
    start, length = 0, len(text)

    while start < length:
        end = min(start + page_size, length)

        if end < length:
            floor = start + page_size // 2
            cut = text.rfind("\n", floor, end)

            if cut == -1:
                cut = text.rfind(" ", floor, end)

            if cut != -1:
                end = cut + 1

        offsets.append((start, end))
        start = end

    return offsets or [(0, 0)]


class BookService:
    """Catalogue en mémoire + lecture paginée des textes."""

    def __init__(self) -> None:
        self._books: dict[int, dict] = {}
        self._order: list[int] = []
        self.source: str = "sample"

    # -------------------------------------------------- chargement

    def load(self) -> None:
        """Charge les métadonnées du catalogue."""

        # Chargement depuis PostgreSQL
        if os.getenv("BOOKS_SOURCE") == "postgres":
            raw = load_books_from_postgres()

            if not raw:
                raise RuntimeError(
                    "Le catalogue PostgreSQL est vide."
                )

            self.source = "corpus"
            source_name = "PostgreSQL"

        # Chargement depuis le fichier JSON réel
        elif settings.metadata_file.exists():
            path = settings.metadata_file
            raw = json.loads(
                path.read_text(encoding="utf-8")
            )

            self.source = "corpus"
            source_name = str(path)

        # Chargement des données d'exemple
        else:
            path = settings.sample_metadata_file

            raw = json.loads(
                path.read_text(encoding="utf-8")
            ) if path.exists() else []

            self.source = "sample"
            source_name = str(path)

            logger.warning(
                "Corpus réel absent : utilisation des livres simulés."
            )

        self._books = {
            int(book["id"]): book
            for book in raw
        }

        self._order = sorted(
            self._books,
            key=lambda i: (
                self._books[i]["title"].lower(), i
            )
        )

        self._read_text.cache_clear()
        self._page_offsets.cache_clear()

        logger.info(
            "%d livres chargés depuis %s",
            len(self._books),
            source_name
        )

    # ----------------------------------------------- métadonnées

    def count(self) -> int:
        return len(self._books)

    def all_ids(self) -> list[int]:
        return list(self._order)

    def list(self, limit: int, offset: int) -> tuple[int, list[dict]]:
        """Retourne (total, livres de la page), triés par titre."""

        ids = self._order[offset: offset + limit]

        return len(self._order), [
            self._books[i] for i in ids
        ]

    def find(self, book_id: int) -> dict | None:
        return self._books.get(book_id)

    def get(self, book_id: int) -> dict:
        book = self._books.get(book_id)

        if book is None:
            raise BookNotFoundError(book_id)

        return book

    # ------------------------------------------------------ texte

    def text_path(self, book_id: int) -> Path:
        return settings.resolve_data_path(
            self.get(book_id)["file_path"]
        )

    @lru_cache(maxsize=16)
    def _read_text(self, book_id: int) -> str:
        try:
            path = self.text_path(book_id)

            return path.read_text(
                encoding="utf-8",
                errors="replace"
            )

        except (OSError, ValueError) as exc:
            raise BookTextUnavailableError(book_id) from exc

    @lru_cache(maxsize=64)
    def _page_offsets(
            self, book_id: int, page_size: int
    ) -> list[tuple[int, int]]:

        return _split_offsets(
            self._read_text(book_id),
            page_size
        )

    def read_text(self, book_id: int) -> str:
        """Texte intégral nettoyé d'un livre."""

        return self._read_text(book_id)

    def text_page(
            self, book_id: int, page: int, page_size: int
    ) -> dict:
        """Retourne une page du texte intégral."""

        book = self.get(book_id)
        offsets = self._page_offsets(book_id, page_size)

        if page > len(offsets):
            raise PageOutOfRangeError(page)

        start, end = offsets[page - 1]

        return {
            "id": book_id,
            "title": book["title"],
            "page": page,
            "page_size": page_size,
            "total_pages": len(offsets),
            "text": self._read_text(book_id)[start:end],
        }


# Instance unique partagée par les routeurs
book_service = BookService()