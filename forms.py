from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField, SubmitField, FileField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileRequired, FileAllowed


class ReqOrseeForm(FlaskForm):
    expename = StringField(
        "Nom court de l'expérience", validators=[DataRequired(), Length(min=2, max=20)]
    )
    date = DateField("Date de l'expérience (format jj/mm/yyyy)", format="%d/%m/%Y")
    time = TimeField("Heure de l'expérience (format hh:mm:ss)", format="%H:%M:%S")
    submit = SubmitField("Valider")


class UploadParticipantsForm(FlaskForm):
    input_file = FileField(
        '',
        validators=[
            FileAllowed(['csv'], message="Fichier csv requis"),
            FileRequired()
        ]
    )
    submit = SubmitField("Créer les bordereaux")

