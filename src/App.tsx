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
import { DemoMonitorPage } from './pages/DemoMonitorPage';
import { AstryxCode } from './components/astryx';

const AppShell: React.FC<{
  searchOpen: boolean;
  setSearchOpen: React.Dispatch<React.SetStateAction<boolean>>;
}> = ({ searchOpen, setSearchOpen }) => {
  const location = useLocation();
  const { tx } = useAppPreferences();
  const isStageController = location.pathname === '/demo-monitor';

  return (
    <div className="min-h-dvh flex flex-col bg-slate-50/40 dark:bg-slate-950 text-slate-900 dark:text-slate-100 transition-colors">
      {!isStageController && (
        <Navbar
          onOpenSearch={() => setSearchOpen(true)}
          totalFigures={portalData.projectInfo.totalFigures}
          totalFrs={portalData.projectInfo.totalFrs}
        />
      )}

      <main
        key={location.pathname}
        className={isStageController ? 'flex-1' : 'flex-1 animate-page-in pb-16 md:pb-0'}
      >
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
          <Route path="/demo-monitor" element={<DemoMonitorPage />} />
        </Routes>
      </main>

      {!isStageController && (
        <footer className="hidden md:block border-t border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 mt-12 transition-colors">
          <div className="max-w-6xl mx-auto px-4 py-4 flex flex-col sm:flex-row items-center justify-between gap-2 text-xs text-slate-500 dark:text-slate-400">
            <div className="inline-flex items-center gap-1.5">
              <FolderCode className="w-3.5 h-3.5 text-orange-600 dark:text-orange-400" />
              <span>
                {tx(
                  'BrandHub Documentation - Chỉnh sửa nội dung tại',
                  'BrandHub Documentation - Edit modular JSON files at'
                )}{' '}
                <AstryxCode className="font-mono text-slate-700 dark:text-slate-300">src/data/</AstryxCode>
              </span>
            </div>
            <div className="flex items-center gap-4">
              <Link
                to="/rules"
                className="inline-flex items-center gap-1 text-slate-600 dark:text-slate-300 hover:text-orange-600 dark:hover:text-orange-400 hover:underline"
              >
                <BookOpen className="w-3.5 h-3.5" />
                <span>Business Rules &amp; Messages</span>
              </Link>
              <Link
                to="/links"
                className="inline-flex items-center gap-1 text-slate-600 dark:text-slate-300 hover:text-orange-600 dark:hover:text-orange-400 hover:underline"
              >
                <Link2 className="w-3.5 h-3.5" />
                <span>{tx('Link gắn Word', 'Word Deep-Links')}</span>
              </Link>
            </div>
          </div>
        </footer>
      )}

      <GlobalSearchModal
        isOpen={searchOpen}
        onClose={() => setSearchOpen(false)}
        data={portalData}
      />
    </div>
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
        <AppShell searchOpen={searchOpen} setSearchOpen={setSearchOpen} />
      </BrowserRouter>
    </AppPreferencesProvider>
  );
};

export default App;
