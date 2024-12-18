import streamlit as st
import openai
import os
from datetime import datetime

# Configurez votre clé API OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialisez les états de session
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Vous êtes un client fictif jouant un rôle dans une simulation de vente."}
    ]
if "step" not in st.session_state:
    st.session_state.step = 0
if "is_finished" not in st.session_state:
    st.session_state.is_finished = False

# Interface personnalisée
st.title("Simulation de Vente - Photographe")
st.markdown("""
Bienvenue dans votre simulation de vente. Vous interagissez avec un client fictif. 
Répondez à ses questions et essayez de conclure la vente avec un pitch final convaincant. 
""")

# Historique de la conversation
st.markdown("### Historique de la discussion")
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.write(f"**Vous :** {msg['content']}")
    elif msg["role"] == "assistant":
        st.write(f"**Client :** {msg['content']}")

# Entrée utilisateur
if not st.session_state.is_finished:
    user_input = st.text_input("Votre message :", key="user_input")
    if st.button("Envoyer"):
        if user_input:
            # Ajouter le message utilisateur à l'historique
            st.session_state.messages.append({"role": "user", "content": user_input})

            # Appeler l'API OpenAI pour générer une réponse
            with st.spinner("Le client répond..."):
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=st.session_state.messages,
                    max_tokens=150,
                    temperature=0.7
                )
            ai_reply = response["choices"][0]["message"]["content"]
            st.session_state.messages.append({"role": "assistant", "content": ai_reply})

            # Vérifier si le client est prêt à conclure
            if "merci" in ai_reply.lower() or "conclure" in user_input.lower():
                st.session_state.is_finished = True
            st.experimental_rerun()

# Évaluation finale
if st.session_state.is_finished:
    st.markdown("### Évaluation Finale")
    with st.spinner("Analyse des performances..."):
        evaluation = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages + [
                {"role": "system", "content": "Évaluez la performance du vendeur sur 10 en fonction de sa capacité à comprendre les besoins, répondre aux objections, et conclure la vente."}
            ],
            max_tokens=100
        )
    feedback = evaluation["choices"][0]["message"]["content"]
    st.write(f"**Résultat :** {feedback}")

    # Réinitialiser pour une nouvelle simulation
    if st.button("Recommencer la simulation"):
        st.session_state.messages = [
            {"role": "system", "content": "Vous êtes un client fictif jouant un rôle dans une simulation de vente."}
        ]
        st.session_state.step = 0
        st.session_state.is_finished = False
        st.experimental_rerun()
