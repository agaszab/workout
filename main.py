import binascii
import hashlib
from forms import *
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_bcrypt import Bcrypt

mydb = mysql.connector.connect(user='root', password='kociakolka', host='127.0.0.1', database='workout')
mycursor = mydb.cursor()

app = Flask(__name__)  # __name__ oznacza, że jest to ta strona jest do zarządzania, tworzymy instancję klasy flaskowej

bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# @login_manager.user_loader     -> wersja z netu
# def load_user(user_id):
#     return User.query.get(int(user_id))
@login_manager.user_loader    # wersja z kursu udemy
def load_user(id):
    return User.query.filter(User.id == id).first()


db.init_app(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)




with app.app_context():
    db.create_all()



def __init__(self, user='', password=''):
    self.user = user
    self.password = password


def hash_password(self):
    """Hash a password for storing."""
    # the value generated using os.urandom(60)
    os_urandom_static = b"ID_\x12p:\\x8d\xe7&\xcb\x70=H1\xc1\x16\xac\xe5BX\xd7\xd6j\xe3i\x11\xbe\xc2"
    salt = hashlib.sha256(os_urandom_static).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', self.password.encode('utf8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(self, stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

def three_last():
    sql = "Select distinct data_from, data_to from plan order by data_from desc limit 3"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    print(myresult)
    data_from = myresult[2][0]
    data_to = myresult[0][1]
    print(type(data_from))
    print(data_to)
    return data_from, data_to

# def login_user(self):
#     sql="select idu, login, pass from users where login=?"
#     mycursor.execute(sql)
#     myresult = mycursor.fetchone()
#
#     if myresult != None and self.verify_password(myresult['pass'], self.password):
#         return  myresult
#     else:
#         self.user = None
#         self.password = None
#         return None

def pokaz_plany(sql):
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    plany = []
    for x in myresult:
        plany.append(x)
    return plany


def pokaz_zakres2(start, stop):
    print(start)
    print(stop)
    sql = "SELECT plan.data_from, plan.data_to, plan.day, exercise.body_part, exercise.name, exercise.description, series.number_sets, series.number_repeats, series.weight, series.superseries, series.set FROM plan, series, exercise where data_from BETWEEN '" + start + "' AND '" + stop + "' and plan.id_series = series.ids and series.id_exercise = ide"
    # sql= "SELECT kurs_pl, any_value('id', 'kurs_usd, data, godzina') FROM kursy where data BETWEEN '"+start+"' AND '"+stop+"' "
    # print(sql)
    list = pokaz_trening(sql)
    return list


def pokaz(sql):
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    print(myresult)
    cwiczenia = []
    for x in myresult:
        cwiczenie = [x[0], x[1], x[2], x[3]]
        cwiczenia.append(cwiczenie)
        # print(str(x[0])+" USD, ",str(x[1])+" PL, -> ",x[2],x[3],x[4])
        # print(myresult)
    print(cwiczenia)
    return cwiczenia


def pokaz_plan2(day, data_from):

    data = str(data_from)

    sql_body_part = """select distinct e.body_part from workout.exercise e inner join workout.series s 
                    on e.ide = s.id_exercise 
                        inner join workout.plan p
                        on p.id_series=s.ids  
                    where p.data_from = '""" + data + """' and p.day=""" + day
    mycursor.execute(sql_body_part)
    body_part = mycursor.fetchall()
    part = []
    for item in body_part:
        part.append(item[0])

    print(part)

    sql = """
                select  p.data_from, p.data_to, p.day, e.name, e.description, e.body_part, s.number_sets, s.number_repeats, s.weight, s.superseries, s.set, p.order, c.body_part_count, e.ide 
                    from exercise e inner join series s 
                    on e.ide = s.id_exercise 
                        inner join plan p
                        on p.id_series=s.ids  
                        inner join ( select  p.data_from as date_count, p.day, count(distinct e.body_part) as body_part_count
							from exercise e inner join series s 
								on e.ide = s.id_exercise 
								inner join plan p
									on p.id_series=s.ids group by p.data_from, p.day )  c 
						on c.date_count=p.data_from and p.day=c.day
                    where p.data_from = '""" + data + """' and p.day=""" + day + """  order by p.order
              """
    print(sql)
    print("_8_")
    mycursor.execute(sql)
    myresult_pom = mycursor.fetchall()
    print(myresult_pom)
    plan1 = []
    plan2 = []

    if (len(myresult_pom) == 0):
        print("brak planu")
        return render_template('nodata.html', data_from=data_from)
    else:
        part = myresult_pom[0][5]
        for x in myresult_pom:
            if x[5] == part:
                plan_1 = [x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9], x[10], x[11], x[12], x[13]]
                plan1.append(plan_1)
            else:
                plan_2 = [x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9], x[10], x[11], x[12], x[13]]
                plan2.append(plan_2)

    print(plan1)
    print("++++++++++++++++++++++++++++")
    print(plan2)
    print("++++++++++++++++++++++++++++")
    return plan1, plan2, data_from, part


def pokaz_plan(day, data_from):
    # mycursor.execute("select data_from from plan order by data_from desc limit 1")
    # myresult = mycursor.fetchall()
    # data = str(myresult[0][0])
    # print(data)
    # print(day)

    data = str(data_from)
    sql_body_part = """select distinct e.body_part from workout.exercise e inner join workout.series s 
                        on e.ide = s.id_exercise 
                            inner join workout.plan p
                            on p.id_series=s.ids  
                        where p.data_from = '""" + data + """' and p.day=""" + str(day)
    mycursor.execute(sql_body_part)
    body_part = mycursor.fetchall()
    part = []
    for item in body_part:
        part.append(item[0])

    print(part)
    sql_pom = """
                select  p.data_from, p.data_to, p.day, e.name, e.description, e.body_part, s.number_sets, s.number_repeats, s.weight, s.superseries, s.set, p.order, c.body_part_count, e.ide 
                    from exercise e inner join series s 
                    on e.ide = s.id_exercise 
                        inner join plan p
                        on p.id_series=s.ids  
                        inner join ( select  p.data_from as date_count, p.day, count(distinct e.body_part) as body_part_count
							from exercise e inner join series s 
								on e.ide = s.id_exercise 
								inner join plan p
									on p.id_series=s.ids group by p.data_from, p.day )  c 
						on c.date_count=p.data_from and p.day=c.day
                    where p.data_from = '""" + data + """' and p.day=""" + str(day) + """  order by p.order
              """
    print(sql_pom)
    mycursor.execute(sql_pom)
    myresult_pom = mycursor.fetchall()
    print(myresult_pom)
    # body_part = myresult_pom[0][5]
    # print(body_part)
    plan1 = []
    plan2 = []
    for x in myresult_pom:
        if x[5] == part[0]:
            plan_1 = [x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9], x[10], x[11], x[12], x[13]]
            plan1.append(plan_1)
        else:
            plan_2 = [x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9], x[10], x[11], x[12], x[13]]
            plan2.append(plan_2)
    print(part)

    return plan1, plan2, part


def pokaz_ex(sql):
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    print(myresult)
    cwiczenia = []
    for x in myresult:
        cwiczenie = [x[0], x[1]]
        cwiczenia.append(cwiczenie)
    return cwiczenia

def pokaz_pl(sql):
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    print(myresult)
    serie = []
    for x in myresult:
        seria = [x[2], x[3],x[4], x[5], x[6]]
        serie.append(seria)
    return serie

def pokaz_trening(sql):
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    print(myresult)
    trening = []
    for x in myresult:
        trening.append(x)
    return trening


def add_exercise(name, description, body_part, mydb):
    print(name)
    print(description)
    print(body_part)
    sql = f"INSERT INTO exercise(name, description, body_part) VALUES ('" + name + "','" + description + "','" + body_part + "')"
    cursor = mydb.cursor()
    cursor.execute(sql)
    mydb.commit()


def update_exercise(id, name, description, body_part, mydb):
    print(name)
    print(description)
    print(body_part)
    sql = f"UPDATE exercise SET name='" + name + "' , description='" + description + "', body_part='" + body_part +"' WHERE ide="+ id
    # sql=f"INSERT INTO exercise(name, description, body_part) VALUES ('"+name+"','"+description+"','"+body_part+"')"
    cursor = mydb.cursor()
    cursor.execute(sql)
    mydb.commit()


def add_series(id_exercise, number_sets, number_repeats, weight, superseries, set, mydb):
    id = str(id_exercise)
    # set_s=str(set)
    # nb=str(number_sets)
    sql = "INSERT INTO `workout`.`series` (`id_exercise`, `number_sets`, `number_repeats`, `weight`, `superseries`, `set`) VALUES (" + id + "," + number_sets + ",'" + number_repeats + "','" + weight + "'," + superseries + "," + set + ")"
    #  sql="INSERT INTO series (id_exercise, number_sets, number_repeats, weight, superseries, set) VALUES ("+id+","+number_sets+",'"+number_repeats+"','"+weight+"',"+superseries+","+set+")"""
    print(sql)
    cursor = mydb.cursor()
    cursor.execute(sql)
    mydb.commit()
    # cursor = mydb.cursor()
    # cursor.execute(sql)
    # mydb.commit()


def edit_series(id_exercise, number_sets, number_repeats, weight, superseries, set, mydb):
    id = str(id_exercise)
    # set_s=str(set)
    # nb=str(number_sets)
    sql = "INSERT INTO `workout`.`series` (`id_exercise`, `number_sets`, `number_repeats`, `weight`, `superseries`, `set`) VALUES (" + id + "," + number_sets + ",'" + number_repeats + "','" + weight + "'," + superseries + "," + set + ")"
    #  sql="INSERT INTO series (id_exercise, number_sets, number_repeats, weight, superseries, set) VALUES ("+id+","+number_sets+",'"+number_repeats+"','"+weight+"',"+superseries+","+set+")"""
    print(sql)
    # cursor = mydb.cursor()
    # cursor.execute(sql)
    # mydb.commit()


def kiedy_cwiczenie(id):
    sql = """select p.data_from, p.data_to, p.day, e.name, e.description, e.body_part, s.number_sets, s.number_repeats, s.weight, s.superseries, s.set, p.order 
                    from exercise e inner join series s 
                    on e.ide = s.id_exercise 
                    inner join plan p
                    on p.id_series=s.ids  
                    where e.ide=""" + str(id) + """ order by p.data_from desc limit 1"""
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    if myresult == []:
        kiedy = "nigdy nie wystąpiło w planach"
    else:
        kiedy_start = myresult[0][0]
        kiedy_stop = myresult[0][1]
        kiedy = "od: " + str(kiedy_start) + " do: " + str(kiedy_stop)
    return kiedy


def ile_razy_cwiczenie(id):
    sql = """
    select count(*) as ile from exercise e inner join series s 
        	    on e.ide = s.id_exercise 
                where e.ide=""" + str(id) + " group by e.ide"

    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    if myresult == []:
        ile_razy = 0
    else:
        ile_razy = myresult[0][0]
    return ile_razy


def wykaz_serii(id):
    sql = "SELECT * FROM series s inner join plan p on s.ids=p.id_series where s.id_exercise=" + str(
        id) + " order by data_from"
    mycursor.execute(sql)
    wynik = mycursor.fetchall()
    return wynik


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    # sql = "select * from exercise order by body_part"
    # wynik = pokaz(sql)
    # list = pokaz("SELECT * FROM kursy")
    # print(list)
    # return render_template('index.html')
    # return render_template('index.html', form=form, wynik=wynik)
    return render_template('index.html')

@app.route('/nodata', methods=['GET', 'POST'])
def nodata():
    return redirect(url_for('nodata'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('panel'))
    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


# @app.route('/userHome')
# def userHome():
#     return render_template('userHome.html')


@app.route('/subpage', methods=['GET', 'POST'])
def subpage():
    form = SearchForm()
    sql = "select * from exercise order by body_part"
    wynik = pokaz(sql)
    # list = pokaz("SELECT * FROM kursy")
    # print(list)
    # return render_template('index.html')
    return render_template('subpage.html', form=form, wynik=wynik)


@app.route('/exercise', methods=['GET', 'POST'])
def exercise():
    id = request.args['id']
    sql = "select * from exercise where ide=" + id
    mycursor.execute(sql)
    wynik = mycursor.fetchall()
    print(wynik)
    ile_razy = ile_razy_cwiczenie(wynik[0][0])
    print(ile_razy)
    kiedy = kiedy_cwiczenie(wynik[0][0])
    print(kiedy)
    serie = wykaz_serii(wynik[0][0])
    print(serie)
    return render_template('exercise.html', wynik=wynik, ile_razy=ile_razy, kiedy=kiedy, serie=serie)


@app.route('/exercises', methods=['GET', 'POST'])
def exercises():
    print(request.args['part'])


    if request.args['part'] and request.args[
        'part'] != "no":  # jeśli jest party=no to znaczy, że link przyszedł bezpośrednio z menu bocznego 'wykaz ćwiczen'
        part = request.args['part']
        if request.args['part'] != "all":
            sql = "select * from exercise where body_part='" + part + "' order by name"
        else:
            sql = "select * from exercise order by body_part"
        mycursor.execute(sql)
        wynik = mycursor.fetchall()
        print(wynik)
    else:
        wynik = []
        part = ""

    wynik_caly = []
    if wynik != []:

        for elem in wynik:
            ile_razy = ile_razy_cwiczenie(elem[0])
            print(ile_razy)
            kiedy = kiedy_cwiczenie(elem[0])
            print(kiedy)
            pom = [elem, ile_razy, kiedy]
            wynik_caly.append(pom)
    print(wynik_caly)
    print(part)
    return render_template('exercises.html', wynik=wynik_caly, part=part)


@app.route("/plan", methods=["GET", "POST"])
def plan():

    if request.args['day']:  # domyslnie pierwszy dzień treningowy, w sumie są cztery
        day = request.args['day']
    else:
        day = 1

    if request.args['data_from'] == '2020-01-01':
        mycursor.execute("select data_from from plan order by data_from desc limit 1")
        myresult = mycursor.fetchall()
        date = str(myresult[0][0])
    else:
        date = request.args['data_from']

    wynik = pokaz_plan(day, date)
    body_part = wynik[2]

    print(wynik)
    # body_part="plecy"
    print(body_part)
    # print(len(wynik[1]))
    # print("to jest wynik[0]:")
    # print(len(wynik[0]))

    if (len(wynik) == 0):
        print("tu jestem")
        return render_template('plan.html', day=day, wynik=wynik, pom=2)

    if len(wynik[1]) == 0:  # sprawdzanie czy plan jest na dwie partie czy na jedną np tylko nogi, dla pom=0 nie jest wyświedlana druga kolumna na stronie
        pom = 0
    else:
        pom = 1

    print(pom)
    print(day)
    print(wynik)
    return render_template('plan.html', day=day, wynik=wynik, pom=pom, body_part=body_part)

@app.route("/plan_from", methods=["GET", "POST"])
def plan_from():
    form = SearchForm()
    if request.method == 'POST':
        date = form.startdate.data
        print(date)
        mycursor.execute("SELECT data_from FROM workout.plan where  data_from < '"+str(date)+"' and data_to > '"+str(date)+"' order by data_from desc limit 1")
        myresult = mycursor.fetchall()

    if len(myresult)==0:
        return render_template('nodata.html')
    else:
        data_from = str(myresult[0][0])
        print(data_from)
        day = 1
        wynik = pokaz_plan(day, data_from)
        body_part = wynik[2]
        if len(wynik[2])==1:
            pom = 0
        if len(wynik[2])==2:
            pom = 1
        else:
            pom = 1

    return render_template('plan.html', day=day, wynik=wynik, pom=pom, body_part=body_part)

@app.route("/plan2", methods=["GET", "POST"])
def plan2():
    form = SearchForm()

    if request.args['day']:  # domyslnie pierwszy dzień treningowy, w sumie są cztery
        day = request.args['day']
    else:
        day = 1

    if request.method == 'POST':
        data_from = form.startdate.data
        day = 1
    else:
        data_from = request.args['data_from']

    print(data_from)
    wynik = pokaz_plan2(day, data_from)
    print("wynik")
    print(wynik)
    body_part=wynik[3]
    print(body_part)

    if (len(wynik) == 0):
        return render_template('nodata.html', data_from=data_from)

    if (len(wynik[1]) == 0):  # sprawdzanie czy plan jest na dwie partie czy na jedną np tylko nogi, dla pom=0 nie jest wyświedlana druga kolumna na stronie
        pom = 0
    else:
        pom = 1
    return render_template('plan.html', day=day, wynik=wynik, pom=pom, body_part=body_part)


@app.route("/plans", methods=["GET", "POST"])
def plans():
    sql = "select distinct data_from, data_to from plan order by data_from"
    wynik = pokaz_plany(sql)
    form = SearchForm()
    return render_template('plans.html', form=form, wynik=wynik)


@app.route("/statistic", methods=["GET", "POST"])
def statistic():
    sql=""
    tytul = ""

    if request.args['opt']:                     # part 1 -> najczęściej, 2 -> ostatnie 3 mies, 3 -> najrzadziej
        opt = int(request.args['opt'])
    else:
        return render_template('exercises.html', part="no")

    if opt == 1:
        sql = """select  e.name, e.body_part, e.ide, count(s.id_exercise) as ile 
                    from exercise e inner join series s 
                     on e.ide = s.id_exercise 
                        inner join plan p
                        on p.id_series=s.ids  
               group by e.ide         
                order by ile desc limit 10"""
        tytul ="Ćwiczenia najczęściej wykonywane w planach"

    if opt == 2:
        wynik=three_last()
        print(wynik)
        sql = """select e.name, e.body_part, e.ide, count(s.id_exercise) as ile 
                    from exercise e inner join series s 
                     on e.ide = s.id_exercise 
                        inner join plan p
                        on p.id_series=s.ids  
            where p.data_from >= '""" + str(wynik[0]) +"""' and data_to <= '"""+ str(wynik[1])  + """'
               group by e.ide         
                order by e.body_part"""
        tytul ="Ćwiczenia wykonywanie w ostatnich trzech miesiącach"

    if opt == 3:
        sql = """select e.name, e.body_part, e.ide, count(s.id_exercise) as ile 
                    from exercise e inner join series s 
                     on e.ide = s.id_exercise 
                        inner join plan p
                        on p.id_series=s.ids   
               group by e.ide         
                order by ile limit 15"""

        tytul ="Najrzadziej wykonywane ćwiczenia"

    if opt ==4:
        sql = """select e.name, e.body_part, e.ide, count(s.id_exercise) as ile 
                    from exercise e left join series s 
                     on e.ide = s.id_exercise 
                        left join plan p
                        on p.id_series=s.ids  
                where p.id_series is null and s.id_exercise is null
               group by e.ide """
        tytul = "ćwiczenia, które są w bazie a nigdy nie były wykorzystane w planach"

    if opt < 1 or opt > 4:  # przypadek, gdy argument jest ale ma złą wartość
        return render_template('exercises.html', part="no")

    mycursor.execute(sql)
    wynik = mycursor.fetchall()
    print(wynik)

    return render_template('statistic.html', wynik=wynik, tutul=tytul)


@app.route("/panel")
@login_required
def panel():
    user = current_user.username
    return render_template('panel.html', user=user)


@app.route("/formularz", methods=["GET", "POST"])
def formularz():
    return render_template('formularz.html')


@app.route("/addex", methods=["GET", "POST"])
@login_required
def addex():
    forme = ExerciseForm()
    if request.method == 'POST':
        name = str(forme.name.data)
        description = str(forme.description.data)
        body_part = str(forme.body_part.data)
        print(name)
        print(description)
        print(body_part)
        if (name != ""):
            add_exercise(name, description, body_part, mydb)
            return render_template('dodane.html')
    return render_template('error.html')


@app.route("/editex", methods=["GET", "POST"])
@login_required
def editex():
    forme = ExerciseForm()
    if request.method == 'POST':
        id = str(forme.id.data)
        name = str(forme.name.data)
        description = str(forme.description.data)
        body_part = str(forme.body_part.data)
        print(name)
        print(description)
        print(body_part)
        if (name != ""):
            update_exercise(id, name, description, body_part, mydb)
            return render_template('dodane.html')
    return render_template('editexercise.html')


@app.route("/addse", methods=["GET", "POST"])
@login_required
def addse():
    forms = SeriesForm()
    if request.method == 'POST':
        exercise = int(forms.exercise.data)
        number_sets = str(forms.number_sets.data)
        number_repeats = str(forms.number_repeats.data)
        weight = str(forms.weight.data)
        if (forms.superseries.data==True):
            super="1"
        else:
            super="0"
        set = str(forms.set.data)
        if (number_sets != "" and number_repeats != ""):
            add_series(exercise, number_sets, number_repeats, weight, super, set, mydb)

    return render_template('dodane.html')


@app.route("/editse", methods=["GET", "POST"])
@login_required
def editse():
    forms = SeriesForm()
    form = SearchForm()
    if request.method == 'POST':
        exercise = int(forms.exercise.data)
        number_sets = str(forms.number_sets.data)
        number_repeats = str(forms.number_repeats.data)
        weight = str(forms.weight.data)
        superseries = str(forms.superseries.data)
        set = str(forms.set.data)
        if (number_sets != "" and number_repeats != ""):
            add_series(exercise, number_sets, number_repeats, weight, superseries, set, mydb)
        # sql="select ids,name from exercise where name="+exercise
        # wynik = pokaz_ex(sql)
        # ide=int(wynik[0])
        print(exercise)
        print(number_sets)
        print(number_repeats)
        print(weight)
        print(superseries)

        # if (exercise!=""):
        #     add_series(name, description, mydb)
        #     return render_template('index.html', form=form, message="ćwiczenie zostało dodane")
    return render_template('index.html', form=form)


@app.route("/addexercise", methods=["GET", "POST"])
@login_required
def addexercise():
    forme = ExerciseForm()
    return render_template('addexercise.html', form=forme)


@app.route("/editexercise", methods=["GET", "POST"])
@login_required
def editexercise():
    flag=0
    if (request.method == 'POST'):
        print()
        forme=ChoiseForm()
        form = ExerciseForm()
       # id = request.args['id']
        id= forme.choise.data
        print(id)
        sql = "select * from exercise where ide=" + id
        mycursor.execute(sql)
        wynik = mycursor.fetchall()
        print(wynik)
        form.id.data=wynik[0][0]
        form.name.data = wynik[0][1]
        form.description.data = wynik[0][2]
        form.body_part.data = wynik[0][3]
    else:
        form = ChoiseForm()
        sql = "select ide, name from exercise order by name"
        wynik = pokaz_ex(sql)
        form.choise.choices = [(ex[0], ex[1]) for ex in wynik]
        flag=1
    return render_template('editexercise.html', form=form, flag=flag)


@app.route("/addseries", methods=["GET", "POST"])
@login_required
def addseries():
    sql = "select ide, name from exercise order by name"
    wynik = pokaz_ex(sql)
    forms = SeriesForm()
    forms.exercise.choices = [(ex[0], ex[1]) for ex in wynik]
    return render_template('addseries.html', form=forms)


@app.route("/editseries", methods=["GET", "POST"])
@login_required
def editseries():
    sql = "select ide, name from exercise order by name"
    wynik = pokaz_ex(sql)
    forms = SeriesForm()
    forms.exercise.choices = [(ex[0], ex[1]) for ex in wynik]
    return render_template('editseries.html', form=forms)


@app.route("/addplan", methods=["GET", "POST"])
@login_required
def addplan():

    sql = "select * from exercise e inner join series s on e.ide = s.id_exercise order by name"
    wynik = pokaz_pl(sql)
    print(wynik)
    formp = PlanForm()
    formp.series.choices = [(se[0],se[1]) for se in wynik]
    # sql="select * from exercise where body_part='" + part + "' order by name"
    return render_template('addplan.html', form=formp)

@app.route("/addpl", methods=["GET", "POST"])
@login_required
def addpl():
    form = PlanForm()
    forms = SeriesForm()
    if request.method == 'POST':
        date_from = form.time_from.data
        date_to = form.time_to.data
        day = int(form.day.data)
        order = int(form.order.data)
        # number_repeats = str(forms.number_repeats.data)
        # weight = str(forms.weight.data)
        # superseries = str(forms.superseries.data)
        # set = str(forms.set.data)
        # if (number_sets != "" and number_repeats != ""):
        #     add_series(exercise, number_sets, number_repeats, weight, superseries, set, mydb)
        # sql="select ids,name from exercise where name="+exercise
        # wynik = pokaz_ex(sql)
        # ide=int(wynik[0])
        print(exercise)

    return render_template('addplan.html', form=form)

@app.route("/editplan", methods=["GET", "POST"])
@login_required
def editplan():
    forme = ExerciseForm()
    return render_template('editplan.html', form=forme)


if __name__ == '__main__':
    app.run(debug=True)
