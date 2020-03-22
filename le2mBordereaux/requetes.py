

def get_requete_participants(expe, date, heure):
    req_full = (
        "SELECT sub.participant_id as UID, sub.gender as Genre, sub.lname as Nom, sub.fname as Prénom, "
        "sub.email as Mail, sub.begin_of_studies as 'Début des études', lg.fr as Discipline "
        "FROM or_participants sub, or_experiments exp, or_sessions sess, or_participate_at part, or_lang lg "
        f"WHERE exp.experiment_name = '{expe}' "
        "AND sess.experiment_id = exp.experiment_id "
        f"AND sess.session_start = {date.strftime('%Y%m%d')}{heure.strftime('%H%M')} "
        "AND part.session_id = sess.session_id "
        "AND sub.participant_id = part.participant_id "
        "AND lg.content_type = 'field_of_studies' "
        "AND lg.content_name = sub.field_of_studies "
        "order by sub.lname, sub.fname"
    )
    # req = (
    #         "SELECT sub.lname, sub.fname "
    #         "FROM or_participants sub, or_experiments exp, or_sessions sess, or_participate_at part "
    #         "WHERE exp.experiment_name = '{}' "
    #         "AND sess.experiment_id = exp.experiment_id "
    #         "AND sess.session_start = {}{} "
    #         "AND part.session_id = sess.session_id "
    #         "AND sub.participant_id = part.participant_id "
    #         "order by sub.lname, sub.fname".format(expe, date.strftime("%Y%m%d"), heure.strftime("%H%M"))
    # )
    return req_full
