import os, uuid
from ..models import db, Documents
from flask import render_template, send_from_directory, session, redirect, url_for, flash, current_app, abort
from . import main
from .. import db
from flask_login import login_required, current_user
from .forms import ChatForm
from .utils import extract_text_from_file, allowed_files, cohere_summarizer
import tempfile
# for creating PDF summaries
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

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
        summarized_text: str = ""

        if file_input and allowed_files(file_input.filename):
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                file_input.save(temp_file.name)
                extracted_text = extract_text_from_file(temp_file.name)
        
        elif extracted_text:
            extracted_text = text_input
        
        else:
            flash('Please upload a docx, pdf, or txt file. Or just paste content in the textbox.', 'error')
            return redirect(url_for('main.upload_file'))

        try:
            summarized_text = cohere_summarizer(extracted_text)
        except Exception as e:
            flash(f"Error during summarization", 'error')
            print(f"Error during summarization:  {str(e)}")
            return redirect(url_for('main.upload_file'))
        
        # persist summary as .pdf
        doc_id = uuid.uuid4().hex[:12]
        summary_filename = f'summary_{doc_id}.pdf'
        summary_filepath = os.path.join(current_app.config['SUMMARY_FOLDER'], summary_filename)
        c = canvas.Canvas(summary_filepath, pagesize=letter)
        text_object = c.beginText(40, 750)
        for line in summarized_text.split('\n'):
            text_object.textLine(line)
        c.drawText(text_object)
        c.save()
        
        # save document info to the database
        document = Documents(
            user_id=current_user.id,
            title=file_input.filename if file_input else 'Text Input',
            summary_filepath=summary_filepath
        )
        
        db.session.add(document)
        db.session.commit()
        

        flash('Summary generated and saved.', 'success')
        return redirect(url_for('main.home'))
    
    return render_template('chat.html', form=form)


def _safe_remove(file_path):
    """Safely remove a file if it exists."""
    try:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
    except:
        pass
    
    
@main.route('/documents', methods=['GET'])
@login_required
def list_documents():
    """List all summarized documents for the current user."""
    documents = Documents.query.filter_by(user_id=current_user.id).all()
    return render_template('documents.html', documents=documents)

@main.route('/documents/<int:doc_id>/download', methods=['GET'])
@login_required
def download(doc_id):
    doc = Documents.query.get_or_404(doc_id)
    if doc.user_id != current_user.id:
        abort(403)  # Forbidden access
        
    folder, filename = os.path.dirname(doc.summary_filepath), os.path.basename(doc.summary_filepath)
    if not os.path.exists(doc.summary_filepath):
        flash('File missing on server.', 'error')
        return redirect(url_for('main.list_documents'))

    return send_from_directory(folder, filename, as_attachment=True, download_name=doc.title + '.pdf')

@main.route('/documents/<int:doc_id>/delete', methods=['POST'])
@login_required
def delete_document(doc_id):
    doc = Documents.query.get_or_404(doc_id)
    if doc.user_id != current_user.id:
        abort(403)
        
    _safe_remove(doc.summary_filepath)
    db.session.delete(doc)
    db.session.commit()
    flash('Document deleted successfully.', 'success')
    return redirect(url_for('main.list_documents'))
