# pages/2_Análise_Geográfica.py

import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.set_page_config(layout="wide", page_title="Análise Geográfica")

# --- CORES DA PALETA PYTHON ---
PYTHON_BLUE = "#3776AB"
PYTHON_YELLOW = "#FFD43B"

st.markdown("## 🌎 Análise Geográfica")
st.markdown("### Central de Análise Geográfica")

# Acessa o dataframe filtrado
if 'df_filtered' not in st.session_state:
    st.warning("Por favor, aplique os filtros na página principal primeiro.")
    st.stop()
df_filtered = st.session_state['df_filtered']

# Seletor de Métricas
metric_options = {
    'Receita Total': 'payment_value_sum',
    'Ticket Médio': 'ticket_medio',
    'Número de Pedidos': 'order_count'
}
selected_metric_label = st.selectbox("Selecione uma métrica para analisar:", options=list(metric_options.keys()))
selected_metric_col = metric_options[selected_metric_label]

# Cálculo das métricas por estado
state_stats = df_filtered.groupby('customer_state', as_index=False).agg(
    payment_value_sum=('payment_value', 'sum'),
    order_count=('order_id', 'nunique')
)
state_stats['ticket_medio'] = state_stats['payment_value_sum'] / state_stats['order_count']
state_stats = state_stats.sort_values(by=selected_metric_col, ascending=False)

col1, col2 = st.columns(2)

with col1, st.container():
    st.markdown(f"#### 🗺️ Mapa de {selected_metric_label} por Estado")
    try:
        with open("br_states.json") as f:
            geojson_data = json.load(f)
    except FileNotFoundError:
        st.error("Arquivo 'br_states.json' não encontrado.")
        st.stop()
        
    fig_map = px.choropleth(
        state_stats, geojson=geojson_data, locations='customer_state', 
        featureidkey="properties.sigla", color=selected_metric_col,
        color_continuous_scale=px.colors.sequential.Blues, hover_name='customer_state',
        hover_data={'customer_state': False, selected_metric_col: ':.2f'}
    )
    fig_map.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig_map, use_container_width=True)

with col2, st.container():
    st.markdown(f"#### 🏆 Top 5 Estados por {selected_metric_label}")
    top_5_states = state_stats.head(5)
    fig_bar_states = px.bar(
        top_5_states, x=selected_metric_col, y='customer_state', orientation='h',
        text_auto='.2s', color_discrete_sequence=[PYTHON_BLUE]
    )
    fig_bar_states.update_layout(
        xaxis_title=selected_metric_label, yaxis_title="Estado", 
        showlegend=False, yaxis={'categoryorder':'total ascending'}
    )
    st.plotly_chart(fig_bar_states, use_container_width=True)