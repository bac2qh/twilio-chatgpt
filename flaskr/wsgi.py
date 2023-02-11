from flaskr import create_app
from flaskr.db import init_db

init_db()
app = create_app()
