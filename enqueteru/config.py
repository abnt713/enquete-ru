class Config(object):
    DEBUG = False
    TESTING = True
    SECRET_KEY = 'kajsxbkfbkjdsafzsdfkzcsfukvfusgzhcgfadsuzhbfhzcvadsf'
    MONGOALCHEMY_DATABASE = 'enqueteru'
    LATEST_API_VERSION = '1'


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
