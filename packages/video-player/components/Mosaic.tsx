import React from 'react';
import { VideoPlayer } from './VideoPlayer';

interface Stream {
  id: string;
  url: string;
  name?: string;
}

interface MosaicProps {
  streams: Stream[];
  layout?: '1x1' | '2x2' | '3x3' | '4x4';
}

export const Mosaic: React.FC<MosaicProps> = ({ streams, layout = '2x2' }) => {
  const gridCols = layout === '1x1' ? 1 : layout === '2x2' ? 2 : layout === '3x3' ? 3 : 4;

  return (
    <div
      style={{
        display: 'grid',
        gridTemplateColumns: `repeat(${gridCols}, 1fr)`,
        gap: '8px',
        width: '100%'
      }}
    >
      {streams.map((stream) => (
        <div key={stream.id} style={{ position: 'relative' }}>
          {stream.name && (
            <div style={{
              position: 'absolute',
              top: 8,
              left: 8,
              background: 'rgba(0,0,0,0.7)',
              color: 'white',
              padding: '4px 8px',
              borderRadius: 4,
              zIndex: 10
            }}>
              {stream.name}
            </div>
          )}
          <VideoPlayer src={stream.url} controls={false} />
        </div>
      ))}
    </div>
  );
};
