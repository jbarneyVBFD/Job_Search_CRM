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

# Error handlers
@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(error=str(e)), 500

if __name__ == "__main__":
    app.run(debug=True)
