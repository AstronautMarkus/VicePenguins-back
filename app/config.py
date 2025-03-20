import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'kasane-teto_my-wife-forever-uwu'
