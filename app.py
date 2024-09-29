import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
current_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
#esp
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(current_dir, "user.sqlite3")
app.config['SECRET_KEY'] = 'xYxx1528'

db = SQLAlchemy(app)
app.app_context().push()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Auto-incrementing ID
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email (must be unique)
    full_name = db.Column(db.String(120), nullable=False)  # Full name
    password = db.Column(db.String(120), nullable=False)  # Hashed password
    address = db.Column(db.String(255), nullable=False)  # Address
    pincode = db.Column(db.String(10), nullable=False)  # Pincode
    
    def set_password(self, password):
        """Hashes the password before saving."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Verifies the password during login."""
        return check_password_hash(self.password, password)
    

class professionals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    service_name = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    document = db.Column(db.LargeBinary, nullable=True)  # Store PDF in BLOB
    address = db.Column(db.String(500), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)

    def set_password(self, password):
        """Hashes the password before saving."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Verifies the password during login."""
        return check_password_hash(self.password, password)

@app.route("/",methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Fetch the user by email
        user = User.query.filter_by(email=email).first()
        user2 = professionals.query.filter_by(email=email).first()

        # Check if the user exists and verify the password
        if user and user.check_password(password):
            session['user_id'] = user.id
            flash('Login successful!')
            return redirect(url_for('cdash'))
        elif user2 and user2.check_password(password):
            session['user_id'] = user2.id
            return redirect(url_for('pdashboard'))
        else:
            return render_template('rnf.html')

    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        full_name = request.form['full_name']
        password = request.form['password']
        address = request.form['address']
        pincode = request.form['pincode']
        
        # Check if the email is already registered
        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please log in.')
            return redirect(url_for('login'))
        
        # Create a new user and hash the password
        new_user = User(email=email, full_name=full_name, address=address, pincode=pincode)
        new_user.set_password(password)

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))

    return render_template('customer.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']
        service_name = request.form['service_name']
        experience = request.form['experience']
        address = request.form['address']
        pincode = request.form['pincode']
        
        # Handle file upload
        if 'document' not in request.files:
            return 'No document part'
        
        file = request.files['document']
        
        if file.filename == '':
            return 'No selected file'
        
        if file and file.filename.endswith('.pdf'):
            # Read the PDF in binary mode
            document_data = file.read()
            
            # Create a new User object
            new_user = professionals(
                full_name=full_name,
                email=email,
                service_name=service_name,
                experience=experience,
                document=document_data,
                address=address,
                pincode=pincode
            )
            new_user.set_password(password)
            
            # Add to the session and commit
            db.session.add(new_user)
            db.session.commit()
            
            return redirect(url_for('login'))

    return render_template('profes_login.html')

@app.route("/pdashboard")
def pdashboard():
    return render_template('professionals.html')

@app.route("/customer")
def customer():
    return render_template('customer.html')
@app.route("/profes_login")
def profes_login():
    return render_template('profes_login.html')

@app.route('/cdash')
def cdash():
    return render_template('cdash.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5500, debug=True)