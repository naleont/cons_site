from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, PrimaryKeyConstraint

db = SQLAlchemy()
db_name = 'consultation.db'


class Works(db.Model):
    __tablename__ = 'works'

    appl_id = db.Column('appl_id', db.Integer, primary_key=True)
    work_name = db.Column('work_name', db.Text)
    area = db.Column('area', db.Text)
    participating = db.Column('participating', db.Boolean)
    email = db.Column('email', db.Text)
    stage = db.Column('stage', db.Text) #

    def __init__(self, work_name, area, participating, email, stage):
        self.work_name = work_name
        self.area = area
        self.participating = participating
        self.email = email
        self.stage = stage


class People(db.Model):
    __tablename__ = 'people'

    person_id = db.Column('person_id', db.Integer, primary_key=True)
    name = db.Column('name', db.Text)
    grade = db.Column('grade', db.Integer)
    role = db.Column('role', db.Text) #

    def __init__(self, name, role, grade):
        self.name = name
        self.grade = grade
        self.role = role #


# class Roles(db.Model):
#     __tablename__ = 'roles'
#
#     role_id = db.Column('role_id', db.Integer, primary_key=True)
#     role_name = db.Column('role_name', db.Text)
#
#     def __init__(self, role_name):
#         self.role_name = role_name


# class Stages(db.Model):
#     __tablename__ = 'stages'
#
#     stage_id = db.Column('stage_id', db.Integer, primary_key=True)
#     stage = db.Column('stage', db.Text)


class WorkNumbers(db.Model):
    __tablename__ = 'work_numbers'
    __table_args__ = (PrimaryKeyConstraint('appl_id'),)

    appl_id = db.Column('appl_id', db.Integer, ForeignKey('works.appl_id'))
    work_no = db.Column('work_no', db.Integer)

    def __init__(self, appl_id, work_no):
        self.appl_id = appl_id
        self.work_no = work_no


class Participants(db.Model):
    __tablename__ = 'participants'
    __table_args__ = (PrimaryKeyConstraint('appl_id', 'author_id', 'supervisor_id'),)

    appl_id = db.Column('appl_id', db.Integer, ForeignKey('works.appl_id'))
    author_id = db.Column('author_id', db.Integer, ForeignKey('people.person_id'))
    supervisor_id = db.Column('supervisor_id', db.Integer, ForeignKey('people.person_id'))
    # role_id = db.Column('role_id', db.Integer, ForeignKey('roles.role_id'))

    def __init__(self, appl_id, author_id, supervisor_id):
        self.appl_id = appl_id
        self.author_id = author_id
        self.supervisor_id = supervisor_id