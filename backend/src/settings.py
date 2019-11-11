from starlette.config import Config


# Configuration from environment variables or '.env' file.
config = Config("../.env")
DB_URI = config("DB_URI")
SECRET_KEY = config("SECRET_KEY")
