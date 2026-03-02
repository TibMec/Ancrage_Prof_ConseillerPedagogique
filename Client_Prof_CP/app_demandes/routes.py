from flask import Flask, render_template
from werkzeug.utils import redirect

from app_demandes.forms import NouveauProfForm, NouveauConseillerForm, LoginForm
from app_demandes.config import Config
from flask import flash, session
import requests

app = Flask(__name__)
app.config.from_object(Config)

codes = [
        ("634-106", "Francais Langue Seconde Base SEC1"),
        ("634-206", "Francais Langue Seconde Base SEC2"),
        ("634-306", "Francais Langue Seconde Base SEC3"),
        ("634-404", "Francais Langue Seconde Base SEC4"),
        ("634-504", "Francais Langue Seconde Base SEC5"),
        ("635-106", "Francais Langue Seconde Enrichi SEC1"),
        ("635-206", "Francais Langue Seconde Enrichi SEC2"),
        ("635-306", "Francais Langue Seconde Enrichi SEC3"),
        ("635-406", "Francais Langue Seconde Enrichi SEC4"),
        ("635-506", "Francais Langue Seconde Enrichi SEC5"),
        ("333-333", "MAT201 - Math avancées"),
        ("444-444", "PHY100 - Physique")
    ]

def api_headers():
    token = session.get("token")
    return {
        "Authorization": f"Bearer {token}"
    }

@app.route('/')
@app.route('/index')
def index():
        club = {'titre': 'Ancrage enseignant - conseiller pédagogique'}
        return render_template('index.html', title='Accueil', mod=club)

# ROUTES PROFIL PROF ===================================================
@app.route('/accueil-prof')
def accueil_prof():
    return render_template('vue_accueil_prof.html',
                           title='Profil enseignant',)

@app.route('/profil-prof')
def profil_prof():
    if "role" not in session:
        return redirect("/login-prof")

    if session["role"] != "prof":
        return "Accès refusé", 403
    return render_template('vue_profil_prof.html',
                           title='Profil enseignant',)

@app.route('/nouveau-prof', methods=['GET', 'POST'])
def nouveau_prof():
    prof_form = NouveauProfForm()

    prof_form.ecoles.choices = [
        ("LBP HS", "Lester B Pearson High School"),
        ("Rosemount", "Rosemount High School"),
        ("LHA JR", "Lauren Hill Academy Junior Campus"),
        ("LHA SR", "Lauren Hill Academy Senior Campus"),
        ("RWA", "Royal West Academy"),
        ("VMC", "Vincent Massey Collegiate")
    ]

    prof_form.codesMatieres.choices = codes

    if prof_form.validate_on_submit():
        data = {
            "nom": prof_form.nom.data,
            "prenom": prof_form.prenom.data,
            "courriel": prof_form.courriel.data,
            "ecoles": prof_form.ecoles.data,
            "codesMatieres": prof_form.codesMatieres.data,
            "password": prof_form.password.data,
        }

        url = "http://127.0.0.1:5700/v1/enseignants"
        reponse = requests.post(url, json=data, headers=api_headers())

        # DEBUG important
        print("STATUS:", reponse.status_code)
        print("REPONSE:", reponse.text)

        if reponse.status_code == 201:
            flash(f"Enseignant ajouté avec succès: {reponse.json()['prof']}")
            return redirect('/index')

        else:
            data_erreur = reponse.json()

            if "Erreur de validation" in data_erreur:
                for err in data_erreur["Erreur de validation"]:
                    flash(err["msg"])

            elif "Erreur" in data_erreur:
                flash(data_erreur["Erreur"])

            else:
                flash("Erreur inconnue")
    print("FORM ERRORS:", prof_form.errors)
    return render_template(
        'nouveau_prof_form.html',
        title='Ajout enseignant',
        form=prof_form
    )

@app.route('/mes-conseillers')
def mes_conseillers():
    if "role" not in session:
        return redirect("/login-prof")
    if session["role"] != "prof":
        return "Accès refusé", 403
    url = f'http://127.0.0.1:5700/v1/conseillers-affilies'
    reponse = requests.get(url, headers=api_headers())

    print("STATUS:", reponse.status_code)
    print("TEXT:", reponse.text)

    data = reponse.json()

    print("data ds route client mes conseillers: ",data)
    print(data["conseillers"])

    return render_template('vue_liste_mes_cp.html', title='Affichage conseillers affiliés', liste_conseillers=data)


# ROUTES PROFIL CONSEILLER ============================================
@app.route('/accueil-cp')
def accueil_cp():
    return render_template('vue_accueil_cp.html',
                           title='Profil conseiller pédagogique',)

@app.route('/profil-cp')
def profil_cp():
    if "role" not in session:
        return redirect("/login-cp")

    if session["role"] != "cp":
        return "Accès refusé", 403
    return render_template('vue_profil_cp.html',
                           title='Profil conseiller pédagogique',)
@app.route('/nouveau-conseiller',methods=['GET','POST'])
def nouveau_conseiller():
    cp_form = NouveauConseillerForm()
    print("email dans session, cote client ",session.get('courriel'))
    cp_form.codesMatieres.choices = codes

    if cp_form.validate_on_submit():
        data = {
            "nom": cp_form.nom.data,
            "prenom": cp_form.prenom.data,
            "courriel": cp_form.courriel.data,
            "tel": cp_form.tel.data,
            "codesMatieres": cp_form.codesMatieres.data,
            "password": cp_form.password.data,
        }
        url = "http://127.0.0.1:5900/v1/conseillers"
        reponse = requests.post(url, json=data, headers=api_headers())

        flash("Conseiller ajouté depuis formulaire")
        return redirect('/index')
    return render_template('nouveau_conseiller_form.html',
                           title='Ajout conseiller', form=cp_form)
@app.route('/maj-conseiller',methods=['GET','POST'])
def maj_conseiller():
    if "role" not in session:
        return redirect("/login-cp")

    if session["role"] != "cp":
        return "Accès refusé", 403

    cp_form = NouveauConseillerForm()

    cp_form.codesMatieres.choices = codes
    courriel = session.get('email')

    print("email dans session, cote client ",session.get('courriel'))
    if cp_form.validate_on_submit():
        data = {
            "nom": cp_form.nom.data,
            "prenom": cp_form.prenom.data,
            "courriel": cp_form.courriel.data,
            "tel": cp_form.tel.data,
            "codesMatieres": cp_form.codesMatieres.data,
            "password": cp_form.password.data,
        }
        url = f"http://127.0.0.1:5900/v1/conseillers/{courriel}"
        reponse = requests.put(url, json=data, headers=api_headers())

        flash("Conseiller modifié")
        return redirect('/index')
    return render_template('nouveau_conseiller_form.html',
                           title='Modifier conseiller', form=cp_form)

@app.route('/liste-enseignants',methods=['GET'])
def liste_enseignants():
    url = f'http://127.0.0.1:5900/v1/enseignants'
    reponse = requests.get(url, headers=api_headers())
    data = reponse.json()
    print(data)
    print(data["professeurs"])

    return render_template('vue_liste_profs.html', title='Affichage profs', liste_profs=data["professeurs"])


# ROUTES AUTHENTIFICATION =========================================
@app.route("/login-prof", methods=["GET", "POST"])
def login_prof():
    form = LoginForm()

    if form.validate_on_submit():
        res = requests.post(
            "http://127.0.0.1:5100/v1/tibinc/login-prof",
            json={
                "courriel": form.courriel.data,
                "password": form.password.data
            }
        )

        try:
            data = res.json()
        except:
            flash("Erreur serveur", "danger")
            return render_template("login_prof_form.html", form=form)

        if res.status_code != 200:
            flash(data.get("erreur", "Connexion impossible"), "danger")
            return render_template("login_prof_form.html", form=form)

        session["token"] = data["token"]
        session["courriel"] = data["courriel"]
        session["role"] = "prof"

        print("token session ds client:", session.get("token"))
        print("courriel session ds client:", session.get("courriel"))
        print("role session ds client:", session.get("role"))

        return redirect("/profil-prof")

    return render_template("login_prof_form.html", form=form)

@app.route("/login-cp", methods=["GET", "POST"])
def login_cp():
    form = LoginForm()

    if form.validate_on_submit():
        res = requests.post(
            "http://127.0.0.1:5100/v1/tibinc/login-cp",
            json={
                "courriel": form.courriel.data,
                "password": form.password.data
            }
        )

        try:
            data = res.json()
        except:
            flash("Erreur serveur", "danger")
            return render_template("login_cp_form.html", form=form)

        if res.status_code != 200:
            flash(data.get("erreur", "Connexion impossible"), "danger")
            return render_template("login_cp_form.html", form=form)

        session["token"] = data["token"]
        session["courriel"] = data["courriel"]
        session["role"] = "cp"

        print("token session ds client:", session.get("token"))
        print("courriel session ds client:", session.get("courriel"))
        print("role session ds client:", session.get("role"))

        return redirect("/profil-cp")

    return render_template("login_cp_form.html", form=form)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")