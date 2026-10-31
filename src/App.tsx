import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom';
import { FolderCode, BookOpen, Link2 } from 'lucide-react';
import portalData from './data';
import { AppPreferencesProvider, useAppPreferences } from './context/AppPreferencesContext';
import { Navbar } from './components/Navbar';
import { GlobalSearchModal } from './components/GlobalSearchModal';
import { FiguresCatalogPage } from './pages/FiguresCatalogPage';
import { FigureDetailPage } from './pages/FigureDetailPage';
import { FrExplorerPage } from './pages/FrExplorerPage';
import { FrDetailPage } from './pages/FrDetailPage';
import { SystemMatrixPage } from './pages/SystemMatrixPage';
import { RulesAndMessagesPage } from './pages/RulesAndMessagesPage';
import { WordLinkManagerPage } from './pages/WordLinkManagerPage';

const AnimatedRoutes: React.FC = () => {
  const location = useLocation();
  const { tx } = useAppPreferences();

  return (
    <>
      <main key={location.pathname} className="flex-1 animate-page-in pb-16 md:pb-0">
        <Routes location={location}>
          <Route path="/" element={<FiguresCatalogPage data={portalData} />} />
          <Route path="/figures" element={<FiguresCatalogPage data={portalData} />} />
          <Route
            path="/reports/:reportId"
            element={<FiguresCatalogPage data={portalData} />}
          />
          <Route
            path="/figures/:figureId"
            element={<FigureDetailPage data={portalData} />}
          />
          <Route path="/frs" element={<FrExplorerPage data={portalData} />} />
          <Route path="/frs/:frCode" element={<FrDetailPage data={portalData} />} />
          <Route path="/matrices" element={<SystemMatrixPage data={portalData} />} />
          <Route path="/rules" element={<RulesAndMessagesPage data={portalData} />} />
          <Route path="/links" element={<WordLinkManagerPage data={portalData} />} />
        </Routes>
      </main>

      <footer className="hidden md:block border-t border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 mt-12 transition-colors">
        <div className="max-w-6xl mx-auto px-4 py-4 flex flex-col sm:flex-row items-center justify-between gap-2 text-xs text-slate-500 dark:text-slate-400">
          <div className="inline-flex items-center gap-1.5">
            <FolderCode className="w-3.5 h-3.5 text-sky-600 dark:text-sky-400" />
            <span>
              {tx(
                'BrandHub Documentation - Chỉnh sửa nội dung tại',
                'BrandHub Documentation - Edit modular JSON files at'
              )}{' '}
              <code className="font-mono text-slate-700 dark:text-slate-300">src/data/</code>
            </span>
          </div>
          <div className="flex items-center gap-4">
            <Link
              to="/rules"
              className="inline-flex items-center gap-1 text-slate-600 dark:text-slate-300 hover:text-sky-700 dark:hover:text-sky-400 hover:underline"
            >
              <BookOpen className="w-3.5 h-3.5" />
              <span>Business Rules &amp; Messages</span>
            </Link>
            <Link
              to="/links"
              className="inline-flex items-center gap-1 text-slate-600 dark:text-slate-300 hover:text-sky-700 dark:hover:text-sky-400 hover:underline"
            >
              <Link2 className="w-3.5 h-3.5" />
              <span>{tx('Link gắn Word', 'Word Deep-Links')}</span>
            </Link>
          </div>
        </div>
      </footer>
    </>
  );
};

export const App: React.FC = () => {
  const [searchOpen, setSearchOpen] = useState(false);

  useEffect(() => {
    const onKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        setSearchOpen((prev) => !prev);
      }
    };
    window.addEventListener('keydown', onKeyDown);
    return () => window.removeEventListener('keydown', onKeyDown);
  }, []);

  return (
    <AppPreferencesProvider>
      <BrowserRouter>
        <div className="min-h-dvh flex flex-col bg-slate-50/40 dark:bg-slate-950 text-slate-900 dark:text-slate-100 transition-colors">
          <Navbar
            onOpenSearch={() => setSearchOpen(true)}
            totalFigures={portalData.projectInfo.totalFigures}
            totalFrs={portalData.projectInfo.totalFrs}
          />

          <AnimatedRoutes />

          <GlobalSearchModal
            isOpen={searchOpen}
            onClose={() => setSearchOpen(false)}
            data={portalData}
          />
        </div>
      </BrowserRouter>
    </AppPreferencesProvider>
  );
};

export default App;
