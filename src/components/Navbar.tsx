import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  Image,
  FileText,
  ShieldCheck,
  BookOpen,
  Link2,
  Search,
  Layers,
  Sun,
  Moon,
  Monitor,
  Languages,
} from 'lucide-react';
import { useAppPreferences, ThemeMode } from '../context/AppPreferencesContext';

interface NavbarProps {
  onOpenSearch: () => void;
  totalFigures: number;
  totalFrs: number;
}

export const Navbar: React.FC<NavbarProps> = ({
  onOpenSearch,
  totalFigures,
  totalFrs,
}) => {
  const { theme, setTheme, lang, toggleLang, tx } = useAppPreferences();

  const navItems = [
    {
      to: '/',
      label: tx(`Figures (${totalFigures})`, `Figures (${totalFigures})`),
      shortLabel: 'Figures',
      icon: Image,
      end: true,
    },
    {
      to: '/frs',
      label: tx(`141 FRs`, `141 FRs`),
      shortLabel: '141 FRs',
      icon: FileText,
    },
    {
      to: '/matrices',
      label: tx('Use Cases & RBAC', 'Use Cases & RBAC'),
      shortLabel: 'Matrix',
      icon: ShieldCheck,
    },
    {
      to: '/rules',
      label: tx('Rules & Messages', 'Rules & Messages'),
      shortLabel: 'BR / MSG',
      icon: BookOpen,
    },
    {
      to: '/links',
      label: tx('Link gắn Word', 'Word Deep-Links'),
      shortLabel: tx('Link Word', 'Links'),
      icon: Link2,
    },
  ];

  const themeOptions: { mode: ThemeMode; icon: typeof Sun; title: string }[] = [
    {
      mode: 'light',
      icon: Sun,
      title: tx('Giao diện Sáng', 'Light Mode'),
    },
    {
      mode: 'dark',
      icon: Moon,
      title: tx('Giao diện Tối', 'Dark Mode'),
    },
    {
      mode: 'system',
      icon: Monitor,
      title: tx('Đồng bộ theo Hệ thống / Thiết bị', 'Sync with System Theme'),
    },
  ];

  return (
    <>
      <header className="sticky top-0 z-40 bg-white/95 dark:bg-slate-900/95 backdrop-blur-md border-b border-slate-200 dark:border-slate-800 transition-colors">
        <div className="max-w-6xl mx-auto px-3 sm:px-4 h-14 flex items-center justify-between gap-2 sm:gap-4">
          <div className="flex items-center gap-4 lg:gap-6 min-w-0">
            <NavLink
              to="/"
              className="inline-flex items-center gap-2 font-bold text-slate-900 dark:text-slate-100 text-base tracking-tight shrink-0 interactive-btn"
            >
              <div className="w-7 h-7 rounded-md bg-sky-600 text-white flex items-center justify-center shadow-xs">
                <Layers className="w-4 h-4" />
              </div>
              <span>
                <span className="text-sky-600 dark:text-sky-400">BrandHub</span>{' '}
                <span className="font-medium text-slate-500 dark:text-slate-400 text-xs sm:text-sm">
                  Docs
                </span>
              </span>
            </NavLink>

            <nav className="hidden md:flex items-center gap-1">
              {navItems.map((item) => {
                const Icon = item.icon;
                return (
                  <NavLink
                    key={item.to}
                    to={item.to}
                    end={item.end}
                    className={({ isActive }) =>
                      `interactive-btn inline-flex items-center gap-1.5 px-2.5 lg:px-3 py-1.5 rounded-md text-xs font-medium cursor-pointer ${
                        isActive
                          ? 'bg-sky-600 text-white shadow-xs'
                          : 'text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-white'
                      }`
                    }
                  >
                    <Icon className="w-3.5 h-3.5 shrink-0" />
                    <span className="whitespace-nowrap">{item.label}</span>
                  </NavLink>
                );
              })}
            </nav>
          </div>

          <div className="flex items-center gap-1.5 sm:gap-2 shrink-0">
            {/* Search Trigger */}
            <button
              onClick={onOpenSearch}
              aria-label={tx('Tìm kiếm nhanh', 'Quick search')}
              className="interactive-btn inline-flex items-center gap-2 px-2.5 sm:px-3 py-1.5 rounded-md bg-slate-100/80 dark:bg-slate-800 hover:bg-slate-200/70 dark:hover:bg-slate-700 border border-slate-200 dark:border-slate-700 text-xs text-slate-600 dark:text-slate-300 cursor-pointer"
            >
              <Search className="w-3.5 h-3.5 text-sky-600 dark:text-sky-400" />
              <span className="hidden sm:inline">
                {tx('Tìm kiếm...', 'Search...')}
              </span>
              <kbd className="hidden lg:inline-block px-1.5 py-0.5 text-[10px] font-mono bg-white dark:bg-slate-900 text-slate-500 dark:text-slate-400 rounded border border-slate-200 dark:border-slate-700">
                Ctrl+K
              </kbd>
            </button>

            {/* VI / EN Language Toggle */}
            <button
              onClick={toggleLang}
              title={tx(
                'Chuyển ngôn ngữ Tiếng Việt / Tiếng Anh',
                'Switch language Vietnamese / English'
              )}
              className="interactive-btn inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-md bg-white dark:bg-slate-800 hover:bg-slate-100 dark:hover:bg-slate-700 border border-slate-200 dark:border-slate-700 text-xs font-mono font-semibold text-slate-700 dark:text-slate-200 cursor-pointer"
            >
              <Languages className="w-3.5 h-3.5 text-sky-600 dark:text-sky-400" />
              <span>{lang.toUpperCase()}</span>
            </button>

            {/* Light / Dark / System Segmented Switcher */}
            <div
              className="inline-flex items-center p-0.5 rounded-md bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700"
              role="group"
              aria-label={tx('Chế độ giao diện', 'Theme mode')}
            >
              {themeOptions.map((opt) => {
                const Icon = opt.icon;
                const active = theme === opt.mode;
                return (
                  <button
                    key={opt.mode}
                    onClick={() => setTheme(opt.mode)}
                    title={opt.title}
                    aria-label={opt.title}
                    className={`interactive-btn p-1.5 rounded cursor-pointer ${
                      active
                        ? 'bg-white dark:bg-slate-900 text-sky-600 dark:text-sky-400 shadow-xs'
                        : 'text-slate-500 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-200'
                    }`}
                  >
                    <Icon className="w-3.5 h-3.5" />
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      </header>

      {/* Mobile Bottom Navigation Bar (Thumb-friendly responsive navigation) */}
      <nav
        aria-label={tx('Điều hướng di động', 'Mobile navigation')}
        className="md:hidden fixed bottom-0 inset-x-0 z-40 bg-white/95 dark:bg-slate-900/95 backdrop-blur-md border-t border-slate-200 dark:border-slate-800 px-1 py-1 flex items-center justify-around shadow-lg"
      >
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              className={({ isActive }) =>
                `interactive-btn flex flex-col items-center justify-center py-1.5 px-2 rounded-md text-[11px] font-medium min-w-[60px] ${
                  isActive
                    ? 'text-sky-600 dark:text-sky-400 bg-sky-50/80 dark:bg-sky-950/50'
                    : 'text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'
                }`
              }
            >
              <Icon className="w-4 h-4 mb-0.5" />
              <span className="truncate">{item.shortLabel}</span>
            </NavLink>
          );
        })}
      </nav>
    </>
  );
};
