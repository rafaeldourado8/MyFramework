# Framework Interno - Monorepo

<p align="center">
  <em>Framework opinioso para DDD com SOLID, autenticação, RBAC e streaming de vídeo</em>
</p>

<p align="center">
<a href="https://github.com/rafaeldourado8/MyFramework/actions" target="_blank">
    <img src="https://img.shields.io/badge/build-passing-brightgreen" alt="Build">
</a>
<a href="https://github.com/rafaeldourado8/MyFramework" target="_blank">
    <img src="https://img.shields.io/badge/python-3.11+-blue.svg" alt="Python">
</a>
<a href="https://github.com/rafaeldourado8/MyFramework/blob/main/LICENSE" target="_blank">
    <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License">
</a>
</p>

---

## Visão Geral

Framework interno modular com 9 packages reutilizáveis:

- **Core Framework**: DDD building blocks (Entity, UseCase, Application)
- **Auth & Security**: JWT, RBAC, Observability
- **Video Stack**: Streaming, Processing, Camera Management, Workers, Player

## Características

- ✅ **DDD**: Domain-Driven Design com bounded contexts
- ✅ **SOLID**: 100% dos princípios aplicados
- ✅ **Baixa Complexidade**: Funções com complexidade < 3
- ✅ **Type-Safe**: Type hints em todo código
- ✅ **Testado**: Testes automatizados
- ✅ **Documentado**: Documentação completa

## Quick Start

### Instalação

```bash
# Clone o repositório
git clone https://github.com/rafaeldourado8/MyFramework.git
cd MyFramework

# Instale os packages
pip install -e packages/core
pip install -e packages/auth
pip install -e packages/rbac
```

### Exemplo Básico

```python
from core import Application, Config, Module
from auth import AuthService, JWTService

# Configuração
config = Config.from_env()

# Serviços
jwt = JWTService(secret="your-secret-key")
auth = AuthService(jwt)

# Aplicação
app = Application(config)
app.register_module(YourModule())
app.run()
```

## Packages

### Core Framework

```python
from core import Entity, UseCase, Application, Module

class User(Entity):
    def __init__(self, id=None, name=""):
        super().__init__(id)
        self.name = name
```

[📖 Documentação completa](packages/core/README.md)

### Auth

```python
from auth import AuthService, JWTService

jwt = JWTService(secret="key")
auth = AuthService(jwt)

# Hash password
result = auth.hash_password("MyPassword123")

# Create tokens
token = auth.create_tokens(user_id, "user@example.com", "user")
```

[📖 Documentação completa](packages/auth/README.md)

### RBAC

```python
from rbac import Role, Permission, require_permission

@app.delete("/users/{id}")
@require_permission("users.delete")
async def delete_user(id: str, role: Role):
    return {"deleted": id}
```

[📖 Documentação completa](packages/rbac/README.md)

### Video Streaming

```python
from video_streaming import StreamingService, MediaMTXClientImpl

mediamtx = MediaMTXClientImpl(host="localhost")
streaming = StreamingService(mediamtx, ffmpeg, storage)

# Start stream
stream = await streaming.start_stream(camera_id, "rtsp://camera/stream")

# Start recording
recording = await streaming.start_recording(stream, retention_days=30)
```

[📖 Documentação completa](docs/video-streaming.md)

### Video Player (React)

```tsx
import { VideoPlayer, Mosaic } from '@monorepo/video-player';

// Single player
<VideoPlayer src="https://video.mp4" controls />

// Mosaic (4 cameras)
<Mosaic 
  streams={streams}
  layout="2x2"
/>
```

[📖 Documentação completa](docs/video-player.md)

## Estrutura

```
MyFramework/
├── packages/
│   ├── core/              # Framework DDD
│   ├── auth/              # Autenticação JWT
│   ├── rbac/              # Controle de acesso
│   ├── observability/     # Métricas + Logs
│   ├── video-streaming/   # Streaming de vídeo
│   ├── video-processing/  # Processamento
│   ├── camera-management/ # Gerenciar câmeras
│   ├── video-workers/     # Background workers
│   ├── video-player/      # React components
│   └── examples/          # Exemplos
└── docs/                  # Documentação
```

## Casos de Uso

### Sistema de Vigilância

```python
from video_streaming import StreamingService
from camera_management import CameraService

# Register cameras
cameras = [camera_service.register_camera(f"Cam {i}", url) for i in range(4)]

# Start streams
streams = [await streaming.start_stream(cam.id, cam.rtsp_url.url) for cam in cameras]

# Frontend: Mosaic
<Mosaic streams={streams} layout="2x2" />
```

### Plataforma de Vídeo

```python
from video_processing import VideoProcessingService

# Generate thumbnail
thumbnails = await processing.generate_thumbnails(video_id, path, interval=10)

# Create preview
preview = await processing.create_clip(video_id, path, start=0, duration=30)
```

## Requisitos

- Python 3.11+
- FastAPI 0.104+
- PostgreSQL (opcional)
- Redis (opcional)
- MediaMTX (para streaming)
- FFmpeg (para processamento)

## Desenvolvimento

```bash
# Instalar dependências de desenvolvimento
pip install -r requirements-dev.txt

# Rodar testes
pytest

# Validar core
cd packages/core
python validate.py
```

## Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/amazing`)
3. Commit suas mudanças (`git commit -m 'Add amazing feature'`)
4. Push para a branch (`git push origin feature/amazing`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja [LICENSE](LICENSE) para mais detalhes.

## Suporte

- 📖 [Documentação](docs/)
- 💬 [Discussions](https://github.com/rafaeldourado8/MyFramework/discussions)
- 🐛 [Issues](https://github.com/rafaeldourado8/MyFramework/issues)

---

<p align="center">
  Feito com ❤️ usando DDD + SOLID
</p>
