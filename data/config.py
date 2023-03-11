import os
basedir = os.path.abspath(os.path.dirname(__file__))


SECRET_KEY = 'secret-key-goes-here'
MAX_CONTENT_LENGTH = 1024 * 1024
UPLOADED_PHOTOS_DEST = os.path.join(basedir, '../static/uploads')