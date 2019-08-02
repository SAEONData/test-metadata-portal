import os


class Config:
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_ECHO = os.getenv('DATABASE_ECHO', '').lower() == 'true'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    HYDRA_CLIENT_ID = os.getenv('HYDRA_CLIENT_ID')
    HYDRA_CLIENT_SECRET = os.getenv('HYDRA_CLIENT_SECRET')
    HYDRA_SCOPES = os.getenv('HYDRA_SCOPES', '').split()
    HYDRA_AUDIENCE = os.getenv('HYDRA_AUDIENCE')
    HYDRA_PUBLIC_URL = os.getenv('HYDRA_PUBLIC_URL')

    ODP_API_URL = os.getenv('ODP_API_URL')
