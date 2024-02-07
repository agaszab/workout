from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, DateField, PasswordField, SubmitField, validators, TextAreaField, HiddenField, BooleanField
from wtforms.validators import DataRequired, Length, ValidationError, InputRequired
# from main import User



class SearchForm(FlaskForm):
    # miesiac2 = StringField('Miesiac')
    # ilosc = IntegerField('Ile miesiecy')
    # miesiac = SelectField('Miesiac',
    #                       choices=["Styczen", "Luty", "Marzec", "Kwiecien", "Maj", "Czerwiec", "Lipiec", "Sierpień",
    #                                "Wrzesień", "Październik", "Listopad", "Grudzień"])
    # rok = SelectField('Miesiac', choices=["2022", "2023"])
    startdate = DateField('Pokaż plan treningowy na dzień : ', format='%Y-%m-%d', validators=(validators.DataRequired(),))
    # stopdate = DateField('Do: ', format='%Y-%m-%d', validators=(validators.DataRequired(),))
    submit = SubmitField("Pokaż", render_kw={'class': "btn btn-dark"})


class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Register', render_kw={'class': "btn btn-dark"})

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError('That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login', render_kw={'class': "btn btn-dark"})



class ExerciseForm(FlaskForm):
    id = HiddenField('Id')
    name = StringField('Nazwa ćwiczenia', validators=[validators.DataRequired()], )
    description = TextAreaField('Opis ćwiczenia', validators=[validators.optional()])
    body_part = SelectField('Partia mięśni', choices=["klatka", "plecy", "triceps", "biceps", "barki", "brzuch", "nogi"])
    submit = SubmitField("Wstaw", render_kw={'class': "btn btn-dark"})

class SeriesForm(FlaskForm):
    # choices=[]
    # for item in list:
    #     choices.append(item[1])
    id = HiddenField('Id')
    exercise = SelectField('Ćwiczenie', validators=[DataRequired()])
    number_sets = IntegerField('Ile serii')
    number_repeats = StringField('Ilość powtórzeń')
    weight = StringField('Obciążenie')
    superseries = BooleanField('superseria')
    set = IntegerField('Numer superserii',  default=0)
    submit = SubmitField("Wstaw", render_kw={'class': "btn btn-dark"})
    submit_wybierz = SubmitField("Wybierz", render_kw={'class': "btn btn-dark"})
    submit_zapisz = SubmitField("Zapisz", render_kw={'class': "btn btn-dark"})
class PlanForm(FlaskForm):

    body_part = SelectField('Partia mięśni',
                            choices=["klatka", "plecy", "triceps", "biceps", "barki", "brzuch", "nogi"])
    exercise = SelectField(u'Ćwiczenie', validators=[DataRequired()])
    series = SelectField(u'Seria', validators=[DataRequired()], id="series")
    time_from = DateField('Data rozpoczęcia: ', format='%Y-%m-%d', validators=(validators.DataRequired(),))
    time_to = DateField('Data zakończenia : ', format='%Y-%m-%d', validators=(validators.DataRequired(),))
    day = SelectField('Dzień treningowy', choices=["1- barki i brzuch", "2- plecy, triceps i biceps", "3 - klatka i brzuch", "4 - nogi"])
    order = IntegerField('Kolejność ćwiczeń danego dnia')
    submit = SubmitField("Wstaw", render_kw={'class': "btn btn-dark"})

class ChoiseForm(FlaskForm):
    choise = SelectField(u'Wybierz dane do edycji', validators=[DataRequired()])
    submit = SubmitField("Wybierz", render_kw={'class': "btn btn-dark"})