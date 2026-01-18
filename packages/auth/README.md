# MyFramework Auth

JWT authentication and password hashing with bcrypt.

## Installation

```bash
pip install myframework-auth
```

## Usage

```python
from myframework.auth import JWTService, Password

jwt = JWTService("secret")
token = jwt.generate_token({"user_id": 1})

password = Password.create("MyPass123")
```

See [documentation](https://github.com/rafaeldourado8/MyFramework/blob/master/docs/auth.md) for details.
