# pages/3_Análise_de_Clientes.py

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Análise de Clientes")

# --- CORES DA PALETA PYTHON ---
PYTHON_BLUE = "#3776AB"
PYTHON_YELLOW = "#FFD43B"

st.markdown("## 👥 Análise de Clientes")
st.markdown("### Funil de Vendas e Satisfação do Cliente")

# Acessa o dataframe filtrado
if 'df_filtered' not in st.session_state:
    st.warning("Por favor, aplique os filtros na página principal primeiro.")
    st.stop()
df_filtered = st.session_state['df_filtered']

col1, col2 = st.columns(2)

with col1, st.container():
    st.markdown("####  funnel Funil de Vendas")
    created_orders = df_filtered['order_id'].nunique()
    paid_orders = df_filtered[df_filtered['order_status'].isin(['processing', 'shipped', 'delivered'])]['order_id'].nunique()
    delivered_orders = df_filtered[df_filtered['order_status'] == 'delivered']['order_id'].nunique()
    
    funnel_data = dict(number=[created_orders, paid_orders, delivered_orders], stage=["Pedidos Criados", "Pedidos Pagos", "Pedidos Entregues"])
    fig_funnel = px.funnel(funnel_data, x='number', y='stage', color_discrete_sequence=[PYTHON_BLUE, PYTHON_YELLOW])
    st.plotly_chart(fig_funnel, use_container_width=True)

with col2, st.container():
    st.markdown("#### ⭐ Distribuição das Notas de Avaliação")
    review_counts = df_filtered['review_score'].value_counts().reset_index().sort_values(by='review_score')
    review_counts.columns = ['Nota', 'Contagem']
    fig_reviews = px.bar(review_counts, x='Nota', y='Contagem', text_auto=True, color_discrete_sequence=[PYTHON_BLUE])
    st.plotly_chart(fig_reviews, use_container_width=True)