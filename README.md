# 📊 Dashboard de Análise de Vendas — Olist

Um **dashboard interativo e completo** para análise do famoso dataset da **Olist**, um dos maiores marketplaces do Brasil.  
Desenvolvido após a **Imersão Dados da Alura**, este projeto aplica conhecimentos de **Python, Análise de Dados, Visualização e Machine Learning** para transformar dados brutos em insights de negócio.

**🔗 Acesse o dashboard:** [dashboardolist-ma6osezh6t8drdkger3nvu.streamlit.app](https://dashboardolist-ma6osezh6t8drdkger3nvu.streamlit.app/)

---

## 🚀 Objetivos do Projeto
- Explorar e visualizar dados de vendas da Olist.
- Identificar padrões de comportamento de clientes e desempenho de produtos.
- Analisar performance geográfica de vendas.
- Utilizar **Machine Learning (Prophet)** para previsão de receita futura.
- Criar uma **aplicação web de Business Intelligence** interativa e acessível.

---

## ✨ Funcionalidades

O dashboard é dividido em **4 seções principais**:

1. **📈 Visão Geral**  
   - KPIs: receita total, número de pedidos e clientes únicos.  
   - Evolução mensal da receita.  
   - Ranking das categorias mais vendidas.

2. **🗺️ Análise Geográfica**  
   - Mapa interativo por estado.  
   - Métricas: Receita Total, Ticket Médio e Nº de Pedidos.  
   - Ranking dos Top 5 estados.

3. **👥 Análise de Clientes**  
   - Funil de vendas: pedido → entrega.  
   - Distribuição das notas de avaliação (reviews).

4. **🤖 Previsão de Vendas (IA)**  
   - Modelo de forecasting com **Prophet (Meta)**.  
   - Projeção da receita para os próximos 12 meses.

---

## 📷 Prévia do Projeto

| Tela Principal | Previsão de Vendas |
| --- | --- |
| ![Screenshot da Tela Principal](https://i.postimg.cc/cJN5D5QB/image.png) | ![Screenshot da Previsão de Vendas](https://i.postimg.cc/dQX6HxFZ/image.png) |

---

## 🛠️ Tecnologias Utilizadas

- **Python 3**
- **Pandas** — Manipulação e análise de dados  
- **Plotly Express** — Visualizações interativas  
- **Streamlit** — Dashboard web  
- **Streamlit Option Menu** — Navegação customizada  
- **Prophet (Meta)** — Previsão de séries temporais  
- **CSS Customizado** — Tema escuro e visual profissional  

---

## ⚙️ Como Executar Localmente

```bash
# 1. Clone o repositório
git clone https://github.com/IsaqueCodeX/Dashboard_olist.git
cd Dashboard_olist

# 2. Crie e ative o ambiente virtual
python -m venv venv
# Windows
.env\Scriptsctivate
# macOS / Linux
source venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute a aplicação
streamlit run app.py
```
> Certifique-se de que todos os arquivos de dados (`.csv` e `br_states.json`) estejam na mesma pasta que o `app.py`.

---

## 🙏 Agradecimentos

Agradecimentos à **Alura** pela excelente **Imersão de Dados com Python**, que inspirou e forneceu a base para o desenvolvimento deste projeto.  

---

## 📌 Próximos Passos
- Adicionar filtros dinâmicos por período e categoria.  
- Incluir análise de correlação entre variáveis.  
- Melhorar a responsividade para dispositivos móveis.  

---

Se você gostou do projeto, ⭐ **star no repositório** e contribua! 🚀
