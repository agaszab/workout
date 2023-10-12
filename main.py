import binascii
import hashlib

import mysql.connector
from flask import Flask, render_template, request, url_for, session, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, DateField, SubmitField, validators, TextAreaField, \
    RadioField  # bo nasz formularz wtf będzie miał pola string
from wtforms.validators import DataRequired

mydb = mysql.connector.connect(user='root', password='kociakolka', host='127.0.0.1', database='workout')
mycursor = mydb.cursor()
app = Flask(__name__)  # __name__ oznacza, że jest to ta strona jest do zarządzania, tworzymy instancję klasy flaskowej
app.config['SECRET_KEY'] = 'AComplicat3dTest.'



class SearchForm(FlaskForm):
    miesiac2 = StringField('Miesiac')
    ilosc = IntegerField('Ile miesiecy')
    miesiac = SelectField('Miesiac',
                          choices=["Styczen", "Luty", "Marzec", "Kwiecien", "Maj", "Czerwiec", "Lipiec", "Sierpień",
                                   "Wrzesień", "Październik", "Listopad", "Grudzień"])
    rok = SelectField('Miesiac', choices=["2022", "2023"])
    startdate = DateField('Od: ', format='%Y-%m-%d', validators=(validators.DataRequired(),))
    stopdate = DateField('Do: ', format='%Y-%m-%d', validators=(validators.DataRequired(),))
    submit = SubmitField("Pokaż")

class ExerciseForm(FlaskForm):

    name = StringField('Nazwa ćwiczenia', validators=[validators.DataRequired()])
    description = TextAreaField('Opis ćwiczenia', validators=[validators.optional()])
    body_part = SelectField('Partia mięśni', choices=["klatka", "plecy", "triceps", "biceps", "barki", "brzuch", "nogi"])
    submit = SubmitField("Wstaw")

class SeriesForm(FlaskForm):
    # choices=[]
    # for item in list:
    #     choices.append(item[1])
    exercise = SelectField(u'Ćwiczenie', validators=[DataRequired()])
    number_sets = IntegerField('Ile serii')
    number_repeats = StringField('Ilość powtórzeń')
    weight = StringField('Obciążenie')
    superseries = RadioField('Superseria', choices=[(0, 'nie'), (1, 'tak')], default=0)
    set = IntegerField('Numer superserii',  default=0)
    submit = SubmitField("Wstaw")


def verify_password(self, stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

def login_user(self):
    sql="select idu, login, pass from users where login=?"
    mycursor.execute(sql)
    myresult = mycursor.fetchone()

    if myresult != None and self.verify_password(myresult['pass'], self.password):
        return  myresult
    else:
        self.user = None
        self.password = None
        return None

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
    sql = "SELECT plan.data_from, plan.data_to, plan.day, exercise.body_part, exercise.name, exercise.description, series.number_sets, series.number_repeats, series.weight, series.superseries, series.set FROM plan, series, exercise where data_from BETWEEN '"+start+"' AND '"+stop+"' and plan.id_series = series.ids and series.id_exercise = ide"
    # sql= "SELECT kurs_pl, any_value('id', 'kurs_usd, data, godzina') FROM kursy where data BETWEEN '"+start+"' AND '"+stop+"' "
    # print(sql)
    list = pokaz_trening(sql)
    return list

def pokaz(sql):
  mycursor.execute(sql)
  myresult = mycursor.fetchall()
  print(myresult)
  cwiczenia=[]
  for x in myresult:
    cwiczenie=[x[0],x[1],x[2],x[3]]
    cwiczenia.append(cwiczenie)
    # print(str(x[0])+" USD, ",str(x[1])+" PL, -> ",x[2],x[3],x[4])
    # print(myresult)
  print(cwiczenia)
  return cwiczenia

def pokaz_plan2(day, data_from):
    print("_6_")
    data = str(data_from)
    print("_7_")
    # sql_pom = "select plan.data_from, plan.data_to, plan.day, exercise.name, exercise.description, exercise.body_part, series.number_sets, series.number_repeats, series.weight, series.superseries, series.set, plan.order from exercise inner join series on exercise.ide = series.id_exercise inner join plan on series.ids = plan.id_series and plan.data_from = '" + data + "' and plan.day=" + day + "  order by plan.order"
    sql_pom = """
                select p.data_from, p.data_to, p.day, e.name, e.description, e.body_part, s.number_sets, s.number_repeats, s.weight, s.superseries, s.set, p.order 
                    from exercise e inner join series s 
                    on e.ide = s.id_exercise 
                        inner join plan p
                        on p.id_series=s.ids  
                    where p.data_from =  '"""+data+"""' and p.day="""+day+"""  order by p.order
              """
    print(sql_pom)
    print("_8_")
    mycursor.execute(sql_pom)
    myresult_pom = mycursor.fetchall()
    print(myresult_pom)
    body_part = myresult_pom[0][5]
    plan1 = []
    plan2 = []
    for x in myresult_pom:
        if x[5] == body_part:
            plan_1 = [x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9], x[10], x[11]]
            plan1.append(plan_1)
        else:
            plan_2 = [x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9], x[10], x[11]]
            plan2.append(plan_2)
    print(plan1)
    print("++++++++++++++++++++++++++++")
    print(plan2)
    print("++++++++++++++++++++++++++++")
    return plan1, plan2
def pokaz_plan(day):
    mycursor.execute("select data_from from plan order by data_from desc limit 1")
    myresult = mycursor.fetchall()
    data = str(myresult[0][0])
    print(data)
    print(day)
    sql_pom = """
                select p.data_from, p.data_to, p.day, e.name, e.description, e.body_part, s.number_sets, s.number_repeats, s.weight, s.superseries, s.set, p.order 
                    from exercise e inner join series s 
                    on e.ide = s.id_exercise 
                        inner join plan p
                        on p.id_series=s.ids  
                    where p.data_from =  '"""+data+"""' and p.day="""+day+"""  order by p.order
              """
    print(sql_pom)
    mycursor.execute(sql_pom)
    myresult_pom = mycursor.fetchall()
    print(myresult_pom)
    body_part=myresult_pom[0][5]
    plan1=[]
    plan2=[]
    for x in myresult_pom:
        if x[5]==body_part:
            plan_1=[x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9],x[10],x[11]]
            plan1.append(plan_1)
        else:
            plan_2=[x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9],x[10],x[11]]
            plan2.append(plan_2)
    print(plan1)
    print("++++++++++++++++++++++++++++")
    print(plan2)
    print("++++++++++++++++++++++++++++")
    return plan1, plan2
def pokaz_ex(sql):
  mycursor.execute(sql)
  myresult = mycursor.fetchall()
  print(myresult)
  cwiczenia=[]
  for x in myresult:
    cwiczenie=[x[0],x[1]]
    cwiczenia.append(cwiczenie)
  return cwiczenia

def pokaz_trening(sql):
  mycursor.execute(sql)
  myresult = mycursor.fetchall()
  print(myresult)
  trening=[]
  for x in myresult:
      trening.append(x)
  return trening

def add_exercise(name, description , body_part, mydb):
    print(name)
    print(description)
    print(body_part)
    sql=f"INSERT INTO exercise(name, description, body_part) VALUES ('"+name+"','"+description+"','"+body_part+"')"
    cursor = mydb.cursor()
    cursor.execute(sql)
    mydb.commit()

def add_series(id_exercise, number_sets, rumber_repeats, weight, superseries, set, mydb):
    id=str(id_exercise)
    # set_s=str(set)
    # nb=str(number_sets)
    sql="INSERT INTO series(id_exercise, number_sets, number_repeats, weight, superseries, set) VALUES ("+id+","+number_sets+",'"+rumber_repeats+"','"+weight+"','"+superseries+"',"+set+")"
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
    if myresult==[]:
        kiedy="nigdy nie wystąpiło w planach"
    else:
        kiedy_start = myresult[0][0]
        kiedy_stop = myresult[0][1]
        kiedy = "od: "+str(kiedy_start)+" do: " + str(kiedy_stop)
    return kiedy

def ile_razy_cwiczenie(id):
    sql = """
    select count(*) as ile from exercise e inner join series s 
        	    on e.ide = s.id_exercise 
                where e.ide="""+str(id)+" group by e.ide"

    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    if myresult==[]:
        ile_razy=0
    else:
        ile_razy = myresult[0][0]
    return ile_razy

def wykaz_serii(id):
    sql="SELECT * FROM series s inner join plan p on s.ids=p.id_series where s.id_exercise="+str(id)+" order by data_from"
    mycursor.execute(sql)
    wynik = mycursor.fetchall()
    return wynik



@app.route('/', methods=['GET','POST'])
def index():
    form = SearchForm()
                        # sql = "select * from exercise order by body_part"
                        # wynik = pokaz(sql)
                        # list = pokaz("SELECT * FROM kursy")
                        # print(list)
                        # return render_template('index.html')
                    # return render_template('index.html', form=form, wynik=wynik)
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        user = request.form["nick"]
        session["user"] = user
        return redirect(url_for("test"))
    else:
        return render_template("login.html"
                               )
    return render_template('logowanie.html')


@app.route('/validateLogin',methods=['POST'])
def validateLogin():

    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']

        sql="select * from users"
        mycursor.execute(sql)
        data = mycursor.fetchall()

        if len(data) > 0:
            if check_password_hash(str(data[0][3]), _password):
                return redirect('/userHome')
            else:
                return render_template('error.html', error='Wrong Email address or Password.')
        else:
            return render_template('error.html', error='Wrong Email address or Password.')

    except Exception as e:
        return render_template('error.html',error = str(e))

@app.route('/userHome')
def userHome():
    return render_template('userHome.html')

@app.route('/subpage', methods=['GET','POST'])
def subpage():
    form = SearchForm()
    sql = "select * from exercise order by body_part"
    wynik = pokaz(sql)
    # list = pokaz("SELECT * FROM kursy")
    # print(list)
    # return render_template('index.html')
    return render_template('subpage.html', form=form, wynik=wynik)

@app.route('/exercise', methods=['GET','POST'])
def exercise():
    id=request.args['id']
    sql = "select * from exercise where ide="+id
    mycursor.execute(sql)
    wynik = mycursor.fetchall()
    print(wynik)
    ile_razy = ile_razy_cwiczenie(wynik[0][0])
    print(ile_razy)
    kiedy = kiedy_cwiczenie(wynik[0][0])
    print(kiedy)
    serie=wykaz_serii(wynik[0][0])
    print(serie)
    return render_template('exercise.html', wynik=wynik, ile_razy=ile_razy, kiedy=kiedy, serie=serie)



@app.route('/exercises', methods=['GET','POST'])
def exercises():
    print(request.args['part'])

    if request.args['part'] and request.args['part'] != "no":     # jeśli jest party=no to znaczy, że link przyszedł bezpośrednio z menu bocznego 'wykaz ćwiczen'
        part = request.args['part']
        if request.args['part'] != "all":
            sql="select * from exercise where body_part='"+part+"' order by name"
        else:
            sql = "select * from exercise order by body_part"
        mycursor.execute(sql)
        wynik = mycursor.fetchall()
        print(wynik)
    else:
        wynik = []
        part=""

    wynik_caly = []
    if wynik != []:

        for elem in wynik:
            ile_razy=ile_razy_cwiczenie(elem[0])
            print(ile_razy)
            kiedy=kiedy_cwiczenie(elem[0])
            print(kiedy)
            pom=[elem, ile_razy, kiedy]
            wynik_caly.append(pom)
    print(wynik_caly)
    print(part)
    return render_template('exercices.html', wynik=wynik_caly, part=part)



@app.route("/plan", methods=["GET", "POST"])
def plan():

    if request.args['day']:  # domyslnie pierwszy dzień treningowy, w sumie są cztery
        day=request.args['day']
    else:
        day=1

    # if request.args['data_from'] == 0:     # jeśli idzie z listy planów to jest konkretna data, jeśli z menu bocznego to brak i wtedy domyślnie ma być aktualna data
    #     wynik = pokaz_plan(day)
    # else:
    #     data_from = request.args['data_from']
    #     wynik = pokaz_plan2(day, data_from)

    wynik = pokaz_plan(day)


    if (len(wynik[1])==0):   # sprawdzanie czy plan jest na dwie partie czy na jedną np tylko nogi, dla pom=0 nie jest wyświedlana druga kolumna na stronie
        pom=0
    else:
        pom=1
    return render_template('plan.html', day=day, wynik=wynik, pom=pom)

@app.route("/plan2", methods=["GET", "POST"])
def plan2():

    if request.args['day']:  # domyslnie pierwszy dzień treningowy, w sumie są cztery
        day=request.args['day']
    else:
        day=1

    data_from = request.args['data_from']

    wynik = pokaz_plan2(day, data_from)

    if (len(wynik[1])==0):   # sprawdzanie czy plan jest na dwie partie czy na jedną np tylko nogi, dla pom=0 nie jest wyświedlana druga kolumna na stronie
        pom=0
    else:
        pom=1
    return render_template('plan.html', day=day, wynik=wynik, pom=pom)

@app.route("/plans", methods=["GET", "POST"])
def plans():
    sql="select distinct data_from, data_to from plan order by data_from"
    wynik=pokaz_plany(sql)
    form = SearchForm()
    # if request.method == 'POST':
    #     startdate = str(form.startdate.data)
    #     stopdate = str(form.stopdate.data)
    #     list = pokaz_zakres2(start=startdate, stop=stopdate)
    #     if (list==[]):
    #         return render_template('index.html', form=form, message="Nie ma danych dla tego zakresu dat")
    #     else:
    #         # return redirect(url_for('index', page='pokaz_zakres.txt', form=form))
    #         return render_template('trening.html', form=form, list=list)
    # # return render_template('index.html', form=form, list=list)
    return render_template('plans.html', form=form, wynik=wynik)

@app.route("/formularz", methods=["GET", "POST"])
def formularz():

    return render_template('formularz.html')


@app.route("/addex", methods=["GET", "POST"])
def addex():
    forme = ExerciseForm()
    form = SearchForm()
    if request.method == 'POST':
        name = str(forme.name.data)
        description = str(forme.description.data)
        body_part = str(forme.body_part.data)
        print(name)
        print(description)
        print(body_part)
        if (name!=""):
            add_exercise(name, description, body_part, mydb)
            return render_template('index.html', form=form, message="ćwiczenie zostało dodane")
    return render_template('subpage.html', form=form)

@app.route("/addse", methods=["GET", "POST"])
def addse():
    forms = SeriesForm()
    form = SearchForm()
    if request.method == 'POST':
        exercise= int(forms.exercise.data)
        number_sets= str(forms.number_sets.data)
        number_repeats= str(forms.number_repeats.data)
        weight= str(forms.weight.data)
        superseries= str(forms.superseries.data)
        set=str(forms.set.data)
        if (number_sets != "" and number_repeats!=""):
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
def addexercise():
    forme = ExerciseForm()
    return render_template('addexercise.html', form=forme)


@app.route("/addseries", methods=["GET", "POST"])
def addseries():
    sql="select ide, name from exercise order by name"
    wynik=pokaz_ex(sql)
    forms = SeriesForm()
    forms.exercise.choices = [(ex[0], ex[1]) for ex in wynik]
    return render_template('addseries.html', form=forms)


@app.route("/addplan", methods=["GET", "POST"])
def addplan():
    forme = ExerciseForm()
    return render_template('addplan.html', form=forme)


if __name__ == '__main__':
    app.run()
