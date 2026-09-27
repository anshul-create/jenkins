import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://cicduser:cicdpassword@localhost:3306/cicddb"
)