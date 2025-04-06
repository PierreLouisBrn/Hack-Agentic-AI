import requests

MISTRAL_API_KEY = "OZSyUAoFi2DmsjJz5Cuqg8vWeFzG9grq"
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {MISTRAL_API_KEY}",
    "Content-Type": "application/json"
}



# --- Agent 2 : Fusion de deux résumés pour tirer une conclusion argumentée ---
PROMPT_SYSTEM2 = """
Tu es un expert en cybersécurité. Tu reçois deux analyses différentes d’un même e-mail.
Ton rôle est de les comparer et de fournir une conclusion finale en plusieurs phrases sur la probabilité que l’e-mail soit une tentative de phishing.

Ta réponse doit :
- Fusionner les points clés des deux analyses.
- Faire une explication sur le risque réel du mail pour savoir si il est dangereux ou non.

Sois clair et professionnel.
"""

# --- Agent 3 : Résumer la conclusion finale en une seule phrase ---
PROMPT_SYSTEM3 = """
Tu es un assistant en cybersécurité.

Tu vas recevoir une analyse complète de la suspicion d’un e-mail.
Ta tâche est de la **résumer en une seule phrase concise**, qui donne une conclusion claire et directe sur le fait que le mail semble frauduleux ou non.

Sois affirmatif, sans détails.
"""

# --- Agent 4 : Décision binaire True / False ---
PROMPT_SYSTEM4 = """
Tu es un filtre anti-phishing automatique.

Tu vas recevoir une analyse complète d’un e-mail.
Ta mission est de répondre uniquement par `True` (si c'est probablement du phishing) ou `False` (si ce n'est pas du phishing).
Ne fournis aucune explication, juste un booléen.
"""


def ConclusionMail(email_body: str, link: str) -> str:
    payload = {
        "model": "mistral-medium",  # ou mistral-small, selon ton plan
        "messages": [
            {"role": "system", "content": PROMPT_SYSTEM2},
            {"role": "user", "content": f"Voici le contenu à analyser :\n\n{email_body} \n{link}"}
        ],
        "temperature": 0.2
    }

def PhraseMail(email_body: str) -> str:
    payload = {
        "model": "mistral-medium",  # ou mistral-small, selon ton plan
        "messages": [
            {"role": "system", "content": PROMPT_SYSTEM3},
            {"role": "user", "content": f"Voici le contenu à analyser :\n\n{email_body} \n{link}"}
        ],
        "temperature": 0.2
    }

def BoolMail(email_body: str) -> str:
    payload = {
        "model": "mistral-medium",  # ou mistral-small, selon ton plan
        "messages": [
            {"role": "system", "content": PROMPT_SYSTEM4},
            {"role": "user", "content": f"Voici le contenu à analyser :\n\n{email_body}"}
        ],
        "temperature": 0.2
    }

    response = requests.post(MISTRAL_API_URL, headers=HEADERS, json=payload)
    
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"❌ Erreur API : {response.status_code} - {response.text}"