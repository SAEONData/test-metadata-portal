from setuptools import setup, find_packages

setup(
    name='Test-Metadata-Portal',
    packages=find_packages(),
    include_package_data=True,
    python_requires='~=3.6',
    install_requires=[
        'flask',
        'flask-dance[sqla]',
        'flask-login',
        'python-dotenv',
        'sqlalchemy',
        'psycopg2',
        'click',
    ],
    dependency_links=[
        'git+https://github.com/SAEONData/Hydra-OAuth2-Blueprint.git#egg=Hydra_OAuth2_Blueprint',
        'git+https://github.com/SAEONData/ODP-API-Client.git#egg=ODP_API_Client',
    ],
)
