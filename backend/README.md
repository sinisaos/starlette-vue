Open terminal and run:

```shell
virtualenv -p python3 envname
cd envname
source bin/activate
git clone https://github.com/sinisaos/starlette-vue.git
cd starlette-vue/backend/
pip install -r requirements.txt
sudo -i -u yourpostgresusername psql
CREATE DATABASE vuedb;
\q
touch .env
## put this two line in .env file
## DB_URI="postgres://username:password@localhost:5432/vuedb"
## SECRET_KEY="your secret key"
cd src
uvicorn app:app --port 8000 --host 0.0.0.0

```


