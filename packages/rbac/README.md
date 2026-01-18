# MyFramework RBAC

Role-Based Access Control with permissions and FastAPI integration.

## Installation

```bash
pip install myframework-rbac
```

## Usage

```python
from myframework.rbac import RBACService, require_permission

rbac = RBACService()
rbac.assign_permission_to_role("admin", "users:delete")

@require_permission("users:delete")
async def delete_user():
    pass
```

See [documentation](https://github.com/rafaeldourado8/MyFramework/blob/master/docs/rbac.md) for details.
