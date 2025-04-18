import requests
import base64
import time

# === CLÉS API ===
VT_API_KEY = "44f476f9d7fa7bc5e17fd3d684daf305433690539cc8ef695079a611db891de0"
URLSCAN_API_KEY = "0196069f-be55-752a-a032-f1f368c3ea4d"
MISTRAL_API_KEY = "OZSyUAoFi2DmsjJz5Cuqg8vWeFzG9grq"
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

# === VIRUSTOTAL ===
def analyser_url_virustotal(url):
    headers = {"x-apikey": VT_API_KEY}
    submit_url = "https://www.virustotal.com/api/v3/urls"
    report_url_base = "https://www.virustotal.com/api/v3/urls/"

    response = requests.post(submit_url, headers=headers, data={"url": url})
    if response.status_code != 200:
        print("❌ VirusTotal - erreur de soumission :", response.text)
        return None

    print("✅ URL soumise avec succès. ⏳ Attente de l’analyse...")
    time.sleep(20)

    url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
    report_response = requests.get(f"{report_url_base}{url_id}", headers=headers)
    if report_response.status_code != 200:
        print("❌ VirusTotal - erreur de rapport :", report_response.text)
        return None

    data = report_response.json()["data"]["attributes"]

    stats = data.get("last_analysis_stats", {})
    categories = data.get("categories", {})
    reputation = data.get("reputation", 0)
    times_submitted = data.get("times_submitted", "N/A")
    votes = data.get("total_votes", {})

    print("\n🔍 Résultat détaillé de VirusTotal :")
    print(f"🌐 URL analysée         : {url}")
    print(f"📊 Statistiques         :")
    print(f"   - Harmless           : {stats.get('harmless', 0)}")
    print(f"   - Malicious          : {stats.get('malicious', 0)}")
    print(f"   - Suspicious         : {stats.get('suspicious', 0)}")
    print(f"   - Undetected         : {stats.get('undetected', 0)}")
    print(f"   - Timeout            : {stats.get('timeout', 0)}")
    print(f"🏷️  Catégories détectées : {categories if categories else 'Aucune'}")
    print(f"⭐ Réputation VT         : {reputation}")
    print(f"📥 Nombre de soumissions : {times_submitted}")
    print(f"🗳️ Votes de la communauté : Malveillant={votes.get('malicious', 0)}, Bénin={votes.get('harmless', 0)}")

    return data


# === URLSCAN.IO ===
def analyser_url_urlscan(url):
    headers = {"API-Key": URLSCAN_API_KEY, "Content-Type": "application/json"}
    data = {"url": url, "visibility": "public"}

    response = requests.post("https://urlscan.io/api/v1/scan/", headers=headers, json=data)
    if response.status_code != 200:
        print("❌ urlscan.io - erreur de soumission :", response.text)
        return None

    uuid = response.json().get("uuid")
    print(f"\n📡 Lien soumis. UUID : {uuid}")
    time.sleep(20)

    result = requests.get(f"https://urlscan.io/api/v1/result/{uuid}/")
    if result.status_code != 200:
        print("❌ urlscan.io - erreur de récupération :", result.text)
        return None

    data = result.json()

    # AFFICHAGE
    task = data.get("task", {})
    page = data.get("page", {})
    verdict = data.get("verdicts", {}).get("overall", {})
    lists = data.get("lists", {})

    print("\n🔍 Résultat du scan urlscan.io :")
    print(f"🕒 Date           : {task.get('time')}")
    print(f"🌍 URL soumise   : {task.get('url')}")
    print(f"📥 URL finale    : {page.get('url')}")
    print(f"🖼️  Titre         : {page.get('title')}")
    print(f"🌐 Domaine       : {page.get('domain')}")
    print(f"🏁 Pays          : {page.get('country')}")
    print(f"🛡️ Verdicts      : {verdict}")
    print(f"🔗 Liens trouvés : {len(lists.get('urls', []))} URL chargées")
    print(f"📸 Screenshot    : {task.get('screenshotURL')}")
    print(f"📝 Rapport complet : {task.get('reportURL')}")

    return data




# === IA : CLASSIFICATION ===
def evaluer_et_expliquer_risque(data_vt, data_urlscan):
    vt_stats = data_vt.get("last_analysis_stats", {})
    vt_categories = data_vt.get("categories", {})
    vt_votes = data_vt.get("total_votes", {})
    vt_reputation = data_vt.get("reputation", 0)
    malicious = vt_stats.get("malicious", 0)
    suspicious = vt_stats.get("suspicious", 0)

    verdict = data_urlscan.get("verdicts", {}).get("overall", {})
    urlscan_score = verdict.get("score", 0)
    urlscan_tags = verdict.get("tags", [])
    urlscan_malicious = verdict.get("malicious", False)
    title = data_urlscan.get("page", {}).get("title", "N/A")

    prompt = f"""
Tu es un expert en cybersécurité. On te donne les résultats de l’analyse d’un lien :
VirusTotal :
- moteurs malicieux : {malicious}
- moteurs suspects : {suspicious}
- catégories : {vt_categories if vt_categories else 'Aucune'}
- réputation : {vt_reputation}
- votes : {vt_votes}

urlscan.io :
- score : {urlscan_score}
- tags : {urlscan_tags}
- malicieux : {urlscan_malicious}
- titre de la page : "{title}"

Classe ce lien comme l’un des trois niveaux suivants : 
1. ❌ DANGEREUX
2. ⚠️ SUSPECT
3. ✅ SÛR

Commence ta réponse par le niveau exact (exemple : ❌ DANGEREUX), puis explique brièvement pourquoi.
"""

    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "mistral-small",  # ou mistral-medium / mistral-large si accessible
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }

    response = requests.post(MISTRAL_API_URL, headers=headers, json=body)
    if response.status_code != 200:
        print("❌ Erreur API Mistral :", response.text)
        return "Indéterminé", "L'appel à Mistral a échoué."

    content = response.json()["choices"][0]["message"]["content"].strip()
    niveau = content.split('\n')[0] if '\n' in content else content
    explication = content

    return niveau, explication


# === EXÉCUTION ===
def linkanalize(url):
    vt_data = analyser_url_virustotal(url)
    us_data = analyser_url_urlscan(url)

    if vt_data and us_data:
        niveau, explication = evaluer_et_expliquer_risque(vt_data, us_data)
        print(f"\n🔐 Verdict final : {niveau}")
        print(explication)
    else:
        niveau = 0
        explication="Impossible de conclure : une des deux analyses a échoué."
        print("❌ Impossible de conclure : une des deux analyses a échoué.")
    return niveau, explication

#print(linkanalize("https://bnstockton.com"))