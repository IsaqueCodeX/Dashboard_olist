# 📊 Dashboard de Análise de Vendas Olist

## 🚀 Resumo do Projeto

Este projeto é um dashboard interativo e completo para a análise de dados do famoso dataset da Olist, um dos maiores marketplaces do Brasil. Desenvolvido como projeto de estudo após a **Imersão Dados da Alura**, o objetivo foi aplicar e aprofundar conhecimentos em Python para análise de dados, desde a manipulação e limpeza até a criação de uma aplicação web de Business Intelligence com funcionalidades de Machine Learning.

O dashboard permite uma exploração rica e dinâmica dos dados de vendas, clientes, performance geográfica e satisfação, culminando em um modelo de previsão de vendas futuras.

**➡️ Link para o App em funcionamento:** `https://dashboardolist-ma6osezh6t8drdkger3nvu.streamlit.app/`

## ✨ Features Principais

O dashboard é dividido em quatro seções principais, acessíveis por um menu de navegação:

- **Visão Geral:** Apresenta os KPIs (Key Performance Indicators) mais importantes, como receita total, número de pedidos e clientes únicos. Inclui gráficos sobre a evolução da receita mensal e o ranking das categorias de produtos mais vendidas.

- **Análise Geográfica:** Uma central interativa para explorar o desempenho das vendas por todo o Brasil. O usuário pode selecionar diferentes métricas (Receita Total, Ticket Médio, Nº de Pedidos) para visualizar tanto em um mapa coroplético quanto em um gráfico de ranking dos Top 5 estados.

- **Análise de Clientes:** Foco no comportamento e satisfação do consumidor, apresentando um funil de vendas (desde a criação do pedido até a entrega) e um gráfico com a distribuição das notas de avaliação (reviews).

- **🤖 Previsão de Vendas (IA):** O grande diferencial! Utilizando a biblioteca `Prophet` do Meta, esta seção apresenta um modelo de forecasting que prevê a receita total para os próximos 12 meses, com base em todo o histórico de dados.

### Screenshots

|                              Tela Principal                              |                          Previsão de Vendas com IA                           |
| :----------------------------------------------------------------------: | :--------------------------------------------------------------------------: |
| ![Screenshot da Tela Principal](https://i.postimg.cc/cJN5D5QB/image.png) | ![Screenshot da Previsão de Vendas](https://i.postimg.cc/dQX6HxFZ/image.png) |

## 🛠️ Tecnologias Utilizadas

Este projeto foi construído utilizando um ecossistema de ferramentas modernas de Data Science em Python:

- **Linguagem:** Python 3
- **Manipulação de Dados:** Pandas
- **Visualização de Dados:** Plotly Express
- **Dashboard Interativo:** Streamlit
- **Componentes de UI:** Streamlit Option Menu
- **Machine Learning (Forecasting):** Prophet (do Meta)
- **Estilização:** CSS customizado para um tema escuro e profissional.

## ⚙️ Como Executar o Projeto Localmente

Para rodar este projeto na sua máquina, siga os passos abaixo:

1.  **Clone o repositório:**

    ```bash
    git clone [https://github.com/IsaqueCodeX/Dashboard_olist.git](https://github.com/IsaqueCodeX/Dashboard_olist.git)
    cd Dashboard_olist
    ```

2.  **Crie e ative um ambiente virtual:**

    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS / Linux
    source venv/bin/activate
    ```

3.  **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute a aplicação:**
    ```bash
    streamlit run app.py
    ```
    _Certifique-se de que todos os arquivos de dados (`.csv` e `br_states.json`) estão na mesma pasta que o `app.py`._

## 🙏 Agradecimentos

Gostaria de agradecer à **Alura** pela incrível **Imersão Dados**, que foi o ponto de partida e a principal fonte de inspiração para este projeto. O conhecimento adquirido durante o evento foi fundamental para a sua realização.
