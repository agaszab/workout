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