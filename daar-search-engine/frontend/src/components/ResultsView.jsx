import { api } from "../services/api.js";
import { useApi } from "../services/useApi.js";
import Pagination from "./Pagination.jsx";
import ResultCard from "./ResultCard.jsx";
import Suggestions from "./Suggestions.jsx";
import { Empty, ErrorMessage, Loading } from "./StatusMessage.jsx";

export const PAGE_SIZE = 10;

// Liste de résultats classés + suggestions, commune aux deux modes de recherche.
export default function ResultsView({ mode, query, page, onPageChange }) {
  const offset = (page - 1) * PAGE_SIZE;
  const { data, error, loading } = useApi(
    (options) =>
      mode === "regex"
        ? api.advancedSearch(query, { limit: PAGE_SIZE, offset }, options)
        : api.search(query, { limit: PAGE_SIZE, offset }, options),
    [mode, query, page]
  );

  if (loading && !data) return <Loading label="Recherche en cours…" />;
  if (error) return <ErrorMessage error={error} />;
  if (!data) return null;

  if (data.total === 0) {
    return (
      <Empty title="Aucun livre ne correspond.">
        {mode === "regex"
          ? "La RegEx est comparée aux mots de l'index : essayez un motif plus large, par exemple whal.*"
          : "Vérifiez l'orthographe ou essayez un autre mot-clé (les textes sont en anglais)."}
      </Empty>
    );
  }

  const totalPages = Math.ceil(data.total / PAGE_SIZE);
  return (
    <div className={`results-layout${loading ? " is-loading" : ""}`}>
      <section aria-label="Résultats">
        <p className="results-count">
          {data.total} livre{data.total > 1 ? "s" : ""} pour <q className={mode === "regex" ? "mono" : undefined}>{data.query}</q>,
          classé{data.total > 1 ? "s" : ""} par pertinence
        </p>
        <ol className="results">
          {data.results.map((result, index) => (
            <ResultCard key={result.id} rank={offset + index + 1} result={result} />
          ))}
        </ol>
        <Pagination page={page} totalPages={totalPages} onChange={onPageChange} label="Pages de résultats" />
      </section>
      <Suggestions title="Vous aimerez peut-être" items={data.suggestions} />
    </div>
  );
}
