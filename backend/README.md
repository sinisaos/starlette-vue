### Instalation

Clone repository in fresh virtualenv.

```bash
git clone https://github.com/sinisaos/starlette-vue.git
```

### Install requirements


```bash
cd backend
pip install -r requirements.txt
```

### Creating an `.env` file.

```bash
cp .env.example .env && rm .env.example
```

### Start server 

```bash
uvicorn app:app --port 8000 --host 0.0.0.0
```

After site is running log in as admin user on [localhost:8000/admin/](http://localhost:8000/admin/).

