import json

import pandas as pd
import xlwt  # pour créer fichier excel
from flask import render_template, url_for, redirect, session

from le2mBordereaux import app, requetes
from le2mBordereaux.forms import ReqOrseeForm, UploadParticipantsForm, BordereauxViergesForm, BordereauxCreateCompta
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
            expe=form.expename.data, date=form.date.data.strftime("%d/%m/%Y"), heure=form.time.data.strftime("%H:%M"),
            date_for_file=form.date.data.strftime("%Y%m%d"), heure_for_file=form.time.data.strftime("%Hh%M")
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
    participants = session.get("participants", [])
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


@app.route("/bordereaux", methods=["GET", "POST"])
def bordereaux():
    form = BordereauxCreateCompta()
    compta_cree = False
    if form.validate_on_submit():
        create_xls(session.get("req_infos", None), session.get("participants", None))
        compta_cree = True
    return render_template("bordereaux.html", title="Bordereaux", req_infos=session.get("req_infos", None),
                           participants=session.get("participants", None), ville=config.VILLE, souche_deb=0,
                           form=form, compta_cree=compta_cree)


@app.route("/bordereaux_vierges", methods=["GET", "POST"])
def bordereaux_vierges():
    form = BordereauxViergesForm()
    if form.validate_on_submit():
        nb_vierges = form.nombre.data
        vierges = [dict(nom="", prenom="") for _ in range(nb_vierges)]
        session["participants"] = vierges
        form_bord = BordereauxCreateCompta()
        return render_template("bordereaux.html", title="Bordereaux", req_infos=session.get("req_infos", None),
                               participants=session.get("participants", None), ville=config.VILLE,
                               souche_deb=form.souche_deb.data - 1,
                               form=form_bord)
    return render_template("bordereaux_vierges.html", form=form, title="Bordereaux",
                           req_infos=session.get("req_infos", None))


@app.route("/about")
def about():
    return render_template("about.html", title="About")


def create_xls(infos_session, participants):
    """
    Crée le fichier de compta et le place dans /tmp
    """
    wb = xlwt.Workbook()
    ws = wb.add_sheet("Bordereau")
    ws.write(0, 0, f"Date: {infos_session['date']} -- Heure: {infos_session['heure']}")
    ws.write(1, 0, f"Experience: {infos_session['expe']}")
    header = ["Souche", "Nom", "Prenom", "Gain", "Forfait", "Total"]
    format_header = xlwt.easyxf('font: bold 1;')
    for i in range(6):
        ws.write(3, i, header[i], format_header)
    nombre_a_creer = len(participants)
    format_money = xlwt.easyxf(num_format_str=u'#,##0.00[$\u20ac-1]')
    for i in range(nombre_a_creer):
        numero_bordereau = i + 1
        ws.write(4 + i, 0, numero_bordereau)
        ws.write(4 + i, 1, participants[i]["nom"])
        ws.write(4 + i, 2, participants[i]["prenom"])
        ws.write(4 + i, 3, 0.00, format_money)
        ws.write(4 + i, 4, 6.00, format_money)
        ws.write(4 + i, 5, xlwt.Formula('SUM(D{}:E{})'.format(5 + i, 5 + i)),
                 format_money)
    format_total = xlwt.easyxf("font: bold 1;")
    ws.write(4 + nombre_a_creer, 2, "Total", format_total)
    ws.write(4 + nombre_a_creer + 1, 2, u"Dont")
    ws.write(4 + nombre_a_creer + 2, 2, u"Total forfait 2€", format_total)
    ws.write(4 + nombre_a_creer + 3, 2, u"Total forfait 6€", format_total)
    format_total_money = xlwt.easyxf('font: bold 1;',
                                     num_format_str=u'#,##0.00[$\u20ac-1]')
    ws.write(4 + nombre_a_creer, 3, xlwt.Formula('SUM(D5:D{})'.format(
        4 + nombre_a_creer)), format_total_money)
    ws.write(4 + nombre_a_creer, 4, xlwt.Formula('SUM(E5:E{})'.format(
        4 + nombre_a_creer)), format_total_money)
    ws.write(4 + nombre_a_creer, 5, xlwt.Formula('SUM(F5:F{})'.format(
        4 + nombre_a_creer)), format_total_money)
    ws.write(4 + nombre_a_creer + 2, 4, xlwt.Formula(
        "SUMIF(E5:E{}, 2)".format(4 + nombre_a_creer)), format_total_money)
    ws.write(4 + nombre_a_creer + 3, 4, xlwt.Formula(
        "SUMIF(E5:E{}, 6)".format(4 + nombre_a_creer)), format_total_money)
    wb.save(
        f"{config.DOSSIER_COMPTA}/{infos_session['date_for_file']}_{infos_session['heure_for_file']}_{infos_session['expe']}.xlsx")
