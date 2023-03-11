Если создаете свое виртуальное окружение!
В файле "flask_uploads.py" некорректо импортирована библиотека werkzeug.  
В файле site-packages\flask_uploads.py
вместо 
from werkzeug import secure_filename,FileStorage
необходимо написать
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

