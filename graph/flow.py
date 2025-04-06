from agents.nlp_analyzer import analyze_email_body
def flows(dico):
    last_seen_id, subject, sender, recipient, raw_date, body_text, links = dico
    analysis_result = analyze_email_body(body_text)
    print("🛡️ Analyse NLP :\n", analysis_result)