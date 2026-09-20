# Start with the environment

### Create the project:

```bash
mkdir task-manager-api
cd task-manager-api
```
### Create virtual environment:

```bash
python3 -m venv venv
```

### Activate venv :

```bash
source venv/bin/activate
```

# Install the initial packages

pip install fastapi uvicorn
pip install sqlalchemy pymysql alembic
pip install python-jose[cryptography] pwdlib
pip install "pwdlib[argon2]"
pip install aiosmtplib
pip install pydantic-settings python-dotenv
pip install pytest httpx
pip install email-validator

Then save :
pip freeze > requirements.txt


