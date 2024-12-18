import streamlit as st
import openai

# Configurez votre clé API OpenAI
openai.api_key = "VOTRE_CLE_API"

# Initialisez l'état de session
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Vous êtes un client fictif jouant un rôle dans une simulation de vente."}
    ]

# Titre de l'application
st.title("Simulation de Vente Photographe")

# Affichez l'historique de la conversation
st.write("### Historique de la discussion")
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.write(f"**Vous :** {msg['content']}")
    elif msg["role"] == "assistant":
        st.write(f"**Client :** {msg['content']}")

# Champ pour l'utilisateur
user_input = st.text_input("Votre message :", key="user_input")

# Si l'utilisateur envoie un message
if st.button("Envoyer"):
    if user_input:
        # Ajouter le message de l'utilisateur à l'historique
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

        # Ajouter la réponse de l'IA à l'historique
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})

        # Effacer le champ de saisie
        st.experimental_rerun()
