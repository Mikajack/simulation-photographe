import streamlit as st
import openai
import os
import json
from datetime import datetime

# Configurez votre clé API OpenAI
openai.api_key = "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"

# Fichier pour enregistrer les simulations
SIMULATION_LOG = "simulation_log.json"

# Initialiser les scénarios
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
    ],
    "Mode": [
        "Nous recherchons un photographe pour une séance de mode. Quels sont vos services ?",
        "Comment garantissez-vous que vos photos capturent bien nos vêtements et accessoires ?",
        "Pouvez-vous proposer des lieux ou des styles pour notre campagne ?",
        "Quels sont vos tarifs pour une séance complète ?",
        "Pourquoi devrions-nous vous engager pour cette séance de mode ?"
    ],
    "Grossesse": [
        "Je veux immortaliser ma grossesse. Que proposez-vous ?",
        "Quels sont vos tarifs pour une séance photo de grossesse ?",
        "Pouvez-vous inclure mon conjoint et mes enfants dans les photos ?",
        "Avez-vous des accessoires ou vêtements pour la séance ?",
        "Pourquoi devrais-je choisir vos services pour cette étape importante ?"
    ],
    "Packshot": [
        "Nous avons besoin de photos de nos produits pour un site web. Que proposez-vous ?",
        "Quels sont vos tarifs pour des photos de produit en studio ?",
        "Pouvez-vous ajouter des retouches pour améliorer l’apparence des produits ?",
        "Comment garantissez-vous que vos photos sont adaptées au e-commerce ?",
        "Pourquoi devrions-nous travailler avec vous pour nos photos de produit ?"
    ],
    "Nouveau-né": [
        "Je veux des photos de mon nouveau-né. Que proposez-vous ?",
        "Quels sont vos tarifs pour une séance photo de bébé ?",
        "Pouvez-vous garantir que la séance sera sans stress pour le bébé ?",
        "Quels accessoires fournissez-vous pour la séance ?",
        "Pourquoi devrais-je choisir vos services pour cette séance unique ?"
    ],
    "Corporate": [
        "Nous recherchons un photographe pour des portraits d'équipe. Pouvez-vous nous expliquer vos services ?",
        "Quels sont vos tarifs pour une séance en entreprise ?",
        "Nous avons une contrainte de temps. Combien de temps dure une séance ?",
        "Comment garantissez-vous que vos photos reflètent notre image professionnelle ?",
        "Pourquoi devrions-nous travailler avec vous pour ce projet ?"
    ],
    "Architecture": [
        "Nous avons besoin d’un photographe pour capturer des bâtiments. Pouvez-vous nous expliquer vos services ?",
        "Quels sont vos tarifs pour photographier un projet immobilier ?",
        "Nous cherchons à différencier notre portfolio. Qu'est-ce qui rend votre travail unique ?",
        "Comment garantissez-vous des photos précises et professionnelles ?",
        "Pourquoi devrions-nous choisir vos services pour notre projet ?"
    ],
    "Culinaire": [
        "Nous recherchons un photographe pour des plats. Quels sont vos services ?",
        "Comment garantissez-vous que vos photos donnent envie de goûter ?",
        "Quels sont vos tarifs pour une séance culinaire ?",
        "Pouvez-vous inclure la retouche pour améliorer les couleurs et les textures ?",
        "Pourquoi devrions-nous choisir vos services pour ce projet culinaire ?"
    ],
    "Animalier": [
        "Je veux des photos de mon animal de compagnie. Que proposez-vous ?",
        "Quels sont vos tarifs pour une séance photo animale ?",
        "Pouvez-vous garantir que mon animal sera à l’aise durant la séance ?",
        "Quels accessoires utilisez-vous pour les photos d’animaux ?",
        "Pourquoi devrais-je choisir vos services pour immortaliser mon compagnon ?"
    ],
    "Sport": [
        "Nous cherchons un photographe pour couvrir un événement sportif. Quels sont vos services ?",
        "Quels sont vos tarifs pour une journée complète de reportage sportif ?",
        "Comment garantissez-vous que vos photos capturent bien l'action ?",
        "Pouvez-vous livrer les photos rapidement après l'événement ?",
        "Pourquoi devrions-nous vous choisir comme photographe de sport ?"
    ],
    "Paysage": [
        "Je voudrais une photo artistique de paysages. Que proposez-vous ?",
        "Quels sont vos tarifs pour des tirages de vos photos de paysage ?",
        "Pouvez-vous personnaliser un cadre ou un format pour mon mur ?",
        "Comment garantissez-vous que vos photos sont uniques ?",
        "Pourquoi devrais-je acheter vos œuvres photographiques ?"
    ],
    "Voyage": [
        "Je voudrais immortaliser mon prochain voyage. Que proposez-vous ?",
        "Quels sont vos tarifs pour m’accompagner lors de ce voyage ?",
        "Comment garantissez-vous que les photos reflèteront bien mes souvenirs ?",
        "Pouvez-vous aussi capturer des portraits pendant le voyage ?",
        "Pourquoi devrais-je vous engager pour ce projet de voyage ?"
    ],
    "Autres": [
        "Expliquez-nous vos besoins, et nous personnaliserons l'expérience pour vous."
    ]
}

# Charger ou initialiser le journal des simulations
if os.path.exists(SIMULATION_LOG):
    with open(SIMULATION_LOG, "r") as f:
        simulation_log = json.load(f)
else:
    simulation_log = {}

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

        for question in questions:
            st.subheader(f"Question : {question}")
            response = st.text_input(f"Votre réponse à : {question}")

            if st.button(f"Évaluer la réponse à : {question}"):
                completion = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=f"Analysez cette réponse : '{response}' à la question : '{question}'. "
                           f"Attribuez un score sur 10 en fonction des critères suivants : "
                           f"1. Clarté, 2. Pertinence, 3. Capacité à gérer les objections.",
                    max_tokens=100
                )
                feedback = completion.choices[0].text.strip()
                st.write(f"Évaluation AI : {feedback}")
                try:
                    score = int(feedback.split(":")[-1].strip())
                except ValueError:
                    score = 0
                total_score += score

        st.success(f"Score final : {total_score} / {len(questions) * 10}")

        # Enregistrer la simulation pour aujourd'hui
        simulation_log[user_id] = today
        
  # Vérifier si le fichier existe, sinon le créer
if not os.path.exists(SIMULATION_LOG):
    with open(SIMULATION_LOG, "w") as f:
        json.dump({}, f)

# Charger le contenu du fichier
with open(SIMULATION_LOG, "r") as f:
    try:
        simulation_log = json.load(f)
    except json.JSONDecodeError:
        simulation_log = {}
        # Réinitialiser le fichier en cas d'erreur
        with open(SIMULATION_LOG, "w") as reset_file:
            json.dump(simulation_log, reset_file)

