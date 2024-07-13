import os

class Config:
    UPLOAD_FOLDER = 'uploads/'
    PROCESSED_FOLDER = 'processed/'
    ALLOWED_EXTENSIONS = {'jpeg', 'jpg', 'png'}
    SECRET_KEY = 'supersecretkey'

    @staticmethod
    def init_app(app):
        pass
