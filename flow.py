from agents.nlp_analyzer import analyze_email_body
from agents.link_analyzer import linkanalize
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

    





    

    return {
        "msg_id": msg_id,
        "is_phishing": is_phishing,
        "summary": summary,
        "reason": reason
    }


def test():
    

    
    for i in links:
        li=links[i]
        link_grade, link_analyze = linkanalize(li)
        print("grade link",link_grade)

test()