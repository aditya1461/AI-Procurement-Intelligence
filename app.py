import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from streamlit_lottie import st_lottie

# ================================
# PAGE CONFIG
# ================================
st.set_page_config(page_title="AI Procurement Intelligence", layout="wide")

# ================================
# LOAD DATA
# ================================

@st.cache_data
def load_data():
    url = "https://drive.google.com/uc?export=download&id=1cqOruxB9MAJdKIVWGKKbDaLEl1LQ3hM4"
    return pd.read_csv(url)

df = load_data()

# ================================
# LOTTIE
# ================================
def load_lottie(url):
    return requests.get(url).json()

lottie_ai = load_lottie("https://assets2.lottiefiles.com/packages/lf20_kyu7xb1v.json")

# ================================
# INTENT SYSTEM
# ================================
INTENTS = {
    "spending": ["spend", "cost", "value"],
    "risk": ["risk", "fraud"],
    "supplier": ["supplier", "vendor"],
    "sector": ["sector"],
    "forecast": ["forecast", "trend"]
}

def detect_intents(query):
    q = query.lower()
    return [i for i in INTENTS if any(w in q for w in INTENTS[i])] or ["general"]

# ================================
# SIDEBAR
# ================================
st.sidebar.title("AI Procurement System")
page = st.sidebar.radio("Navigation", ["Home", "Chat", "Dashboard", "About"])

# ================================
# HOME
# ================================
if page == "Home":

    col1, col2 = st.columns([2,1])

    with col1:
        st.title("AI Procurement Intelligence System")

        st.markdown("""
        ### 📊 System Capabilities

        #### 1. Spending & Contract Value Analysis
        - Total procurement spend by year, country, sector
        - Average contract values
        - Contract size distribution
        - Top contractors

        #### 2. Supplier / Vendor Analysis
        - Supplier concentration
        - Local vs international suppliers
        - Repeat suppliers
        - Supplier diversity

        #### 3. Procurement Method Analysis
        - Method distribution (ICB, NCB, Direct)
        - Trends over time
        - Value vs method correlation

        #### 4. Sector & Project Analysis
        - Sector-wise investment
        - Project-level spend tracking
        - Country-level activity

        #### 5. Timeline & Efficiency
        - Procurement duration
        - Delays & benchmarks

        #### 6. Geographic Analysis
        - Country-wise procurement
        - Supplier origin analysis

        #### 7. Risk & Compliance
        - High-risk contracts
        - Direct contracting risks
        - Supplier concentration risk

        #### 8. Forecasting
        - Growth trends
        - Future projections
        """)

    with col2:
        st_lottie(lottie_ai, height=300)

# ================================
# CHAT
# ================================
elif page == "Chat":

    st.title("💬 Chat with Procurement Agent")

    st.info("""
    💡 Try:
    - show spending trend  
    - risk analysis  
    - supplier analysis  
    - sector spending  
    - forecast growth  
    """)

    user_input = st.chat_input("Ask your question...")

    if user_input:
        intents = detect_intents(user_input)

        for intent in intents:

            if intent == "spending":
                data = df.groupby('year')['contract_value'].sum().reset_index()
                fig = px.line(data, x='year', y='contract_value',
                              title="Yearly Spending Trend",
                              markers=True)
                st.plotly_chart(fig, use_container_width=True)

            elif intent == "risk":
                risk = df['risk_flag'].mean() * 100
                st.metric("Risk Percentage", f"{risk:.2f}%")

            elif intent == "supplier":
                data = df['supplier_name'].value_counts().head(10).reset_index()
                data.columns = ['supplier', 'count']
                fig = px.bar(data, x='count', y='supplier',
                             orientation='h',
                             title="Top Suppliers")
                st.plotly_chart(fig, use_container_width=True)

            elif intent == "sector":
                data = df.groupby('sector')['contract_value'].sum().reset_index()
                fig = px.bar(data, x='sector', y='contract_value',
                             title="Sector Spending",
                             color='sector')
                st.plotly_chart(fig, use_container_width=True)

            elif intent == "forecast":
                data = df.groupby('year')['contract_value'].sum().reset_index()
                fig = px.line(data, x='year', y='contract_value',
                              title="Forecast Trend",
                              line_shape='spline')
                st.plotly_chart(fig, use_container_width=True)

            else:
                st.write("Try a more specific query")

# ================================
# DASHBOARD
# ================================
elif page == "Dashboard":

    st.title("📊 Advanced Dashboard")

    # 1 Yearly Trend
    yearly = df.groupby('year')['contract_value'].sum().reset_index()
    st.plotly_chart(px.line(yearly, x='year', y='contract_value', title="Yearly Spend", markers=True))

    # 2 Sector
    sector = df.groupby('sector')['contract_value'].sum().reset_index()
    st.plotly_chart(px.bar(sector, x='sector', y='contract_value', title="Sector Spend"))

    # 3 Top Countries
    country = df.groupby('country')['contract_value'].sum().sort_values(ascending=False).head(10).reset_index()
    st.plotly_chart(px.bar(country, x='country', y='contract_value', title="Top Countries"))

    # 4 Procurement Method (FIXED POSITION)
    method = df['procurement_method'].value_counts().reset_index()
    method.columns = ['method', 'count']

    fig = px.pie(
        method,
        names='method',
        values='count',
        title="Procurement Methods Distribution",
        hole=0.4
    )

    fig.update_traces(textinfo='percent+label')

    st.plotly_chart(fig, use_container_width=True)

    # 5 Supplier Distribution
    supplier = df['supplier_country'].value_counts().head(10).reset_index()
    supplier.columns = ['country', 'count']

    st.plotly_chart(px.bar(supplier, x='country', y='count', title="Top Supplier Countries"))

# ================================
# ABOUT
# ================================
elif page == "About":

    st.title("📘 Project Details")

    st.markdown("""
    ## 🔹 Phase 1: Data Pipeline
    - Collected ADB procurement dataset
    - Cleaned messy Excel data
    - Standardized columns
    - Created final CSV

    ## 🔹 Phase 2: Analytics Engine
    - Built functions for:
        - Spending
        - Supplier
        - Sector
        - Risk
        - Forecast

    ## 🔹 Phase 3: Agent System
    - Developed NLP-based intent detection
    - Multi-intent handling
    - Automated analysis routing

    ## 🔹 Phase 4: Streamlit UI
    - Interactive dashboard
    - Chat-based interface
    - Real-time insights

    ## 🚀 Technologies Used
    - Python
    - Pandas
    - Plotly
    - Streamlit

    ## 🎯 Goal
    To build an intelligent procurement decision system.

    ## 👨‍💻 Developed By
    Aditya Nandal
    """)