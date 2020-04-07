Open terminal and run:

```shell
virtualenv -p python3 envname
cd envname
source bin/activate
git clone https://github.com/sinisaos/starlette-vue.git
cd starlette-vue/backend/
pip install -r requirements.txt
mysql -u root -p
CREATE DATABASE test CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit;
touch .env
## put this two line in .env file
## DB_URI="mysql://username:password@localhost/test"
## SECRET_KEY="your secret key"
cd src
uvicorn app:app --port 8000 --host 0.0.0.0

```


