from flask import Flask
from flask import render_template, request
from models import db, Works, People, WorkNumbers, Participants  # , Roles, Stages
from sqlalchemy.sql import func, select

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///consultation.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = app
db.init_app(app)
db.create_all()


def write_application(res, additional):
    try:
        works = Works(res['Название работы'], res['Область работы'], additional['participating'],
                      res['e-mail'], additional['stage'])
        db.session.add(works)
        db.session.commit()
        appl_id = works.appl_id
        people = People(res['Автор(ы)'], 'Автор', res['Класс автора(ов)'])
        db.session.add(people)
        db.session.commit()
        author_id = people.person_id
        people = People(res['Руководитель(и)'], 'Руководитель', None)
        db.session.add(people)
        db.session.commit()
        supervisor_id = people.person_id
        if 'Номер работы' in res.keys():
            work_no = WorkNumbers(appl_id, res['Номер работы'])
            db.session.add(work_no)
            db.session.commit()
        participants = Participants(appl_id, author_id, supervisor_id)
        db.session.add(participants)
        db.session.commit()

        success = 'отправлена'

    except Exception as e:
        print(e)
        success = 'не отправлена'
    return success


def get_stats():
    appl_num = db.session.query(Works).count()
    youngest = db.session.execute(select([func.min(People.grade)])).fetchone()[0]
    oldest = db.session.execute(select([func.max(People.grade)])).fetchone()[0]
    appl_grade = {}
    for grade in range(5, 12):
        appl_grade[grade] = db.session.query(People).filter(People.grade == grade).count()
    most_appl_grade = max(appl_grade, key=appl_grade.get)
    areas = db.session.execute(select(Works.area)).fetchall()
    areas = [ar[0] for ar in areas]
    areas_dict = {}
    for area in areas:
        areas_dict[area] = areas.count(area)
    most_appl_area = max(areas_dict, key=areas_dict.get)
    return appl_num, youngest, oldest, most_appl_grade, most_appl_area


@app.route('/')
def main_page():
    return render_template('new_main.html')


@app.route('/apply')
def apply():
    return render_template('new_form.html')


@app.route('/results')
def results():
    res = {}
    res['e-mail'] = request.values.get('email', str)
    email = request.values.get('email', str)
    res['Название работы'] = request.values.get('work_name', str)
    res['Область работы'] = request.values.get('area', str)
    if request.values.get('work_no', str):
        res['Номер работы'] = request.values.get('work_no', str)
    res['Автор(ы)'] = request.values.get('authors', str)
    res['Руководитель(и)'] = request.values.get('supervisor', str)
    res['Класс автора(ов)'] = request.values.get('grade', int)
    additional = {}
    if request.values.get('participation', str) == 'yes':
        additional['participating'] = True
    elif request.values.get('participation', str) == 'no':
        additional['participating'] = False
    additional['stage'] = request.values.get('stage', str)
    success = write_application(res, additional)
    return render_template('application_successful.html', res=res, email=email, success=success)


@app.route('/application_successful')
def application_successful():
    return render_template('application_successful.html')


@app.route('/statistics')
def stats():
    appl_num, youngest, oldest, most_appl_grade, most_appl_area = get_stats()
    return render_template('stats.html', appl_num=appl_num, youngest=youngest, oldest=oldest,
                           most_appl_grade=most_appl_grade, most_appl_area=most_appl_area)


if __name__ == '__main__':
    app.run(debug=False)
