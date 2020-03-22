import json

import pandas as pd
from flask import render_template, url_for, redirect, session

from le2mBordereaux import app, requetes
from le2mBordereaux.forms import ReqOrseeForm, UploadParticipantsForm, BordereauxViergesForm
from . import config


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", title="Home")


@app.route("/req_orsee", methods=['GET', 'POST'])
def req_orsee():
    form = ReqOrseeForm()
    if form.validate_on_submit():
        req_infos = dict(
            expe=form.expename.data, date=form.date.data, heure=form.time.data
        )
        session["req_infos"] = dict(
            # passage en strftime pour sérialisation json. Stocké pour liste_participants, bordereaux
            expe=form.expename.data, date=form.date.data.strftime("%d/%m/%Y"), heure=form.time.data.strftime("%H:%M")
        )
        session["req"] = json.dumps(
            requetes.get_requete_participants(**req_infos))  # pour orsee_result
        return redirect(url_for("req_orsee_result"))
    return render_template("req_orsee.html", title="Requete ORSEE", form=form)


@app.route("/req_orsee_result", methods=['GET', 'POST'])
def req_orsee_result():
    return render_template("req_orsee_result.html", requete=json.loads(session["req"]))


@app.route("/liste_participants", methods=["GET", "POST"])
def liste_participants():
    form = UploadParticipantsForm()
    participants = []
    if form.validate_on_submit():
        input_file = form.input_file.data
        df = pd.read_csv(input_file, names=["uid", "genre", "nom", "prenom", "mail", "deb_etudes", "etudes"])
        df.genre = df.genre.apply(str.upper)
        df.nom = df.nom.apply(str.upper)
        df.prenom = df.prenom.apply(str.capitalize)
        participants = df.to_dict("records")
        session["participants"] = participants  # pour bordereaux
    return render_template(
        "liste_participants.html",
        title="Participants", form=form, req_infos=session.get("req_infos", None), participants=participants
    )


@app.route("/bordereaux")
def bordereaux():
    return render_template("bordereaux.html", title="Bordereaux", req_infos=session.get("req_infos", None),
                           participants=session.get("participants", None), ville=config.VILLE, souche_deb=0)


@app.route("/bordereaux_vierges", methods=["GET", "POST"])
def bordereaux_vierges():
    form = BordereauxViergesForm()
    if form.validate_on_submit():
        nb_vierges = form.nombre.data
        vierges = [dict(nom="", prenom="") for _ in range(nb_vierges)]
        return render_template("bordereaux.html", title="Bordereaux", req_infos=session.get("req_infos", None),
                               participants=vierges, ville=config.VILLE, souche_deb=form.souche_deb.data - 1)
    return render_template("bordereaux_vierges.html", form=form, title="Bordereaux",
                           req_infos=session.get("req_infos", None))


@app.route("/about")
def about():
    return render_template("about.html", title="About")
