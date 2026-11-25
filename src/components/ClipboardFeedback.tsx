import { useEffect, useRef, useState } from 'react';
import { useAppPreferences } from '../context/AppPreferencesContext';

type CopyResult =
  | { status: 'copied'; key: string }
  | { status: 'failed'; key: string; url: string };

export function useLinkClipboard() {
  const [result, setResult] = useState<CopyResult | null>(null);
  const latestAttempt = useRef(0);
  const resetTimer = useRef<ReturnType<typeof setTimeout> | undefined>(undefined);

  useEffect(() => () => {
    latestAttempt.current += 1;
    clearTimeout(resetTimer.current);
  }, []);

  const copyLink = async (key: string, url: string) => {
    const attempt = ++latestAttempt.current;
    clearTimeout(resetTimer.current);
    setResult(null);

    try {
      await navigator.clipboard.writeText(url);
    } catch {
      if (attempt === latestAttempt.current) setResult({ status: 'failed', key, url });
      return;
    }

    if (attempt === latestAttempt.current) {
      setResult({ status: 'copied', key });
      resetTimer.current = setTimeout(() => setResult(null), 1500);
    }
  };

  return {
    copyLink,
    isCopied: (key: string) => result?.status === 'copied' && result.key === key,
    failedUrl: (key: string) => result?.status === 'failed' && result.key === key ? result.url : undefined,
  };
}

export function ClipboardFeedback({ url }: { url: string | undefined }) {
  const { tx } = useAppPreferences();
  const field = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (!url) return;
    field.current?.focus();
    field.current?.select();
  }, [url]);

  if (!url) return null;

  return (
    <div className="mt-2 min-w-0 text-left whitespace-normal text-xs">
      <p role="alert" className="mb-1 text-red-700 dark:text-red-300">
        {tx('Không sao chép được. Hãy sao chép đường link bên dưới.', 'Could not copy. Copy the link below manually.')}
      </p>
      <input
        ref={field}
        aria-label={tx('Đường link để sao chép', 'Link to copy')}
        readOnly
        value={url}
        onFocus={(event) => event.currentTarget.select()}
        className="w-full min-w-0 rounded border border-slate-300 px-2 py-1 font-mono text-slate-900 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-100"
      />
    </div>
  );
}
