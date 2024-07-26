import streamlit as st
import pandas as pd
import datetime
import random
import plotly.express as px


def normalize_weights(weights):
    total = sum(weights.values())
    return {k: v / total for k, v in weights.items()}

def display_normalized_weights(weights, title):
    st.sidebar.markdown(f"<p style='font-size:12px; margin-bottom:0;'><u>Normalized <strong>{title}</strong> weights</u>:</p>", unsafe_allow_html=True)
    for k, v in weights.items():
        st.sidebar.markdown(f"<p style='font-size:11px; margin:0;'>{k}: {v:.2f}</p>", unsafe_allow_html=True)
    st.sidebar.markdown("<br>", unsafe_allow_html=True)  # Ajoute un peu d'espace après chaque groupe

def get_position_score(position, weights):
    if position <= 3:
        return weights['top3']
    elif position <= 10:
        return weights['top10']
    elif position <= 20:
        return weights['top20']
    else:
        return weights['above20']

def get_freshness_score(days, weights):
    if days <= 45:
        return weights['less45']
    elif days <= 90:
        return weights['less90']
    else:
        return weights['above90']

def calculate_score(row, weights, df_min, df_max):
    normalized_values = {
        'volume': (row['volume'] - df_min['volume']) / (df_max['volume'] - df_min['volume']),
        'position': 1 - (row['position'] - df_min['position']) / (df_max['position'] - df_min['position']),
        'cpc': (row['cpc'] - df_min['cpc']) / (df_max['cpc'] - df_min['cpc']),
        'freshness': 1 - (row['days_since_update'] - df_min['days_since_update']) / (df_max['days_since_update'] - df_min['days_since_update'])
    }
    
    score = sum(normalized_values[key] * weights[key] for key in weights)
    return round(score * 100, 1)

def calculate_score2(row, weights, position_weights, freshness_weights, df_min, df_max):
    normalized_values = {
        'volume': (row['volume'] - df_min['volume']) / (df_max['volume'] - df_min['volume']),
        'cpc': (row['cpc'] - df_min['cpc']) / (df_max['cpc'] - df_min['cpc']),
    }
    
    position_score = get_position_score(row['position'], position_weights)
    freshness_score = get_freshness_score(row['days_since_update'], freshness_weights)
    
    score = (normalized_values['volume'] * weights['volume'] +
             position_score * weights['position'] +
             normalized_values['cpc'] * weights['cpc'] +
             freshness_score * weights['freshness'])
    
    return round(score * 100, 1)

def generate_test_data():
    keywords = [
        'online csr master', 'csr and sustainable development master',
        'csr master internship paris', 'csr master university',
        'csr master paris', 'csr master internship',
        'csr master ranking', 'csr master continuing education',
        'csr master job prospects', 'csr master cnam',
        'csr master 2 internship', 'csr master 2 paris',
        'csr school paris', 'top csr master france',
        'best csr master 2024', 'csr master ranking europe',
        'csr master global ranking', 'csr master awards',
        'full-time csr master', 'evening csr master',
        'online csr master', 'intensive csr master',
        'hybrid csr master'
    ]
    
    data = {
        'url': ['https://example.com/' + '-'.join(kw.split()) for kw in keywords],
        'keyword': keywords,
        'volume': [random.randint(100, 5000) for _ in range(len(keywords))],
        'position': [random.randint(1, 50) for _ in range(len(keywords))],
        'cpc': [round(random.uniform(0.5, 10.0), 2) for _ in range(len(keywords))],
        'last_update_date': [
            datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 150))
            for _ in range(len(keywords))
        ]
    }
    
    return pd.DataFrame(data)

def plot_horizontal_bar(df):
    fig = px.bar(df.sort_values('score2', ascending=True).tail(20), 
                 y='keyword', x='score2', 
                 orientation='h',
                 color='score2',
                 color_continuous_scale='RdYlGn',
                 title='Top 20 Keywords by Score2')
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig)

def plot_scatter(df):
    fig = px.scatter(df, x='score2', y='volume', 
                     color='position', size='cpc',
                     hover_name='keyword',
                     color_continuous_scale='Viridis',
                     title='Score2 vs Volume, Position, and CPC')
    st.plotly_chart(fig)

def read_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


st.set_page_config(layout="wide", page_title="SEO Content Scoring - Python Script")
# Application title
st.markdown(read_markdown_file('src/templates/navbar.md'), unsafe_allow_html=True)
st.title("SEO Content Scoring (light version)")

st.sidebar.header("Weight Adjustment (both score)")
# Main weights
main_weights = normalize_weights({
    'volume': st.sidebar.slider("Volume Weight", 0.0, 1.0, 0.25, 0.05),
    'position': st.sidebar.slider("Position Weight", 0.0, 1.0, 0.40, 0.05),
    'cpc': st.sidebar.slider("CPC Weight", 0.0, 1.0, 0.20, 0.05),
    'freshness': st.sidebar.slider("Freshness Weight", 0.0, 1.0, 0.15, 0.05)
})
display_normalized_weights(main_weights, "main")

st.sidebar.header("Weight Adjustment (only for score2)")
# Position weights
st.sidebar.subheader("Weights for position")
position_weights = normalize_weights({
    'top3': st.sidebar.slider("Top 3", 0.0, 1.0, 0.1, 0.05),
    'top10': st.sidebar.slider("Top 4-10", 0.0, 1.0, 1.0, 0.05),
    'top20': st.sidebar.slider("Top 11-20", 0.0, 1.0, 0.8, 0.05),
    'above20': st.sidebar.slider("Beyond top 20", 0.0, 1.0, 0.5, 0.05)
})
display_normalized_weights(position_weights, "position")

# Freshness weights
st.sidebar.subheader("Weights for freshness")
freshness_weights = normalize_weights({
    'less45': st.sidebar.slider("Less than 45 days", 0.0, 1.0, 0.1, 0.05),
    'less90': st.sidebar.slider("Between 45 and 90 days", 0.0, 1.0, 0.8, 0.05),
    'above90': st.sidebar.slider("More than 90 days", 0.0, 1.0, 1.0, 0.05)
})
display_normalized_weights(freshness_weights, "freshness")

# Option to use test data or upload a file
st.markdown("---")
option = st.radio("Choose an option:", ("Use test data", "Upload a CSV file"))

if option == "Use test data":
    df = generate_test_data()
else:
    uploaded_file = st.file_uploader("Choose your CSV file", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        st.warning("Please upload a CSV file.")
        st.stop()

# Data processing
if df is not None:
    if df['last_update_date'].dtype != 'datetime64[ns]':
        df['last_update_date'] = pd.to_datetime(df['last_update_date'])
    df['days_since_update'] = (datetime.datetime.now() - df['last_update_date']).dt.days

    df_min = df[['volume', 'position', 'cpc', 'days_since_update']].min()
    df_max = df[['volume', 'position', 'cpc', 'days_since_update']].max()

    df['score'] = df.apply(lambda row: calculate_score(row, main_weights, df_min, df_max), axis=1)
    df['score2'] = df.apply(lambda row: calculate_score2(row, main_weights, position_weights, freshness_weights, df_min, df_max), axis=1)
    
    df_sorted = df.sort_values('score2', ascending=False)
    
    st.dataframe(df_sorted)

    plot_horizontal_bar(df_sorted)
    plot_scatter(df_sorted)
    
    csv = df_sorted.to_csv(index=False)
    st.download_button(
        label="Download results as CSV",
        data=csv,
        file_name="seo_scoring_results.csv",
        mime="text/csv",
    )

st.markdown(read_markdown_file('src/templates/content.md'), unsafe_allow_html=True)
st.markdown("---")
st.markdown(read_markdown_file('src/templates/cta.md'), unsafe_allow_html=True)
st.markdown("---")
st.markdown(read_markdown_file('src/templates/footer.md'), unsafe_allow_html=True)