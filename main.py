import json

import pandas as pd
from flask import Flask, render_template, url_for, redirect, session

import config
import requetes
from forms import ReqOrseeForm, UploadParticipantsForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '169944cb18b918a084db8f6d24df1240'


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
            expe=form.expename.data, date=form.date.data.strftime("%d-%m-%Y"), heure=form.time.data.strftime("%H:%M:%S")
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
        df = pd.read_csv(input_file, names=["Nom", "Prenom"])
        df.Nom = df.applymap(str.upper)
        df.Prenom = df.applymap(str.capitalize)
        participants = df.values.tolist()
        session["participants"] = participants  # pour bordereaux
        return render_template("bordereaux.html", participants=session["participants"], ville=config.VILLE,
                           req_infos=session["req_infos"])
    return render_template(
        "liste_participants.html",
        form=form, req_infos=session.get("req_infos", None), participants=participants
    )

# @app.route("/bordereaux")
# def bordereaux():
#     nb_participants = len(session["participants"])
#     nb_pages, restant = divmod(nb_participants, 4)
#     if restant:
#         nb_pages += 1
#     return render_template("bordereaux.html", participants=session["participants"], ville=config.VILLE,
#                            req_infos=session["req_infos"])
#

@app.route("/about")
def about():
    return render_template("about.html", title="About")


if __name__ == "__main__":
    app.run(debug=True)
