from curses import flash
from flask import render_template, session, redirect, url_for
from . import main
from .. import db
from flask_login import login_required, current_user
from .forms import ChatForm
from .utils import extract_text_from_file, allowed_files
import tempfile

@main.route('/', methods=['GET', 'POST'])
def home():

    return render_template('index.html')

@main.route('/chat', methods=['GET', 'POST'])
@login_required
def upload_file():
    form = ChatForm()
    if form.validate_on_submit():
        text_input = form.message.data
        file_input = form.file.data
        
        extracted_text = None
        
        if file_input and allowed_files(file_input.filename):
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                file_input.save(temp_file.name)
                extracted_text = extract_text_from_file(temp_file.name)
        
        elif extracted_text:
            extracted_text = text_input
        
        else:
            flash('Please upload a docx, pdf, or txt file. Or just paste content in the textbox.', 'error')
            return redirect(url_for('main.upload_file'))

        summarized_text = "This is a placeholder for the summarized text."  # Replace with actual summarization logic

        flash('Message sent successfully!', 'success')
        return redirect(url_for('main.home'))
    
    return render_template('chat.html', form=form)
