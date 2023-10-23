from main import db, app
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
class Community(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    community = db.Column(db.String(255))
    program = db.Column(db.String(255), nullable=False)
    subprogram = db.Column(db.String(255), nullable=False)
    week = db.Column(db.Integer, nullable=True)
    totalWeek = db.Column(db.Integer, nullable=False)
    user =db.Column(db.String(255), unique=True, nullable=False)
    

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    program = db.Column(db.String(255), nullable=False)


class Program(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    program = db.Column(db.String(255), unique=True, nullable=False)

class Subprogram(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    program = db.Column(db.String(255), nullable=False)
    subprogram = db.Column(db.String(255), nullable=False)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(255), nullable=False)

# ----------------------- Upload Files ------------------------------------
class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)

# Create the database tables
with app.app_context():
    db.create_all()




###################### QUERIES #########################


def create_tables_and_insert_subprogram():
    subprograms_to_insert = [
        Subprogram(program='Literacy', subprogram='Sub-Literacy2'),
        Subprogram(program='Socio-economic', subprogram='Sub-Socio-economic2'),
        Subprogram(program='Environmental Stewardship', subprogram='Sub-Environmental Stewardship2' ),
        Subprogram(program='Health and Wellness', subprogram='Sub-Health and Wellness2'),
        Subprogram(program='Cultural Enhancement', subprogram='Sub-Cultural Enhancement2'),
        Subprogram(program='Values Formation', subprogram='Sub-Values Formation2'),
        Subprogram(program='Disaster Management', subprogram='Sub-Disaster Management2'),
        Subprogram(program='Sub-Gender and Development', subprogram='Sub-Gender and Development2')
    ]

    programs_to_insert = [
        Program(program='Literacy'),
        Program(program='Socio-economic'),
        Program(program='Environmental Stewardship'),
        Program(program='Health and Wellness'),
        Program(program='Cultural Enhancement'),
        Program(program='Values Formation'),
        Program(program='Disaster Management'),
        Program(program='Sub-Gender and Development'),
    ]

    programs_to_role = [
        Role(role='Admin'),
        Role(role='Coordinator')
    ]

    db.session.add_all()
    db.session.commit()

@app.route('/db')
def initialize_database():
    create_tables_and_insert_subprogram()
    return 'Subprogram.'

@app.route('/test')
def display_subprograms():

    return render_template('test.html')


