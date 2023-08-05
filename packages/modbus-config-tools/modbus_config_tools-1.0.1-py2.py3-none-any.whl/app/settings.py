class Config(object):
    import os
    from pathlib import Path
    DEBUG = False
    SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'
    BASE_DIR = Path(__file__).resolve().parent

    log_level = 'DEBUG'
    log_path = os.path.join(BASE_DIR, 'logs','')
    conf_path = os.path.join(BASE_DIR, 'conf', '')
    p = Path(conf_path)

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    import datetime
    DEBUG = True
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=31),
