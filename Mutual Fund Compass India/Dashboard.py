import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page configuration
st.set_page_config(page_title="Mutual Fund Compass India", layout="wide")

# Title
st.title("Mutual Fund Compass India")

# Load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv("comprehensive_mutual_funds_data.csv")
    # Replace empty strings or '-' with NaN
    df.replace(['', '-'], pd.NA, inplace=True)
    # Convert numeric columns to float where applicable
    numeric_cols = ['min_sip', 'min_lumpsum', 'expense_ratio', 'fund_size_cr', 'fund_age_yr',
                    'sortino', 'alpha', 'sd', 'beta', 'sharpe', 'risk_level', 'rating',
                    'returns_1yr', 'returns_3yr', 'returns_5yr']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
category_filter = st.sidebar.multiselect("Category", options=df['category'].unique(), default=df['category'].unique())
amc_filter = st.sidebar.multiselect("AMC Name", options=df['amc_name'].unique(), default=df['amc_name'].unique())
risk_level_filter = st.sidebar.slider("Risk Level", int(df['risk_level'].min()), int(df['risk_level'].max()), (int(df['risk_level'].min()), int(df['risk_level'].max())))
rating_filter = st.sidebar.slider("Rating", int(df['rating'].min()), int(df['rating'].max()), (int(df['rating'].min()), int(df['rating'].max())))

# Apply filters
filtered_df = df[
    (df['category'].isin(category_filter)) &
    (df['amc_name'].isin(amc_filter)) &
    (df['risk_level'].between(risk_level_filter[0], risk_level_filter[1])) &
    (df['rating'].between(rating_filter[0], rating_filter[1]))
]

# Function to calculate future value
def calculate_future_value(principal, rate, years):
    if pd.isna(rate):
        return None
    return principal * (1 + rate / 100) ** years

# Tabs for different sections
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Overview", "Performance", "Risk Analysis", "Fund Details", "Investment Calculator"])

# Tab 1: Overview
with tab1:
    st.subheader("Dataset Overview")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Funds", len(filtered_df))
    with col2:
        st.metric("Avg Fund Size (Cr)", f"{filtered_df['fund_size_cr'].mean():.2f}")
    with col3:
        st.metric("Avg Expense Ratio", f"{filtered_df['expense_ratio'].mean():.2f}%")
    with col4:
        st.metric("Avg Fund Age (Years)", f"{filtered_df['fund_age_yr'].mean():.2f}")

    # Category Distribution
    fig_category = px.pie(filtered_df, names='category', title="Fund Distribution by Category")
    st.plotly_chart(fig_category, use_container_width=True)

    # AMC Distribution
    fig_amc = px.histogram(filtered_df, x='amc_name', title="Funds by AMC", nbins=len(df['amc_name'].unique()))
    fig_amc.update_layout(xaxis={'tickangle': 45})
    st.plotly_chart(fig_amc, use_container_width=True)

# Tab 2: Performance
with tab2:
    st.subheader("Performance Metrics")
    returns_cols = ['returns_1yr', 'returns_3yr', 'returns_5yr']
    fig_returns = make_subplots(rows=1, cols=3, subplot_titles=("1-Year Returns", "3-Year Returns", "5-Year Returns"))
    for i, col in enumerate(returns_cols, 1):
        fig_returns.add_trace(
            go.Box(y=filtered_df[col], name=col.split('_')[1]), row=1, col=i
        )
    fig_returns.update_layout(height=400, title_text="Returns Distribution")
    st.plotly_chart(fig_returns, use_container_width=True)

    # Top Performers
    st.write("Top 10 Funds by 5-Year Returns")
    top_funds = filtered_df.nlargest(10, 'returns_5yr')[['scheme_name', 'returns_5yr', 'category', 'amc_name']]
    st.dataframe(top_funds)

# Tab 3: Risk Analysis
with tab3:
    st.subheader("Risk Analysis")
    col1, col2 = st.columns(2)
    with col1:
        fig_risk = px.scatter(filtered_df, x='sd', y='sharpe', color='risk_level', size='fund_size_cr',
                              hover_data=['scheme_name'], title="Sharpe Ratio vs Standard Deviation")
        st.plotly_chart(fig_risk, use_container_width=True)
    with col2:
        fig_beta = px.box(filtered_df, x='category', y='beta', title="Beta Distribution by Category")
        fig_beta.update_layout(xaxis={'tickangle': 45})
        st.plotly_chart(fig_beta, use_container_width=True)

    # Risk Level Distribution
    fig_risk_level = px.histogram(filtered_df, x='risk_level', title="Funds by Risk Level")
    st.plotly_chart(fig_risk_level, use_container_width=True)

# Tab 4: Fund Details
with tab4:
    st.subheader("Fund Details")
    selected_fund = st.selectbox("Select Fund", filtered_df['scheme_name'].unique())
    fund_data = filtered_df[filtered_df['scheme_name'] == selected_fund].iloc[0]
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Scheme Name:**", fund_data['scheme_name'])
        st.write("**AMC Name:**", fund_data['amc_name'])
        st.write("**Category:**", fund_data['category'])
        st.write("**Sub Category:**", fund_data['sub_category'])
        st.write("**Fund Manager:**", fund_data['fund_manager'])
        st.write("**Fund Age (Years):**", fund_data['fund_age_yr'])
        st.write("**Fund Size (Cr):**", f"{fund_data['fund_size_cr']:.2f}")
    with col2:
        st.write("**Min SIP:**", fund_data['min_sip'])
        st.write("**Min Lumpsum:**", fund_data['min_lumpsum'])
        st.write("**Expense Ratio:**", f"{fund_data['expense_ratio']:.2f}%")
        st.write("**Risk Level:**", fund_data['risk_level'])
        st.write("**Rating:**", fund_data['rating'])
        st.write("**1-Year Return:**", f"{fund_data['returns_1yr']:.2f}%")
        st.write("**3-Year Return:**", f"{fund_data['returns_3yr']:.2f}%")
        st.write("**5-Year Return:**", f"{fund_data['returns_5yr']:.2f}%")
    
    # Risk Metrics
    st.write("**Risk Metrics**")
    fig_risk_metrics = go.Figure(data=[
        go.Bar(name='Sortino', x=['Sortino'], y=[fund_data['sortino']]),
        go.Bar(name='Alpha', x=['Alpha'], y=[fund_data['alpha']]),
        go.Bar(name='Sharpe', x=['Sharpe'], y=[fund_data['sharpe']]),
        go.Bar(name='Beta', x=['Beta'], y=[fund_data['beta']]),
        go.Bar(name='SD', x=['SD'], y=[fund_data['sd']])
    ])
    fig_risk_metrics.update_layout(barmode='group', title="Risk Metrics for Selected Fund")
    st.plotly_chart(fig_risk_metrics, use_container_width=True)

# Tab 5: Investment Calculator
with tab5:
    st.subheader("Investment Calculator")
    calc_fund = st.selectbox("Select Fund for Investment", filtered_df['scheme_name'].unique(), key="calc_fund")
    investment_amount = st.number_input("Enter Investment Amount (₹)", min_value=0.0, value=10000.0, step=1000.0)
    time_period = st.selectbox("Select Time Period", ["1 Year", "3 Years", "5 Years"])

    fund_data_calc = filtered_df[filtered_df['scheme_name'] == calc_fund].iloc[0]
    returns_dict = {
        "1 Year": fund_data_calc['returns_1yr'],
        "3 Years": fund_data_calc['returns_3yr'],
        "5 Years": fund_data_calc['returns_5yr']
    }

    if st.button("Calculate Future Value"):
        years = {"1 Year": 1, "3 Years": 3, "5 Years": 5}[time_period]
        rate = returns_dict[time_period]
        future_value = calculate_future_value(investment_amount, rate, years)

        if future_value is not None:
            st.success(f"If you invest ₹{investment_amount:,.2f} in {calc_fund}:")
            st.write(f"**After {time_period}: ₹{future_value:,.2f}**")
            st.write(f"**Expected Annual Return:** {rate:.2f}%")
            st.write(f"**Total Growth:** ₹{(future_value - investment_amount):,.2f} ({((future_value - investment_amount) / investment_amount * 100):.2f}%)")
        else:
            st.warning(f"Return data for {time_period} is not available for {calc_fund}.")

        # Visualization
        fig_calc = go.Figure()
        fig_calc.add_trace(go.Bar(x=['Initial Investment', f'After {time_period}'], 
                                  y=[investment_amount, future_value if future_value else 0],
                                  text=[f"₹{investment_amount:,.2f}", f"₹{future_value:,.2f}" if future_value else "N/A"],
                                  textposition='auto'))
        fig_calc.update_layout(title=f"Investment Growth for {calc_fund}", yaxis_title="Amount (₹)")
        st.plotly_chart(fig_calc, use_container_width=True)

# Raw Data
st.subheader("Raw Data")
if st.checkbox("Show Raw Data"):
    st.dataframe(filtered_df)

