import { useState, useEffect } from 'react';

interface VideoStream {
  id: string;
  url: string;
  status: 'loading' | 'playing' | 'error';
}

export const useVideoStream = (streamId: string, apiUrl: string) => {
  const [stream, setStream] = useState<VideoStream | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStream = async () => {
      try {
        const response = await fetch(`${apiUrl}/streams/${streamId}`);
        const data = await response.json();
        setStream({
          id: data.id,
          url: data.url,
          status: 'playing'
        });
      } catch (err) {
        setError('Failed to load stream');
        setStream(null);
      } finally {
        setLoading(false);
      }
    };

    fetchStream();
  }, [streamId, apiUrl]);

  return { stream, loading, error };
};
