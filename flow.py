from agents.nlp_analyzer import analyze_email_body
from agents.link_analyzer import linkanalize
from agents.report_generator import ConclusionMail,PhraseMail,BoolMail

def flows(dico):
    last_seen_id, subject, sender, recipient, raw_date, body_text, links = dico
    body_analysis = analyze_email_body(body_text)
    print("🛡️ Analyse NLP :\n", body_analysis)

    if links != "":
        link_grade, link_analyze = linkanalize(links)
        print("grade link",link_grade)
    else:
        link_grade = 5
        link_analyze ="Impossible de conclure : une des deux analyses a échoué."



    summary=ConclusionMail(body_analysis,link_analyze)
    print("analyse",summary)
    reason=PhraseMail(summary)
    print("reason",reason)
    is_phishing=BoolMail(summary)
    print("bool ", is_phishing)

    

    return {
        "is_phishing": is_phishing,
        "summary": summary,
        "reason": reason
    }


def test():
    Mail="""Bonjour,

    Nous avons détecté une activité inhabituelle sur votre compte. Pour des raisons de sécurité, votre accès a été temporairement suspendu.

    Veuillez confirmer vos informations dans les 24 heures pour éviter la suppression définitive de votre compte :

    


    Sans réponse de votre part, nous serons dans l’obligation de clôturer définitivement votre compte, conformément à nos conditions générales d’utilisation.

    Merci de votre compréhension."""
    link="https://bnstockton.com"
    body_analysis = analyze_email_body(Mail)
    print("🛡️ Analyse NLP :\n", body_analysis)

    if link != "":
        link_grade, link_analyze = linkanalize(link)
        print("grade link",link_grade)
    else:
        link_grade = 5
        link_analyze ="Impossible de conclure : une des deux analyses a échoué."


    summary=ConclusionMail(body_analysis,link_analyze)
    print("analyse",summary)
    reason=PhraseMail(summary)
    print("reason",reason)
    is_phishing=BoolMail(summary)
    print("bool ", is_phishing)

test()