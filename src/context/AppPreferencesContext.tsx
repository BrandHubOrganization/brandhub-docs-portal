import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';

export type ThemeMode = 'light' | 'dark' | 'system';
export type LanguageMode = 'vi' | 'en';

interface AppPreferencesContextValue {
  theme: ThemeMode;
  resolvedTheme: 'light' | 'dark';
  setTheme: (mode: ThemeMode) => void;
  cycleTheme: () => void;
  lang: LanguageMode;
  setLang: (lang: LanguageMode) => void;
  toggleLang: () => void;
  tx: (vi: string, en: string) => string;
}

const THEME_STORAGE_KEY = 'brandhub_docs_theme_v2';
const LANG_STORAGE_KEY = 'brandhub_docs_lang_v2';

const AppPreferencesContext = createContext<AppPreferencesContextValue | undefined>(
  undefined
);

function getSystemDark(): boolean {
  if (typeof window === 'undefined' || !window.matchMedia) return false;
  return window.matchMedia('(prefers-color-scheme: dark)').matches;
}

export const AppPreferencesProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  // Default strictly to 'light' (White background) unless user explicitly switches
  const [theme, setThemeState] = useState<ThemeMode>(() => {
    if (typeof window === 'undefined') return 'light';
    const saved = localStorage.getItem(THEME_STORAGE_KEY);
    if (saved === 'light' || saved === 'dark' || saved === 'system') return saved;
    return 'light';
  });

  const [systemDark, setSystemDark] = useState<boolean>(() => getSystemDark());

  // Default strictly to 'vi' (Tiếng Việt)
  const [lang, setLangState] = useState<LanguageMode>(() => {
    if (typeof window === 'undefined') return 'vi';
    const saved = localStorage.getItem(LANG_STORAGE_KEY);
    if (saved === 'vi' || saved === 'en') return saved;
    return 'vi';
  });

  // Listen to OS/Mobile system color-scheme changes in real time
  useEffect(() => {
    if (typeof window === 'undefined' || !window.matchMedia) return;
    const mql = window.matchMedia('(prefers-color-scheme: dark)');
    const handler = (e: MediaQueryListEvent) => setSystemDark(e.matches);
    mql.addEventListener('change', handler);
    return () => mql.removeEventListener('change', handler);
  }, []);

  const resolvedTheme: 'light' | 'dark' =
    theme === 'system' ? (systemDark ? 'dark' : 'light') : theme;

  // Apply .dark class and color-scheme to <html>
  useEffect(() => {
    const root = document.documentElement;
    if (resolvedTheme === 'dark') {
      root.classList.add('dark');
      root.style.colorScheme = 'dark';
    } else {
      root.classList.remove('dark');
      root.style.colorScheme = 'light';
    }
  }, [resolvedTheme]);

  // Apply lang attribute to <html>
  useEffect(() => {
    document.documentElement.lang = lang;
  }, [lang]);

  const setTheme = useCallback((mode: ThemeMode) => {
    setThemeState(mode);
    localStorage.setItem(THEME_STORAGE_KEY, mode);
  }, []);

  const cycleTheme = useCallback(() => {
    setThemeState((prev) => {
      const next: ThemeMode =
        prev === 'light' ? 'dark' : prev === 'dark' ? 'system' : 'light';
      localStorage.setItem(THEME_STORAGE_KEY, next);
      return next;
    });
  }, []);

  const setLang = useCallback((nextLang: LanguageMode) => {
    setLangState(nextLang);
    localStorage.setItem(LANG_STORAGE_KEY, nextLang);
  }, []);

  const toggleLang = useCallback(() => {
    setLangState((prev) => {
      const next: LanguageMode = prev === 'vi' ? 'en' : 'vi';
      localStorage.setItem(LANG_STORAGE_KEY, next);
      return next;
    });
  }, []);

  const tx = useCallback(
    (vi: string, en: string) => (lang === 'en' ? en : vi),
    [lang]
  );

  return (
    <AppPreferencesContext.Provider
      value={{
        theme,
        resolvedTheme,
        setTheme,
        cycleTheme,
        lang,
        setLang,
        toggleLang,
        tx,
      }}
    >
      {children}
    </AppPreferencesContext.Provider>
  );
};

export function useAppPreferences(): AppPreferencesContextValue {
  const ctx = useContext(AppPreferencesContext);
  if (!ctx) {
    throw new Error('useAppPreferences must be used within AppPreferencesProvider');
  }
  return ctx;
}
