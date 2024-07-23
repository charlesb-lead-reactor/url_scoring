import streamlit as st
import pandas as pd
import datetime
import random
from sklearn.preprocessing import MinMaxScaler

def calculer_score(df, weights):
    df_normalized = df.copy()
    
    # Normalisation de toutes les variables numériques
    scaler = MinMaxScaler()
    colonnes_a_normaliser = ['volume', 'position', 'cpc', 'jours_depuis_maj']
    df_normalized[colonnes_a_normaliser] = scaler.fit_transform(df[colonnes_a_normaliser])
    
    # Inversion du score de position normalisé (plus la position est basse, meilleur est le score)
    df_normalized['score_position'] = 1 - df_normalized['position']
    
    # Inversion du score de fraîcheur normalisé (plus récent est meilleur)
    df_normalized['score_fraicheur'] = 1 - df_normalized['jours_depuis_maj']
    
    # Calcul du score total
    score = (df_normalized['volume'] * weights['volume'] +
             df_normalized['score_position'] * weights['position'] +
             df_normalized['cpc'] * weights['cpc'] +
             df_normalized['score_fraicheur'] * weights['fraicheur'])
    
    return score * 100

def calculer_score2(df, weights, position_weights, freshness_weights):
    df_normalized = df.copy()
    
    # Normalisation de toutes les variables numériques
    scaler = MinMaxScaler()
    colonnes_a_normaliser = ['volume', 'cpc', 'jours_depuis_maj']
    df_normalized[colonnes_a_normaliser] = scaler.fit_transform(df[colonnes_a_normaliser])
    
    # Calcul du score de position personnalisé
    df_normalized['score_position'] = df['position'].apply(lambda x: 
        position_weights['top3'] if x <= 3 else
        position_weights['top10'] if x <= 10 else
        position_weights['top20'] if x <= 20 else
        position_weights['above20']
    )
    
    # Calcul du score de fraîcheur personnalisé
    df_normalized['score_fraicheur'] = df['jours_depuis_maj'].apply(lambda x:
        freshness_weights['less45'] if x <= 45 else
        freshness_weights['less90'] if x <= 90 else
        freshness_weights['above90']
    )
    
    # Calcul du score total
    score = (df_normalized['volume'] * weights['volume'] +
             df_normalized['score_position'] * weights['position'] +
             df_normalized['cpc'] * weights['cpc'] +
             df_normalized['score_fraicheur'] * weights['fraicheur'])
    
    return score * 100

def generer_donnees_test():
    mots_cles = [
        'master rse à distance', 'master rse et développement durable',
        'master rse alternance paris', 'master rse université',
        'master rse paris', 'master rse alternance',
        'classement master rse', 'master rse formation continue',
        'master rse débouchés', 'master rse cnam',
        'master 2 rse alternance', 'master 2 rse paris',
        'école rse paris', 'top master rse france',
        'meilleur master rse 2024', 'classement master rse europe',
        'classement master rse mondial', 'palmarès master rse',
        'master rse temps plein', 'master rse cours du soir',
        'master rse en ligne', 'master rse intensif',
        'master rse formation hybride'
    ]
    
    data = {
        'url': ['https://example.com/' + '-'.join(mc.split()) for mc in mots_cles],
        'mot_cle': mots_cles,
        'volume': [random.randint(100, 5000) for _ in range(len(mots_cles))],
        'position': [random.randint(1, 50) for _ in range(len(mots_cles))],
        'cpc': [round(random.uniform(0.5, 10.0), 2) for _ in range(len(mots_cles))],
        'date_maj': [
            datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 150))
            for _ in range(len(mots_cles))
        ]
    }
    
    return pd.DataFrame(data)

# Titre de l'application
st.title("Scoring SEO des contenus")

st.sidebar.header("Ajustement des poids")

# Poids pour les scores
weight_volume = st.sidebar.slider("Poids du volume", 0.0, 1.0, 0.25, 0.05)
weight_position = st.sidebar.slider("Poids de la position", 0.0, 1.0, 0.40, 0.05)
weight_cpc = st.sidebar.slider("Poids du CPC", 0.0, 1.0, 0.20, 0.05)
weight_fraicheur = st.sidebar.slider("Poids de la fraîcheur", 0.0, 1.0, 0.15, 0.05)

# Normalisation des poids
total_weight = weight_volume + weight_position + weight_cpc + weight_fraicheur
weight_volume /= total_weight
weight_position /= total_weight
weight_cpc /= total_weight
weight_fraicheur /= total_weight

st.sidebar.write("Poids normalisés :")
st.sidebar.write(f"Volume : {weight_volume:.2f}")
st.sidebar.write(f"Position : {weight_position:.2f}")
st.sidebar.write(f"CPC : {weight_cpc:.2f}")
st.sidebar.write(f"Fraîcheur : {weight_fraicheur:.2f}")

st.sidebar.header("Poids pour Score 2")

# Poids pour les positions
st.sidebar.subheader("Poids des positions")
weight_top3 = st.sidebar.slider("Top 3", 0.0, 1.0, 0.1, 0.05)
weight_top10 = st.sidebar.slider("Top 4-10", 0.0, 1.0, 1.0, 0.05)
weight_top20 = st.sidebar.slider("Top 11-20", 0.0, 1.0, 0.8, 0.05)
weight_above20 = st.sidebar.slider("Au-delà du top 20", 0.0, 1.0, 0.5, 0.05)

# Poids pour la fraîcheur
st.sidebar.subheader("Poids de la fraîcheur")
weight_less45 = st.sidebar.slider("Moins de 45 jours", 0.0, 1.0, 0.1, 0.05)
weight_less90 = st.sidebar.slider("Entre 45 et 90 jours", 0.0, 1.0, 0.8, 0.05)
weight_above90 = st.sidebar.slider("Plus de 90 jours", 0.0, 1.0, 1.0, 0.05)

# Option pour utiliser des données de test ou uploader un fichier
option = st.radio("Choisissez une option :", ("Utiliser des données de test", "Uploader un fichier CSV"))

if option == "Utiliser des données de test":
    df = generer_donnees_test()
else:
    uploaded_file = st.file_uploader("Choisissez votre fichier CSV", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        st.warning("Veuillez uploader un fichier CSV.")
        st.stop()

# Traitement des données
if df is not None:
    if df['date_maj'].dtype != 'datetime64[ns]':
        df['date_maj'] = pd.to_datetime(df['date_maj'])
    df['jours_depuis_maj'] = (datetime.datetime.now() - df['date_maj']).dt.days

    weights = {
        'volume': weight_volume,
        'position': weight_position,
        'cpc': weight_cpc,
        'fraicheur': weight_fraicheur
    }

    position_weights = {
        'top3': weight_top3,
        'top10': weight_top10,
        'top20': weight_top20,
        'above20': weight_above20
    }

    freshness_weights = {
        'less45': weight_less45,
        'less90': weight_less90,
        'above90': weight_above90
    }

    df['score'] = calculer_score(df, weights)
    df['score2'] = calculer_score2(df, weights, position_weights, freshness_weights)
    
    df_sorted = df.sort_values('score2', ascending=False)
    
    st.dataframe(df_sorted)
    
    st.subheader("Comparaison des scores")
    chart_data = df_sorted[['url', 'score', 'score2']].set_index('url')
    st.bar_chart(chart_data)
    
    csv = df_sorted.to_csv(index=False)
    st.download_button(
        label="Télécharger les résultats en CSV",
        data=csv,
        file_name="resultats_scoring_seo.csv",
        mime="text/csv",
    )