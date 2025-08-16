from flask_wtf import FlaskForm
from wtforms import FileField, TextAreaField, SubmitField

class ChatForm(FlaskForm):
    message = TextAreaField('Message', render_kw={"rows": 3, "cols": 50})
    file = FileField('Upload File')
    submit = SubmitField('Send')
