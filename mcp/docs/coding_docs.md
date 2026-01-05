# 1) OAuth 2.0 — Quick Docs (Cheat Sheet)

## ✅ What OAuth is

OAuth 2.0 is an **authorization framework** that lets apps access a user’s data **without sharing the user’s password**.

### Key Roles

* **Resource Owner**: User
* **Client**: Your app
* **Authorization Server**: Google/GitHub/Auth0
* **Resource Server**: API (Google Drive API etc.)

---

## ✅ Most common OAuth flows

### **Authorization Code Flow (recommended for web apps)**

1. User logs in & approves
2. Provider returns **authorization code**
3. Your backend exchanges code for **access token**
4. You call API using access token

**Used for:** server-based apps

---

### **PKCE Flow (recommended for mobile / SPAs)**

Same as above but adds a code challenge so tokens aren’t stolen easily.

**Used for:** mobile apps, SPAs

---

### Access Token vs Refresh Token

| Token         | Purpose              | Expiry |
| ------------- | -------------------- | ------ |
| Access Token  | Call APIs            | short  |
| Refresh Token | Get new access token | long   |

---

## OAuth request example

### Step 1: Redirect to provider:

```http
GET https://accounts.google.com/o/oauth2/v2/auth?
  client_id=XXX&
  redirect_uri=https://yourapp.com/callback&
  response_type=code&
  scope=openid%20email%20profile&
  state=abc123
```

### Step 2: Exchange code for token:

```http
POST https://oauth2.googleapis.com/token
Content-Type: application/x-www-form-urlencoded

client_id=XXX&
client_secret=YYY&
code=CODE_FROM_STEP1&
grant_type=authorization_code&
redirect_uri=https://yourapp.com/callback
```

---

# 2) JWT — Documentation (Cheat Sheet)

## ✅ What JWT is

JWT (JSON Web Token) is a **compact token format** used for authentication/authorization.

A JWT is **three parts**:

```
HEADER.PAYLOAD.SIGNATURE
```

Example:

```txt
eyJhbGciOiJIUzI1NiIs... (header)
.eyJ1c2VySWQiOjEyMy... (payload)
.b8VfTq9W... (signature)
```

---

## ✅ JWT Fields (common)

Payload typically includes:

* `sub` → user id
* `iat` → issued at time
* `exp` → expiry time
* `aud` → intended audience
* `iss` → issuer

---

## ✅ JWT signing

JWT is *not encrypted* by default — payload can be read.

Signature ensures:
✅ token not modified
✅ token created by trusted issuer

---

## ✅ JWT Python example

```python
import jwt
from datetime import datetime, timedelta

secret = "mysecret"

token = jwt.encode(
    {"sub": "123", "exp": datetime.utcnow() + timedelta(hours=1)},
    secret,
    algorithm="HS256"
)

print(token)
```

Decode:

```python
data = jwt.decode(token, secret, algorithms=["HS256"])
print(data)
```

---

# 3) pip — Random Docs + Useful Commands

## ✅ Install package

```bash
pip install requests
```

## ✅ Install specific version

```bash
pip install requests==2.31.0
```

## ✅ Upgrade package

```bash
pip install --upgrade requests
```

## ✅ Install from requirements file

```bash
pip install -r requirements.txt
```

## ✅ Show installed packages

```bash
pip list
pip freeze
```

## ✅ Uninstall

```bash
pip uninstall requests
```

---

# 4) uv — Random Docs + Useful Commands

`uv` is a **super fast Python package/project manager** (Rust-based).

## ✅ Initialize project

```bash
uv init
```

## ✅ Add dependencies

```bash
uv add fastapi
```

## ✅ Lock dependencies

```bash
uv lock
```

## ✅ Install dependencies (sync)

```bash
uv sync
```

## ✅ Run commands inside env

```bash
uv run python main.py
uv run pytest
```

## ✅ Create virtual environment

```bash
uv venv
```

Creates:

```
./.venv/
```

## ✅ pip-style installs

```bash
uv pip install requests
uv pip install -r requirements.txt
```

---

# 5) Python List Methods — Documentation & Examples

Assume:

```python
nums = [1, 2, 3]
```

### ✅ Common Methods

| Method         | Purpose                 |
| -------------- | ----------------------- |
| `append(x)`    | add to end              |
| `extend(iter)` | add multiple            |
| `insert(i,x)`  | insert at index         |
| `remove(x)`    | remove first occurrence |
| `pop(i)`       | remove by index         |
| `clear()`      | remove all              |
| `index(x)`     | find index              |
| `count(x)`     | count occurrences       |
| `sort()`       | sort list               |
| `reverse()`    | reverse list            |
| `copy()`       | shallow copy            |

Examples:

```python
nums.append(4)
nums.extend([5,6])
nums.insert(0, 100)
nums.pop()          # removes last
nums.remove(2)      # removes first 2
nums.sort()
nums.reverse()
```

---

# 6) Python Dict Methods — Documentation & Examples

Assume:

```python
d = {"a": 1, "b": 2}
```

### ✅ Common Methods

| Method                   | Purpose              |
| ------------------------ | -------------------- |
| `get(k, default)`        | safe lookup          |
| `keys()`                 | keys view            |
| `values()`               | values view          |
| `items()`                | key-value pairs      |
| `update({...})`          | merge                |
| `pop(k)`                 | remove key           |
| `popitem()`              | remove last inserted |
| `setdefault(k, default)` | get or set           |
| `clear()`                | remove all           |
| `copy()`                 | shallow copy         |

Examples:

```python
d.get("c", 0)               # returns 0
d.update({"c": 3})
d.setdefault("d", 99)       # adds d if missing
d.pop("a")
for k, v in d.items():
    print(k, v)
```

---

# ✅ Bonus: Combined Example (OAuth token → JWT → API call)

```python
import requests

token = "ACCESS_TOKEN"
headers = {"Authorization": f"Bearer {token}"}
r = requests.get("https://api.example.com/user", headers=headers)

print(r.json())
```

---


