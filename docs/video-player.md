# Video Player Package

Componentes React para player de vídeo com suporte a mosaic.

## Instalação

```bash
npm install @monorepo/video-player
# or
yarn add @monorepo/video-player
```

## Peer Dependencies

```json
{
  "react": "^18.0.0",
  "react-dom": "^18.0.0"
}
```

## Quick Start

```tsx
import { VideoPlayer, Mosaic } from '@monorepo/video-player';

function App() {
  return (
    <div>
      {/* Single player */}
      <VideoPlayer 
        src="https://example.com/video.mp4"
        controls
        autoPlay
      />
      
      {/* Mosaic (4 cameras) */}
      <Mosaic 
        streams={[
          { id: '1', url: 'rtsp://cam1', name: 'Camera 1' },
          { id: '2', url: 'rtsp://cam2', name: 'Camera 2' },
          { id: '3', url: 'rtsp://cam3', name: 'Camera 3' },
          { id: '4', url: 'rtsp://cam4', name: 'Camera 4' }
        ]}
        layout="2x2"
      />
    </div>
  );
}
```

## Components

### VideoPlayer

Player de vídeo básico com controles.

```tsx
import { VideoPlayer } from '@monorepo/video-player';

<VideoPlayer 
  src="https://example.com/video.mp4"
  autoPlay={false}
  controls={true}
  onTimeUpdate={(time) => console.log('Current time:', time)}
/>
```

**Props:**
- `src: string` - URL do vídeo
- `autoPlay?: boolean` - Auto play (default: false)
- `controls?: boolean` - Mostrar controles (default: true)
- `onTimeUpdate?: (time: number) => void` - Callback quando tempo muda

### Mosaic

Visualização de múltiplos vídeos em grid.

```tsx
import { Mosaic } from '@monorepo/video-player';

const streams = [
  { id: '1', url: 'rtsp://192.168.1.100/stream', name: 'Entrance' },
  { id: '2', url: 'rtsp://192.168.1.101/stream', name: 'Parking' },
  { id: '3', url: 'rtsp://192.168.1.102/stream', name: 'Office' },
  { id: '4', url: 'rtsp://192.168.1.103/stream', name: 'Warehouse' }
];

<Mosaic 
  streams={streams}
  layout="2x2"
/>
```

**Props:**
- `streams: Stream[]` - Array de streams
- `layout?: '1x1' | '2x2' | '3x3' | '4x4'` - Layout do grid (default: '2x2')

**Stream Type:**
```typescript
interface Stream {
  id: string;
  url: string;
  name?: string;
}
```

## Hooks

### useVideoStream

Hook para carregar stream da API.

```tsx
import { useVideoStream } from '@monorepo/video-player';

function VideoComponent({ streamId }: { streamId: string }) {
  const { stream, loading, error } = useVideoStream(
    streamId,
    'http://api.example.com'
  );
  
  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!stream) return null;
  
  return <VideoPlayer src={stream.url} controls />;
}
```

**Parameters:**
- `streamId: string` - ID do stream
- `apiUrl: string` - URL base da API

**Returns:**
```typescript
{
  stream: VideoStream | null;
  loading: boolean;
  error: string | null;
}
```

## Casos de Uso

### Sistema de Vigilância

```tsx
import { Mosaic } from '@monorepo/video-player';
import { useState, useEffect } from 'react';

function SecurityDashboard() {
  const [streams, setStreams] = useState([]);
  
  useEffect(() => {
    // Fetch streams from API
    fetch('/api/cameras')
      .then(res => res.json())
      .then(data => setStreams(data.cameras));
  }, []);
  
  return (
    <div>
      <h1>Security Dashboard</h1>
      <Mosaic streams={streams} layout="3x3" />
    </div>
  );
}
```

### Player com Timeline

```tsx
import { VideoPlayer } from '@monorepo/video-player';
import { useState } from 'react';

function VideoWithTimeline() {
  const [currentTime, setCurrentTime] = useState(0);
  const [events, setEvents] = useState([
    { time: 10, label: 'Motion detected' },
    { time: 45, label: 'Person entered' },
    { time: 120, label: 'Door opened' }
  ]);
  
  return (
    <div>
      <VideoPlayer 
        src="/video.mp4"
        onTimeUpdate={setCurrentTime}
        controls
      />
      
      <div className="timeline">
        {events.map(event => (
          <div 
            key={event.time}
            className={currentTime >= event.time ? 'active' : ''}
          >
            {event.time}s - {event.label}
          </div>
        ))}
      </div>
    </div>
  );
}
```

### Live Streaming

```tsx
import { VideoPlayer } from '@monorepo/video-player';

function LiveStream({ cameraId }: { cameraId: string }) {
  const hlsUrl = `http://mediamtx:8888/${cameraId}/index.m3u8`;
  
  return (
    <div>
      <div className="live-badge">🔴 LIVE</div>
      <VideoPlayer 
        src={hlsUrl}
        autoPlay
        controls
      />
    </div>
  );
}
```

### Mosaic com Seleção

```tsx
import { Mosaic } from '@monorepo/video-player';
import { useState } from 'react';

function SelectableMosaic() {
  const [selectedStream, setSelectedStream] = useState(null);
  const streams = [...]; // your streams
  
  return (
    <div>
      <Mosaic 
        streams={streams}
        layout="2x2"
        onStreamClick={setSelectedStream}
      />
      
      {selectedStream && (
        <div className="fullscreen">
          <VideoPlayer src={selectedStream.url} controls />
        </div>
      )}
    </div>
  );
}
```

## Styling

### Custom Styles

```tsx
import { VideoPlayer } from '@monorepo/video-player';
import './custom-player.css';

<VideoPlayer 
  src="/video.mp4"
  controls
  style={{
    width: '100%',
    maxWidth: '800px',
    borderRadius: '8px'
  }}
/>
```

### Mosaic Layout

```css
.mosaic-container {
  display: grid;
  gap: 8px;
  padding: 16px;
  background: #000;
}

.mosaic-item {
  position: relative;
  aspect-ratio: 16/9;
  overflow: hidden;
  border-radius: 4px;
}

.mosaic-label {
  position: absolute;
  top: 8px;
  left: 8px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
}
```

## Formatos Suportados

- **MP4** (H.264/H.265)
- **WebM** (VP8/VP9)
- **HLS** (.m3u8)
- **DASH** (.mpd)
- **RTSP** (via MediaMTX → HLS)

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Performance

### Otimizações

- Use HLS para streaming
- Lazy load videos
- Limit mosaic size (max 16 streams)
- Use video thumbnails for preview

### Example

```tsx
import { Mosaic } from '@monorepo/video-player';
import { useState } from 'react';

function OptimizedMosaic({ streams }) {
  const [visibleStreams, setVisibleStreams] = useState(
    streams.slice(0, 9) // Show only 9 at a time
  );
  
  return (
    <>
      <Mosaic streams={visibleStreams} layout="3x3" />
      
      <button onClick={() => setVisibleStreams(streams.slice(9, 18))}>
        Next Page
      </button>
    </>
  );
}
```

## Troubleshooting

### Video não carrega

- Verificar URL do vídeo
- Verificar CORS headers
- Verificar formato suportado

### RTSP não funciona

- RTSP não é suportado diretamente no browser
- Use MediaMTX para converter RTSP → HLS
- Acesse via HLS URL

### Performance ruim

- Reduzir número de streams simultâneos
- Usar resolução menor
- Usar HLS com adaptive bitrate
