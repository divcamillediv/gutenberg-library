import { afterEach, describe, expect, it, vi } from "vitest";
import { api, ApiError } from "./api.js";

function mockFetch(status, body) {
  const fetchMock = vi.fn().mockResolvedValue({
    ok: status >= 200 && status < 300,
    status,
    json: async () => body,
  });
  vi.stubGlobal("fetch", fetchMock);
  return fetchMock;
}

afterEach(() => vi.unstubAllGlobals());

describe("client API", () => {
  it("construit l'URL de recherche avec pagination", async () => {
    const fetchMock = mockFetch(200, { total: 0, results: [], suggestions: [] });
    await api.search("white whale", { limit: 10, offset: 20 });
    expect(fetchMock.mock.calls[0][0]).toBe("/api/search?q=white+whale&limit=10&offset=20");
  });

  it("encode les caractères spéciaux d'une RegEx", async () => {
    const fetchMock = mockFetch(200, { total: 0, results: [], suggestions: [] });
    await api.advancedSearch("whal(e|es)+");
    expect(fetchMock.mock.calls[0][0]).toContain("regex=whal%28e%7Ces%29%2B");
  });

  it("transmet le message d'erreur du backend", async () => {
    mockFetch(400, { detail: "La requête est vide." });
    await expect(api.search("")).rejects.toMatchObject({ status: 400, message: "La requête est vide." });
  });

  it("résume les erreurs de validation FastAPI (422)", async () => {
    mockFetch(422, { detail: [{ msg: "Input should be greater than or equal to 1" }] });
    await expect(api.getBookText(1, { page: 0 })).rejects.toBeInstanceOf(ApiError);
  });

  it("signale un backend injoignable", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new TypeError("Failed to fetch")));
    await expect(api.health()).rejects.toMatchObject({ status: 0 });
  });
});
