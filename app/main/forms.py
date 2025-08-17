from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import Optional
from flask_wtf.file import FileAllowed, FileField

class ChatForm(FlaskForm):
    message = TextAreaField('Paste text', render_kw={"rows": 1, "cols": 50}, validators=[Optional()])
    file = FileField('Upload File',  validators=[Optional(), FileAllowed(('pdf', 'docx', 'txt'))])
    submit = SubmitField('Send')
