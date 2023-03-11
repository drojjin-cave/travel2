from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import  SubmitField
from wtforms.validators import DataRequired

from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage



class NewsForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField("Содержание")
    add = SubmitField('Добавить/изменить')
    photos = UploadSet('photos', IMAGES)
    photo = FileField()
    delete_foto = SubmitField('Удалить обложку')
