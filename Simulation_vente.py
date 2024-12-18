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

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "step" not in st.session_state:
    st.session_state.step = 0

if user_id in simulation_log and simulation_log[user_id] == today:
    st.warning("Vous avez déjà réalisé une simulation aujourd'hui. Revenez demain pour une nouvelle simulation.")
else:
    st.title("Simulation de Vente Photographe")

    if st.session_state.step == 0:
        client_message = "Bonjour ! Je cherche un photographe pour un projet spécial. Pouvez-vous m'en dire plus sur vos services ?"
        if len(st.session_state.chat_history) == 0:
            st.session_state.chat_history.append({"client": client_message})
        st.write(f"**Client :** {client_message}")

        response = st.text_input("Votre réponse :", key="step_0_response")
        if st.button("Envoyer votre réponse", key="step_0_send"):
            st.session_state.chat_history.append({"user": response})
            st.session_state.step += 1

    elif st.session_state.step == 1:
        user_response = st.session_state.chat_history[-1]["user"]
        st.write(f"**Votre réponse précédente :** {user_response}")

        completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Vous êtes un client fictif jouant un rôle dans une simulation de vente."},
        {"role": "user", "content": f"Voici l'historique de la conversation : {st.session_state.chat_history}. Répondez de manière naturelle et réaliste."}
    ],
    max_tokens=150
)
        
        ai_reply = completion.choices[0].text.strip()
        st.session_state.chat_history.append({"client": ai_reply})
        st.write(f"**Client :** {ai_reply}")

        response = st.text_input("Votre réponse :", key="step_1_response")
        if st.button("Envoyer votre réponse", key="step_1_send"):
            st.session_state.chat_history.append({"user": response})
            st.session_state.step += 1

    elif st.session_state.step == 2:
        st.write("Continuez la discussion pour répondre aux besoins du client.")

        completion = openai.ChatCompletion.create(
            engine="text-davinci-003",
            prompt=f"Voici l'historique de la conversation : {st.session_state.chat_history}. Le client commence à poser des objections. Répondez en tant que client fictif.",
            max_tokens=150
        )
        ai_reply = completion.choices[0].text.strip()
        st.session_state.chat_history.append({"client": ai_reply})
        st.write(f"**Client :** {ai_reply}")

        response = st.text_input("Votre réponse :", key="step_2_response")
        if st.button("Envoyer votre réponse", key="step_2_send"):
            st.session_state.chat_history.append({"user": response})
            st.session_state.step += 1

    elif st.session_state.step == 3:
        st.write("Finalisez la vente avec un pitch et une proposition de prix.")
        response = st.text_area("Rédigez votre pitch final :", key="final_pitch")
        if st.button("Envoyer votre pitch final", key="final_send"):
            st.session_state.chat_history.append({"user": response})

            completion = openai.ChatCompletion.create(
                engine="text-davinci-003",
                prompt=f"Voici l'historique complet de la conversation : {st.session_state.chat_history}. Évaluez la performance du vendeur sur 10 en fonction de :\\n1. Compréhension des besoins.\\n2. Réponse aux objections.\\n3. Pitch final convaincant.",
                max_tokens=100
            )
            feedback = completion.choices[0].text.strip()
            st.write(f"**Évaluation finale :** {feedback}")

            # Enregistrer la simulation pour aujourd'hui
            simulation_log[user_id] = today
            with open(SIMULATION_LOG, "w") as f:
                json.dump(simulation_log, f)
            st.success("Simulation terminée. Revenez demain pour une nouvelle simulation.")
