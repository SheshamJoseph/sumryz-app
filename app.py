from config import configs
import os
from app import create_app, db 
from app.models import User

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User)


@app.cli.command("init-db")
def init_db():
    """Create all database tables."""
    db.create_all()
    print("Database tables created.")

if __name__ == "__main__":
    app.run(debug=True)
