# pages/1_Visão_Geral.py

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Visão Geral")

# --- CORES DA PALETA PYTHON ---
PYTHON_BLUE = "#3776AB"
PYTHON_YELLOW = "#FFD43B"

st.markdown("## Visão Geral")
st.markdown("### KPIs e Desempenho de Vendas")

# Acessa o dataframe filtrado que foi salvo no session_state pelo app.py
df_filtered = st.session_state['df_filtered']

# --- KPIs ---
col1, col2, col3 = st.columns(3)
col1.metric("Receita Total", f"R$ {df_filtered['payment_value'].sum():,.2f}")
col2.metric("Pedidos Totais", f"{df_filtered['order_id'].nunique():,}")
col3.metric("Clientes Únicos", f"{df_filtered['customer_unique_id'].nunique():,}")

st.markdown("<br>", unsafe_allow_html=True)

# --- Gráficos ---
col_charts1, col_charts2 = st.columns(2)
with col_charts1, st.container():
    st.markdown("#### 📈 Evolução da Receita")
    df_revenue_time = df_filtered.set_index('order_purchase_timestamp').groupby(pd.Grouper(freq='M'))['payment_value'].sum().reset_index()
    fig_line = px.line(df_revenue_time, x='order_purchase_timestamp', y='payment_value', color_discrete_sequence=[PYTHON_YELLOW])
    st.plotly_chart(fig_line, use_container_width=True)

with col_charts2, st.container():
    st.markdown("#### 📦 Top 10 Categorias")
    top_categories = df_filtered['categoria_pt'].value_counts().nlargest(10).reset_index()
    top_categories.columns = ['Categoria', 'Pedidos']
    fig_bar = px.bar(top_categories, x='Pedidos', y='Categoria', orientation='h', color_discrete_sequence=[PYTHON_BLUE])
    fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_bar, use_container_width=True)