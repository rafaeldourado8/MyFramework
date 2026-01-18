# RBAC Package

Role-Based Access Control com permissions.

## Instalação

```bash
pip install -e packages/rbac
```

## Quick Start

```python
from rbac import Role, Permission, RBACService

# Create permissions
read_users = Permission(code="users.read", name="Read Users")
write_users = Permission(code="users.write", name="Write Users")
delete_users = Permission(code="users.delete", name="Delete Users")

# Create role
admin = Role(code="admin", name="Administrator")
admin.add_permission(read_users)
admin.add_permission(write_users)
admin.add_permission(delete_users)

# Check permission
if admin.has_permission("users.delete"):
    print("Admin can delete users")

# User role
user = Role(code="user", name="User")
user.add_permission(read_users)

# Check with service
can_delete = RBACService.can_access(user, "users.delete")  # False
can_read = RBACService.can_access(user, "users.read")  # True
```

## FastAPI Integration

```python
from fastapi import FastAPI, Depends, HTTPException
from rbac import Role, Permission, require_permission, require_any_permission
from auth import get_current_user
from uuid import UUID

app = FastAPI()

# Get user role (your implementation)
async def get_current_role(user_id: UUID = Depends(get_current_user)) -> Role:
    user = get_user_by_id(user_id)
    return user.role

# Protected route - single permission
@app.delete("/users/{id}")
@require_permission("users.delete")
async def delete_user(id: str, role: Role = Depends(get_current_role)):
    # Delete user logic
    return {"deleted": id}

# Protected route - any permission
@app.get("/users")
@require_any_permission(["users.read", "users.write"])
async def list_users(role: Role = Depends(get_current_role)):
    # List users logic
    return {"users": []}

# Manual check
@app.post("/users")
async def create_user(data: dict, role: Role = Depends(get_current_role)):
    if not RBACService.can_access(role, "users.write"):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    # Create user logic
    return {"user": data}
```

## API Reference

### Permission

Entidade de permissão.

```python
from rbac import Permission

permission = Permission(
    code="users.read",
    name="Read Users",
    description="Can read user data"
)
```

### Role

Entidade de role com permissions.

```python
from rbac import Role, Permission

role = Role(code="admin", name="Administrator")

# Add permission
permission = Permission(code="users.write")
role.add_permission(permission)

# Remove permission
role.remove_permission(permission)

# Check permission
has_perm = role.has_permission("users.write")  # True
```

### RBACService

Serviço de controle de acesso.

```python
from rbac import RBACService, Role, Permission

# Check single permission
can_access = RBACService.can_access(role, "users.delete")

# Check any permission
can_access_any = RBACService.can_access_any(
    role,
    ["users.read", "users.write"]
)

# Check all permissions
can_access_all = RBACService.can_access_all(
    role,
    ["users.read", "users.write"]
)

# Grant permission
result = RBACService.grant_permission(role, permission)

# Revoke permission
result = RBACService.revoke_permission(role, permission)
```

## Permission Naming Convention

Use dot notation para organizar permissions:

```
resource.action
module.resource.action
```

**Exemplos:**
```python
# Basic
"users.read"
"users.write"
"users.delete"

# Nested
"admin.users.read"
"admin.users.write"
"api.keys.create"

# Specific
"posts.publish"
"posts.draft"
"comments.moderate"
```

## Roles Comuns

### Admin

```python
admin = Role(code="admin", name="Administrator")
admin.add_permission(Permission(code="users.read"))
admin.add_permission(Permission(code="users.write"))
admin.add_permission(Permission(code="users.delete"))
admin.add_permission(Permission(code="posts.read"))
admin.add_permission(Permission(code="posts.write"))
admin.add_permission(Permission(code="posts.delete"))
```

### Editor

```python
editor = Role(code="editor", name="Editor")
editor.add_permission(Permission(code="posts.read"))
editor.add_permission(Permission(code="posts.write"))
editor.add_permission(Permission(code="posts.publish"))
```

### Viewer

```python
viewer = Role(code="viewer", name="Viewer")
viewer.add_permission(Permission(code="users.read"))
viewer.add_permission(Permission(code="posts.read"))
```

## Casos de Uso

### Sistema de Blog

```python
# Permissions
permissions = [
    Permission(code="posts.read", name="Read Posts"),
    Permission(code="posts.write", name="Write Posts"),
    Permission(code="posts.publish", name="Publish Posts"),
    Permission(code="posts.delete", name="Delete Posts"),
    Permission(code="comments.read", name="Read Comments"),
    Permission(code="comments.moderate", name="Moderate Comments"),
]

# Roles
author = Role(code="author", name="Author")
author.add_permission(permissions[0])  # read
author.add_permission(permissions[1])  # write

editor = Role(code="editor", name="Editor")
editor.add_permission(permissions[0])  # read
editor.add_permission(permissions[1])  # write
editor.add_permission(permissions[2])  # publish

admin = Role(code="admin", name="Admin")
for perm in permissions:
    admin.add_permission(perm)
```

### API Routes

```python
@app.post("/posts")
@require_permission("posts.write")
async def create_post(data: dict, role: Role):
    return {"post": data}

@app.put("/posts/{id}/publish")
@require_permission("posts.publish")
async def publish_post(id: str, role: Role):
    return {"published": id}

@app.delete("/posts/{id}")
@require_permission("posts.delete")
async def delete_post(id: str, role: Role):
    return {"deleted": id}

@app.post("/comments/{id}/moderate")
@require_permission("comments.moderate")
async def moderate_comment(id: str, action: str, role: Role):
    return {"moderated": id, "action": action}
```

## Hierarquia de Roles

```python
# Super Admin (todas permissions)
super_admin = Role(code="super_admin", name="Super Admin")

# Admin (quase todas)
admin = Role(code="admin", name="Admin")

# Manager (subset)
manager = Role(code="manager", name="Manager")

# User (básico)
user = Role(code="user", name="User")
```

## Integração com Database

```python
from sqlalchemy import Column, String, Table, ForeignKey
from sqlalchemy.orm import relationship

# Models
class RoleModel(Base):
    __tablename__ = "roles"
    
    id = Column(String, primary_key=True)
    code = Column(String, unique=True)
    name = Column(String)
    permissions = relationship("PermissionModel", secondary="role_permissions")

class PermissionModel(Base):
    __tablename__ = "permissions"
    
    id = Column(String, primary_key=True)
    code = Column(String, unique=True)
    name = Column(String)

role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", String, ForeignKey("roles.id")),
    Column("permission_id", String, ForeignKey("permissions.id"))
)

# Convert to domain
def to_domain_role(model: RoleModel) -> Role:
    role = Role(code=model.code, name=model.name)
    for perm_model in model.permissions:
        perm = Permission(code=perm_model.code, name=perm_model.name)
        role.add_permission(perm)
    return role
```

## Troubleshooting

### Permission denied

- Verificar se role tem a permission
- Verificar código da permission (case-sensitive)
- Verificar se decorator está correto

### Role não encontrado

- Verificar se role foi criado
- Verificar se user tem role atribuído
