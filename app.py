# app.py - Versão Final Definitiva

import streamlit as st
import pandas as pd
import plotly.express as px
import os
import json
from streamlit_option_menu import option_menu
from prophet import Prophet

# --- Configuração da Página ---
st.set_page_config(page_title="Dashboard de Vendas Olist", page_icon="🐍", layout="wide")

# --- Carregamento do CSS Customizado ---
def load_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Arquivo CSS '{file_name}' não foi encontrado.")
        st.stop()

# --- Carregamento e Processamento de Dados ---
@st.cache_data
def load_data():
    data_dir = '.'
    files = {
        'orders': 'olist_orders_dataset.csv', 'order_items': 'olist_order_items_dataset.csv',
        'products': 'olist_products_dataset.csv', 'customers': 'olist_customers_dataset.csv',
        'order_reviews': 'olist_order_reviews_dataset.csv', 'payments': 'olist_order_payments_dataset.csv',
        'category_translation': 'product_category_name_translation.csv'
    }
    dfs = {}
    for name, filename in files.items():
        try:
            dfs[name] = pd.read_csv(os.path.join(data_dir, filename))
        except FileNotFoundError:
            st.error(f"Erro: O arquivo de dados '{filename}' não foi encontrado.")
            st.stop()
    df = dfs['orders'].merge(dfs['order_reviews'], on='order_id', how='left')
    df = df.merge(dfs['order_items'], on='order_id', how='left')
    df = df.merge(dfs['products'], on='product_id', how='left')
    df = df.merge(dfs['customers'], on='customer_id', how='left')
    df = df.merge(dfs['payments'], on='order_id', how='left')
    df = df.merge(dfs['category_translation'], on='product_category_name', how='left')
    df.dropna(subset=['order_purchase_timestamp'], inplace=True)
    
    date_cols = [col for col in df.columns if 'timestamp' in col or '_date' in col]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')

    # Lógica para atualizar as datas para o período atual
    max_original_date = df['order_purchase_timestamp'].max()
    current_date = pd.Timestamp.now()
    time_diff = current_date - max_original_date
    for col in date_cols:
        df[col] = df[col] + time_diff
    
    df['categoria_pt'] = df['product_category_name'].str.replace('_', ' ').str.title()
    return df

# --- Inicialização ---
load_css("style.css")
df = load_data()
PYTHON_BLUE = "#3776AB"
PYTHON_YELLOW = "#FFD43B"

# --- Cabeçalho ---
st.title("🐍 Análise de Vendas Olist")
st.markdown("<p>Dashboard interativo para exploração e previsão de dados do marketplace Olist.</p>", unsafe_allow_html=True)
st.markdown("---")


# --- Painel de Filtros Principal (Sempre Visível) ---
with st.container(border=True):
    st.markdown("#### Painel de Filtros")
    col1, col2 = st.columns([1, 2])
    with col1:
        # Datas padrão: Últimos 12 meses a partir da nova data máxima (hoje)
        max_date = df['order_purchase_timestamp'].max()
        default_start_date = max_date - pd.DateOffset(months=12)
        start_date = st.date_input("Data de Início", value=default_start_date, min_value=df['order_purchase_timestamp'].min().date(), max_value=max_date.date())
        end_date = st.date_input("Data de Fim", value=max_date, min_value=df['order_purchase_timestamp'].min().date(), max_value=max_date.date())
    with col2:
        all_states = sorted(df['customer_state'].unique())
        selected_states = st.multiselect("Selecione os Estados", all_states, default=['SP', 'RJ', 'MG'])

# --- Aplicação dos Filtros ---
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)
df_filtered = df[
    (df['order_purchase_timestamp'] >= start_date) & 
    (df['order_purchase_timestamp'] <= end_date) &
    (df['customer_state'].isin(selected_states))
]
st.markdown("---")

# --- Navegação entre Páginas ---
selected_page = option_menu(
    menu_title=None,
    options=["Visão Geral", "Análise Geográfica", "Análise de Clientes", "Previsão de Vendas"],
    icons=["bar-chart-line", "map-fill", "people-fill", "graph-up-arrow"],
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#0E1117"},
        "icon": {"color": "#FAFAFA", "font-size": "20px"},
        "nav-link": {"font-size": "16px", "text-align": "center", "margin":"0px", "color": "#FAFAFA"},
        "nav-link-selected": {"background-color": PYTHON_BLUE},
    }
)
st.markdown("---")

# --- Página 1: Visão Geral ---
if selected_page == "Visão Geral":
    st.markdown("### KPIs e Desempenho de Vendas")
    col1, col2, col3 = st.columns(3)
    col1.metric("Receita Total", f"R$ {df_filtered['payment_value'].sum():,.2f}")
    col2.metric("Pedidos Totais", f"{df_filtered['order_id'].nunique():,}")
    col3.metric("Clientes Únicos", f"{df_filtered['customer_unique_id'].nunique():,}")
    st.markdown("<br>", unsafe_allow_html=True)
    col_charts1, col_charts2 = st.columns(2)
    with col_charts1, st.container():
        df_revenue_time = df_filtered.set_index('order_purchase_timestamp').groupby(pd.Grouper(freq='M'))['payment_value'].sum().reset_index()
        fig_line = px.line(df_revenue_time, x='order_purchase_timestamp', y='payment_value', title="📈 Evolução da Receita", template="plotly_dark", color_discrete_sequence=[PYTHON_YELLOW])
        fig_line.update_layout(paper_bgcolor="#1C1C1E", plot_bgcolor="#1C1C1E")
        st.plotly_chart(fig_line, use_container_width=True)
    with col_charts2, st.container():
        top_categories = df_filtered['categoria_pt'].value_counts().nlargest(10).reset_index()
        top_categories.columns = ['Categoria', 'Pedidos']
        fig_bar = px.bar(top_categories, x='Pedidos', y='Categoria', orientation='h', title="📦 Top 10 Categorias", template="plotly_dark", color_discrete_sequence=[PYTHON_YELLOW])
        fig_bar.update_layout(yaxis={'categoryorder':'total ascending'}, paper_bgcolor="#1C1C1E", plot_bgcolor="#1C1C1E")
        st.plotly_chart(fig_bar, use_container_width=True)

# --- Página 2: Análise Geográfica ---
if selected_page == "Análise Geográfica":
    st.markdown("### 🌎 Central de Análise Geográfica")
    metric_options = {'Receita Total': 'payment_value_sum', 'Ticket Médio': 'ticket_medio', 'Número de Pedidos': 'order_count'}
    selected_metric_label = st.selectbox("Selecione uma métrica para analisar:", options=list(metric_options.keys()))
    selected_metric_col = metric_options[selected_metric_label]
    state_stats = df_filtered.groupby('customer_state', as_index=False).agg(payment_value_sum=('payment_value', 'sum'), order_count=('order_id', 'nunique'))
    state_stats['ticket_medio'] = state_stats['payment_value_sum'] / state_stats['order_count']
    state_stats = state_stats.sort_values(by=selected_metric_col, ascending=False)
    col1, col2 = st.columns(2)
    with col1, st.container():
        st.markdown(f"#### 🗺️ Mapa de {selected_metric_label}")
        try:
            with open("br_states.json") as f:
                geojson_data = json.load(f)
            fig_map = px.choropleth(state_stats, geojson=geojson_data, locations='customer_state', featureidkey="properties.sigla", color=selected_metric_col, color_continuous_scale="Viridis", hover_name='customer_state', hover_data={'customer_state': False, selected_metric_col: ':.2f'}, title=f"Mapa de {selected_metric_label}", template="plotly_dark")
            fig_map.update_layout(paper_bgcolor="#1C1C1E", geo_bgcolor="#1C1C1E")
            fig_map.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig_map, use_container_width=True)
        except FileNotFoundError:
            st.error("Arquivo 'br_states.json' não encontrado.")
    with col2, st.container():
        st.markdown(f"#### 🏆 Top 5 Estados por {selected_metric_label}")
        top_5_states = state_stats.head(5)
        fig_bar_states = px.bar(top_5_states, x=selected_metric_col, y='customer_state', orientation='h', text_auto='.2s', title=f"Top 5 Estados por {selected_metric_label}", template="plotly_dark", color_discrete_sequence=[PYTHON_YELLOW])
        fig_bar_states.update_layout(xaxis_title=selected_metric_label, yaxis_title="Estado", showlegend=False, yaxis={'categoryorder':'total ascending'}, paper_bgcolor="#1C1C1E", plot_bgcolor="#1C1C1E")
        st.plotly_chart(fig_bar_states, use_container_width=True)

# --- Página 3: Análise de Clientes ---
if selected_page == "Análise de Clientes":
    st.markdown("### Funil de Vendas e Satisfação do Cliente")
    col1, col2 = st.columns(2)
    with col1, st.container():
        st.markdown("#### 🔻 Funil de Vendas")
        created_orders = df_filtered['order_id'].nunique()
        paid_orders = df_filtered[df_filtered['order_status'].isin(['processing', 'shipped', 'delivered'])]['order_id'].nunique()
        delivered_orders = df_filtered[df_filtered['order_status'] == 'delivered']['order_id'].nunique()
        funnel_data = dict(number=[created_orders, paid_orders, delivered_orders], stage=["Pedidos Criados", "Pedidos Pagos", "Pedidos Entregues"])
        fig_funnel = px.funnel(funnel_data, x='number', y='stage', title="Funil de Vendas", template="plotly_dark", color_discrete_sequence=[PYTHON_YELLOW])
        fig_funnel.update_layout(paper_bgcolor="#1C1C1E", plot_bgcolor="#1C1C1E")
        st.plotly_chart(fig_funnel, use_container_width=True)
    with col2, st.container():
        st.markdown("#### ⭐ Distribuição das Notas de Avaliação")
        review_counts = df_filtered['review_score'].value_counts().reset_index().sort_values(by='review_score')
        review_counts.columns = ['Nota', 'Contagem']
        fig_reviews = px.bar(review_counts, x='Nota', y='Contagem', text_auto=True, title="Distribuição das Notas de Avaliação", template="plotly_dark", color_discrete_sequence=[PYTHON_YELLOW])
        fig_reviews.update_layout(paper_bgcolor="#1C1C1E", plot_bgcolor="#1C1C1E")
        st.plotly_chart(fig_reviews, use_container_width=True)

# --- Página 4: Previsão de Vendas ---
if selected_page == "Previsão de Vendas":
    st.markdown("### 🤖 IA: Previsão de Receita Futura")
    with st.container():
        st.info("Esta análise utiliza o modelo Prophet para prever a receita total para os próximos 12 meses, com base em todo o histórico de vendas.")
        df_prophet = df.set_index('order_purchase_timestamp').groupby(pd.Grouper(freq='D'))['payment_value'].sum().reset_index()
        df_prophet.columns = ['ds', 'y']
        model = Prophet()
        model.fit(df_prophet)
        future = model.make_future_dataframe(periods=365)
        forecast = model.predict(future)
        fig_forecast = model.plot(forecast, xlabel='Data', ylabel='Receita (R$)')
        ax = fig_forecast.gca()
        ax.set_title("Previsão de Receita para os Próximos 12 Meses", size=18)
        ax.set_xlabel("Data", size=12)
        ax.set_ylabel("Receita (R$)", size=12)
        st.pyplot(fig_forecast, use_container_width=True)
        with st.expander("Ver dados da previsão"):
            st.dataframe(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(365))