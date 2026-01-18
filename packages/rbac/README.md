# RBAC Package

Role-Based Access Control with permissions.

## Features

- Role and Permission entities
- Permission checking
- FastAPI decorators for route protection

## Usage

### Create Roles and Permissions

```python
from rbac import Role, Permission

# Create permissions
read_users = Permission(code="users.read", name="Read Users")
write_users = Permission(code="users.write", name="Write Users")

# Create role
admin = Role(code="admin", name="Administrator")
admin.add_permission(read_users)
admin.add_permission(write_users)

# Check permission
can_read = admin.has_permission("users.read")  # True
```

### RBAC Service

```python
from rbac import RBACService, Role, Permission

role = Role(code="user")
permission = Permission(code="posts.read")

# Grant permission
result = RBACService.grant_permission(role, permission)

# Check access
can_access = RBACService.can_access(role, "posts.read")  # True
```

### FastAPI Integration

```python
from fastapi import FastAPI, Depends
from rbac import require_permission, Role

app = FastAPI()

@app.get("/admin")
@require_permission("admin.access")
async def admin_route(role: Role):
    return {"message": "Admin access granted"}

@app.get("/users")
@require_any_permission(["users.read", "users.write"])
async def users_route(role: Role):
    return {"users": []}
```

## Permission Naming Convention

Use dot notation:
- `resource.action` (e.g., `users.read`, `posts.write`)
- `module.resource.action` (e.g., `admin.users.delete`)
