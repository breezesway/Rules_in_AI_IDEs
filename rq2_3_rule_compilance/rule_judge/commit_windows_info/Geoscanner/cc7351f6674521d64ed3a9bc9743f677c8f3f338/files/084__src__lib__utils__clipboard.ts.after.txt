import { useResultsStore } from '../results/state';

export const useClipboard = () => {
  const { copiedSnippets, addCopiedSnippet, removeCopiedSnippet } = useResultsStore();

  const copyToClipboard = async (snippetId: string, code: string) => {
    try {
      await navigator.clipboard.writeText(code);
      addCopiedSnippet(snippetId);
      setTimeout(() => removeCopiedSnippet(snippetId), 2000);
      return true;
    } catch (error) {
      console.error('Failed to copy code:', error);
      return false;
    }
  };

  const isCopied = (snippetId: string) => {
    return copiedSnippets.includes(snippetId);
  };

  return {
    copyToClipboard,
    isCopied,
  };
};
