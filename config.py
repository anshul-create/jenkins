import os

# Prefer an explicit connection string when one is provided (matches
# config.py's original behaviour and works well for local development).
DATABASE_URL = os.getenv("DATABASE_URL")

# Otherwise fall back to the discrete MYSQL_* variables, which is what
# docker-compose.yml passes to the container. MYSQL_HOST=mysql resolves to
# the MySQL service on the compose network.
if not DATABASE_URL:
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
    MYSQL_USER = os.getenv("MYSQL_USER", "cicduser")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "cicdpassword")
    MYSQL_DB = os.getenv("MYSQL_DB", "cicddb")

    DATABASE_URL = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
        f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    )
