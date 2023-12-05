from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, DateField, PasswordField, SubmitField, validators, TextAreaField, RadioField
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
    submit = SubmitField("Pokaż")


class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError('That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')


# class ExerciseForm(FlaskForm):
#
#     name = StringField('Nazwa ćwiczenia', validators=[validators.DataRequired()])
#     description = TextAreaField('Opis ćwiczenia', validators=[validators.optional()])
#     submit = SubmitField("Wstaw")


# class SeriesForm(FlaskForm):
#     # choices=[]
#     # for item in list:
#     #     choices.append(item[1])
#     exercise = SelectField(u'Ćwiczenie', validators=[DataRequired()])
#     number_sets = IntegerField('Ile serii')
#     number_repeats = StringField('Ilość powtórzeń')
#     weight = StringField('Obciążenie')
#     superseries = RadioField('Superseria', choices=[(0, 'nie'), (1, 'tak')], default=0)
#     set = IntegerField('Numer superserii',  default=0)
#     submit = SubmitField("Wstaw")


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

class PlanForm(FlaskForm):

    series = SelectField(u'Seria', validators=[DataRequired()])
    period = StringField('Ilość powtórzeń')
    weight = StringField('Obciążenie')
    superseries = RadioField('Superseria', choices=[(0, 'nie'), (1, 'tak')], default=0)
    set = IntegerField('Numer superserii',  default=0)
    submit = SubmitField("Wstaw")

