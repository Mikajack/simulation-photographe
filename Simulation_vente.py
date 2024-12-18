import streamlit as st
import openai
import os
import json
from datetime import datetime

# Configurez votre clé API OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Fichier pour enregistrer les simulations
SIMULATION_LOG = "simulation_log.json"

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
    st.title("Simulation de Vente Photographe")

    st.write("Vous allez engager une conversation avec un client potentiel. Répondez aux questions et adaptez votre discours au fur et à mesure de la discussion.")

    if st.button("Commencer la simulation"):
        # Début de la simulation
        chat_history = []

        # Étape 1 : Bris de glace
        client_message = "Bonjour ! Je cherche un photographe pour un projet spécial. Pouvez-vous m'en dire plus sur vos services ?"
        chat_history.append({"client": client_message})
        st.write(f"**Client :** {client_message}")
        response = st.text_input("Votre réponse :", key="intro_response")

        if response:
            chat_history.append({"user": response})
            st.write("L'IA réfléchit...")

            completion = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Vous êtes un client fictif. Voici l'historique de la conversation : {chat_history}. Répondez de manière naturelle et réaliste.",
                max_tokens=150
            )
            ai_reply = completion.choices[0].text.strip()
            chat_history.append({"client": ai_reply})
            st.write(f"**Client :** {ai_reply}")

            # Simulation continue
            if "quand" in response.lower():
                st.write("Le client demande plus de détails sur les dates.")

            if "prix" in response.lower():
                st.write("Le client s'intéresse aux tarifs.")

            if "objections" in ai_reply.lower():
                st.write("Le client a une objection. Répondez pour la contrer.")

            # Finalisation
            if "merci" in response.lower():
                st.write("Le client semble prêt à conclure. Faites votre pitch final et annoncez le prix.")

        # Une fois la simulation terminée, évaluer
        if st.button("Terminer la simulation et évaluer"):
            completion = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Voici l'historique complet de la conversation : {chat_history}. Évaluez la performance du vendeur sur 10 en fonction de sa capacité à :\n1. Comprendre les besoins du client.\n2. Répondre aux objections.\n3. Proposer un pitch convaincant.",
                max_tokens=100
            )
            feedback = completion.choices[0].text.strip()
            st.write(f"**Évaluation finale :** {feedback}")

            # Enregistrer la simulation pour aujourd'hui
            simulation_log[user_id] = today
            with open(SIMULATION_LOG, "w") as f:
                json.dump(simulation_log, f)
