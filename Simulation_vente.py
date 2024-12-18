import streamlit as st
import openai
import os
import json
from datetime import datetime

# Configurez votre clé API OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Fichier pour enregistrer les simulations
SIMULATION_LOG = "simulation_log.json"

# Définir les scénarios
scenarios = {
    "Mariage": [
        "Bonjour, nous cherchons un photographe pour notre mariage. Pouvez-vous nous expliquer ce que vous proposez ?",
        "Quels sont vos tarifs et les avantages de vos services pour un mariage ?",
        "Nous hésitons car nous avons un budget serré. Pouvez-vous nous proposer une option ?",
        "Comment garantissez-vous que nos photos seront uniques et mémorables ?",
        "Pourquoi devrions-nous vous choisir parmi d'autres photographes ?"
    ],
    "Portrait": [
        "Je voudrais un portrait professionnel pour mon CV. Que proposez-vous ?",
        "Quels sont vos tarifs pour un portrait individuel ?",
        "Pouvez-vous retoucher les photos ?",
        "Combien de temps faut-il pour recevoir les photos ?",
        "Pourquoi devrais-je vous choisir comme photographe de portrait ?"
    ]
    # Ajoutez d'autres scénarios ici...
}

# Vérifier si le fichier SIMULATION_LOG existe, sinon le créer
if not os.path.exists(SIMULATION_LOG):
    with open(SIMULATION_LOG, "w") as f:
        json.dump({}, f)

# Charger le journal des simulations
with open(SIMULATION_LOG, "r") as f:
    try:
        simulation_log = json.load(f)
    except json.JSONDecodeError:
        simulation_log = {}
        with open(SIMULATION_LOG, "w") as reset_file:
            json.dump(simulation_log, reset_file)

# Récupérer l'utilisateur actuel (par son nom ou identifiant)
user_id = st.text_input("Entrez votre identifiant utilisateur :", "utilisateur_anonyme")

# Vérifier si une simulation a déjà été faite aujourd'hui
today = datetime.now().strftime("%Y-%m-%d")
if user_id in simulation_log and simulation_log[user_id] == today:
    st.warning("Vous avez déjà réalisé une simulation aujourd'hui. Revenez demain pour une nouvelle simulation.")
else:
    scenario_choice = st.selectbox("Choisissez un scénario :", list(scenarios.keys()))

    if st.button("Commencer la simulation"):
        questions = scenarios[scenario_choice]
        total_score = 0

        st.write("### Simulation de vente")
        for i, question in enumerate(questions):
            st.write(f"**Question {i + 1}:** {question}")
            response = st.text_input(f"Votre réponse à cette question ({i + 1}) :", key=f"response_{i}")

            if response:
                completion = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=f"Analysez cette réponse : '{response}' à la question : '{question}'. "
                           f"Attribuez un score sur 10 en fonction des critères suivants : "
                           f"1. Clarté, 2. Pertinence, 3. Capacité à gérer les objections.",
                    max_tokens=100
                )
                feedback = completion.choices[0].text.strip()
                st.write(f"**Évaluation AI :** {feedback}")
                try:
                    score = int(feedback.split(":")[-1].strip())
                except ValueError:
                    score = 0
                total_score += score

        st.success(f"Score final : {total_score} / {len(questions) * 10}")

        # Enregistrer la simulation pour aujourd'hui
        simulation_log[user_id] = today
        with open(SIMULATION_LOG, "w") as f:
            json.dump(simulation_log, f)
