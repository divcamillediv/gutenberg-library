import { Route, Routes } from "react-router-dom";
import Layout from "./components/Layout.jsx";
import HomePage from "./pages/HomePage.jsx";
import ResultsPage from "./pages/ResultsPage.jsx";
import AdvancedSearchPage from "./pages/AdvancedSearchPage.jsx";
import LibraryPage from "./pages/LibraryPage.jsx";
import BookPage from "./pages/BookPage.jsx";
import NotFoundPage from "./pages/NotFoundPage.jsx";

// Vues de l'application :
//   /            accueil + recherche par mot-clé
//   /search      résultats classés + suggestions
//   /advanced    recherche avancée par RegEx (formulaire + résultats)
//   /books       catalogue paginé
//   /books/:id   détail et lecture du texte intégral
export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<HomePage />} />
        <Route path="search" element={<ResultsPage />} />
        <Route path="advanced" element={<AdvancedSearchPage />} />
        <Route path="books" element={<LibraryPage />} />
        <Route path="books/:bookId" element={<BookPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Route>
    </Routes>
  );
}
