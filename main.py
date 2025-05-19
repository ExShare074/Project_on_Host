from app import app, db
from app import routes, models
import logging
from logging.handlers import RotatingFileHandler
import os

with app.app_context():
    db.create_all()

if not os.path.exists('logs'):
    os.mkdir('logs')
file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=1)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

app.logger.setLevel(logging.INFO)
app.logger.info('Приложение запущено')

if __name__ == "__main__":
    app.run()