from flask import Flask, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(100), nullable=False)

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=False)
    type = db.Column(db.String(100), nullable=False)  # e.g., 'Email', 'Phone call', 'Interview'
    details = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    details = db.Column(db.String(300), nullable=False)
    due_date = db.Column(db.DateTime)
    completed = db.Column(db.Boolean, default=False)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))

db.create_all()

# Create tables
db.create_all()

# User Loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def home():
    return "Welcome to the Job Search CRM!"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        return 'Invalid username or password'
    return '''
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/contacts', methods=['POST'])
@login_required
def add_contact():
    data = request.get_json()
    new_contact = Contact(name=data['name'], email=data['email'])
    db.session.add(new_contact)
    db.session.commit()
    return jsonify({'id': new_contact.id}), 201

@app.route('/contacts', methods=['GET'])
@login_required
def get_contacts():
    contacts = Contact.query.all()
    return jsonify([{'id': contact.id, 'name': contact.name, 'email': contact.email} for contact in contacts])

@app.route('/applications/<int:id>', methods=['PUT'])
@login_required
def update_application_status(id):
    data = request.get_json()
    application = Application.query.get(id)
    if application:
        application.status = data['status']
        db.session.commit()
        return jsonify({'id': id, 'new_status': data['status']}), 200
    return jsonify({'error': 'Application not found'}), 404

@app.route('/activities', methods=['POST'])
@login_required
def add_activity():
    data = request.get_json()
    new_activity = Activity(contact_id=data['contact_id'], type=data['type'], details=data['details'])
    db.session.add(new_activity)
    db.session.commit()
    return jsonify({'id': new_activity.id}), 201

@app.route('/activities/<int:contact_id>', methods=['GET'])
@login_required
def get_activities(contact_id):
    activities = Activity.query.filter_by(contact_id=contact_id).all()
    return jsonify([{'id': activity.id, 'type': activity.type, 'details': activity.details, 'timestamp': activity.timestamp} for activity in activities])

@app.route('/tasks', methods=['POST'])
@login_required
def add_task():
    data = request.get_json()
    new_task = Task(details=data['details'], due_date=data['due_date'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'id': new_task.id}), 201

@app.route('/tasks', methods=['GET'])
@login_required
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{'id': task.id, 'details': task.details, 'due_date': task.due_date, 'completed': task.completed} for task in tasks])

@app.route('/tasks/<int:task_id>/complete', methods=['PUT'])
@login_required
def complete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed = True
        db.session.commit()
        return jsonify({'id': task_id, 'completed': True}), 200
    return jsonify({'error': 'Task not found'}), 404

@app.route('/notes', methods=['POST'])
@login_required
def add_note():
    data = request.get_json()
    new_note = Note(content=data['content'], contact_id=data['contact_id'])
    db.session.add(new_note)
    db.session.commit()
    return jsonify({'id': new_note.id}), 201

@app.route('/notes/<int:contact_id>', methods=['GET'])
@login_required
def get_notes(contact_id):
    notes = Note.query.filter_by(contact_id=contact_id).all()
    return jsonify([{'id': note.id, 'content': note.content} for note in notes])

# Error handlers
@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(error=str(e)), 500

if __name__ == "__main__":
    app.run(debug=True)
