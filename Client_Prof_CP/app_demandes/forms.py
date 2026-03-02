from tkinter import Listbox

from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, SelectMultipleField
from wtforms.validators import DataRequired, Email,Regexp, Length


class NouveauProfForm(FlaskForm):
    nom = StringField(
        "Nom",
        validators=[
            DataRequired(message="Le nom est obligatoire"),
            Length(min=2, message="Le nom est trop court")
        ]
    )

    prenom = StringField(
        "Prénom",
        validators=[
            DataRequired(message="Le prénom est obligatoire")
        ]
    )

    courriel = StringField(
        "Courriel professionnel",
        validators=[
            DataRequired(message="Le courriel est obligatoire"),
            Email(message="Email invalide")
        ]
    )

    ecoles = SelectMultipleField(
        "Écoles enseignées",
        choices=[],
        validators=[DataRequired(message="Choisir au moins une école")]
    )

    codesMatieres = SelectMultipleField(
        "Matières enseignées",
        choices=[],
        validators=[DataRequired(message="Choisir au moins une matière")]
    )

    password = PasswordField(
        "Mot de passe",
        validators=[
            DataRequired(message="Le mot de passe est obligatoire"),
            Regexp(
                r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*\W).{8,}$",
                message="Mot de passe doit contenir majuscule, minuscule, chiffre, caractère spécial et faire au moins 8 caractères"
            )
        ]
    )
    submit = SubmitField("Sauvegarder")

class NouveauConseillerForm(FlaskForm):
    nom = StringField(
        "Nom",
        validators=[
            DataRequired(message="Le nom est obligatoire"),
            Length(min=2, message="Le nom est trop court")
        ]
    )

    prenom = StringField(
        "Prénom",
        validators=[
            DataRequired(message="Le prénom est obligatoire")
        ]
    )

    courriel = StringField(
        "Courriel professionnel",
        validators=[
            DataRequired(message="Le courriel est obligatoire"),
            Email(message="Email invalide")
        ]
    )
    tel = StringField("Téléphone professionnel:", validators=[DataRequired()])

    codesMatieres = SelectMultipleField(
        "Matières supervisées",
        choices=[],
        validators=[DataRequired(message="Choisir au moins une matière")]
    )

    password = PasswordField(
        "Mot de passe",
        validators=[
            DataRequired(message="Le mot de passe est obligatoire"),
            Regexp(
                r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*\W).{8,}$",
                message="Doit contenir majuscule, minuscule, chiffre, caractère spécial et faire au moins 8 caractères"
            )
        ]
    )
    submit = SubmitField("Sauvegarder")

class LoginForm(FlaskForm):
    courriel = StringField("Courriel",validators=[DataRequired(), Email()])
    password = PasswordField("Mot de passe",validators=[DataRequired()])
    submit = SubmitField("Se connecter")