import os, uuid
from ..models import db, Documents
from flask import render_template, send_from_directory, session, redirect, url_for, flash, current_app, abort
from . import main
from .. import db
from flask_login import login_required, current_user
from .forms import ChatForm
from .utils import extract_text_from_file, allowed_files, cohere_summarizer
import markdown2
from markdown_pdf import MarkdownPdf, Section

@main.route('/', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        return redirect(url_for('main.chat'))

    return render_template('index.html')

@main.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    form = ChatForm()
    messages = []
    documents = Documents.query.filter_by(user_id=current_user.id).all()  # fetch docs for sidebar

    if form.validate_on_submit():
        text_input = form.message.data
        file_input = form.file.data
        
        extracted_text = None
        summarized_text = ""

        if file_input and allowed_files(file_input.filename):
            print("File uploaded")
            print(file_input.filename)
            extracted_text = extract_text_from_file(file_input)
        
        elif text_input:
            extracted_text = text_input
        
        else:
            flash('Please upload a docx, pdf, or txt file. Or just paste content in the textbox.', 'error')
            return redirect(url_for('main.chat'))

        try:
            summarized_text = cohere_summarizer(extracted_text)
        except Exception as e:
            flash(f"Error during summarization", 'error')
            print(f"Error during summarization:  {str(e)}")
            return redirect(url_for('main.chat'))
        
        # persist summary as .pdf
        doc_id = uuid.uuid4().hex[:12]
        summary_filename = f'summary_{doc_id}.pdf'
        summary_filepath = os.path.join(current_app.config['SUMMARY_FOLDER'], summary_filename)
        
        summary_pdf = MarkdownPdf()
        summary_pdf.add_section(Section(summarized_text))
        summary_pdf.save(summary_filepath)

        # save document info to the database
        document = Documents(
            user_id=current_user.id,
            title=file_input.filename if file_input else 'Text Input',
            summary_filepath=summary_filepath
        )
        
        db.session.add(document)
        db.session.commit()
        
        # Add message for display
        if text_input:
            messages.append({"user": "me", "text": markdown2.markdown(text_input)})
        if summarized_text:
             messages.append({"user": "other", "text": markdown2.markdown(summarized_text)})

        flash('Summary generated and saved.', 'success')
        return render_template('chat.html', form=form, messages=messages, documents=documents)
    
    else:
        print("Not validated")

    
    return render_template('chat.html', form=form, messages=messages, documents=documents)



def _safe_remove(file_path):
    """Safely remove a file if it exists."""
    try:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
    except:
        pass
    

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
    return redirect(url_for('main.chat'))
