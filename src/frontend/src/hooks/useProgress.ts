import { useEffect, useState } from "react";

export function useProgress(eventName: string) {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    function handler(e: any) {
      setProgress(e.detail);
    }

    window.addEventListener(eventName, handler);
    return () => {
      window.removeEventListener(eventName, handler);
      setProgress(0);
    };
  }, [eventName]);

  return progress;
}
