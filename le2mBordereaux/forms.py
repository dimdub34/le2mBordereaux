from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import IntegerField, StringField, DateField, TimeField, SubmitField, FileField
from wtforms.validators import DataRequired, Length, NumberRange


class ReqOrseeForm(FlaskForm):
    expename = StringField(
        "Nom court de l'expérience", validators=[DataRequired(), Length(min=2, max=20)]
    )
    date = DateField("Date de l'expérience (format jj/mm/yyyy)", format="%d/%m/%Y")
    time = TimeField("Heure de l'expérience (format hh:mm)", format="%H:%M")
    submit = SubmitField("Valider")


class UploadParticipantsForm(FlaskForm):
    input_file = FileField(
        '',
        validators=[
            FileAllowed(['csv'], message="Fichier csv requis"),
            FileRequired()
        ]
    )
    submit = SubmitField("Afficher la liste des participants")


class BordereauxViergesForm(FlaskForm):
    nombre = IntegerField(label="Nombre de bordereaux à créer", validators=[DataRequired(), NumberRange(min=1, max=100)])
    souche_deb = IntegerField(label="Numéro de la première souche", validators=[DataRequired(), NumberRange(min=1, max=100)])
    submit = SubmitField("Valider")


class BordereauxCreateCompta(FlaskForm):
    submit = SubmitField("Créer le fichier de compta")