

def get_requete_participants(expe, date, heure):
    req = (
            "SELECT sub.lname, sub.fname "
            "FROM or_participants sub, or_experiments exp, or_sessions sess, or_participate_at part "
            "WHERE exp.experiment_name = '{}' "
            "AND sess.experiment_id = exp.experiment_id "
            "AND sess.session_start = {}{} "
            "AND part.session_id = sess.session_id "
            "AND sub.participant_id = part.participant_id "
            "order by sub.lname, sub.fname".format(expe, date.strftime("%Y%m%d"), heure.strftime("%H%M"))
    )
    return req
