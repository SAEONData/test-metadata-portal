import os


class Config:
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')

    HYDRA_PUBLIC_URL = os.getenv('HYDRA_PUBLIC_URL')
    OAUTH2_CLIENT_ID = os.getenv('OAUTH2_CLIENT_ID')
    OAUTH2_CLIENT_SECRET = os.getenv('OAUTH2_CLIENT_SECRET')
    OAUTH2_SCOPES = os.getenv('OAUTH2_SCOPES', '').split()
    OAUTH2_AUDIENCE = os.getenv('OAUTH2_AUDIENCE')

    ODP_API_URL = os.getenv('ODP_API_URL')
    ACCOUNTS_API_URL = os.getenv('ACCOUNTS_API_URL')
    CKAN_API_KEY = os.getenv('CKAN_API_KEY')
