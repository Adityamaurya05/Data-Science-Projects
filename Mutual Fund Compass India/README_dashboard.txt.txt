Mutual Fund Compass India

Overview
This project provides a comprehensive analysis of mutual funds available in India, designed to assist investors in making informed decisions based on their age, financial goals, and risk appetite. It includes detailed information on types of mutual funds, risk profiles, age-based investment strategies, tax implications, and evaluation metrics. The project also features an interactive Streamlit dashboard built using a dataset of Indian mutual funds, offering visualizations and an investment calculator to estimate future returns.

Table of Contents
- Introduction
- Features
- Dataset
- Installation
- Usage
- Project Structure
- Evaluation Metrics
- Tax Implications
- Resources
- Contributing
- License

Introduction
Mutual funds are a popular investment vehicle in India, pooling money from multiple investors to invest in diversified portfolios managed by professionals. This project aims to guide investors—whether beginners or experienced—through the landscape of mutual funds by offering insights into types of mutual funds, age-based investment recommendations, risk profiles and strategies, tax implications, and tools to evaluate and select funds. The accompanying Streamlit dashboard enhances this analysis with interactive visualizations and an investment calculator based on real mutual fund data.

Features
- Detailed Guide: Explanation of mutual fund types, risk profiles, and investment strategies tailored to different age groups.
- Streamlit Dashboard:
  - Overview of fund categories and AMC distribution
  - Performance analysis (1-yr, 3-yr, 5-yr returns)
  - Risk analysis (Sharpe Ratio, Beta, etc.)
  - Detailed fund insights
  - Investment calculator to estimate future value
- Tax Information: Overview of tax rules for mutual funds in India.
- Evaluation Metrics: Key metrics like CAGR, Sharpe Ratio, Alpha, Beta, and Standard Deviation.

Dataset
The project includes a dataset (mutual_funds.csv) with details of various mutual funds in India, including:
- Scheme Name
- Minimum SIP/Lumpsum
- Expense Ratio
- Fund Size (Cr)
- Fund Age (Years)
- Returns (1-yr, 3-yr, 5-yr)
- Risk Metrics (Sortino, Alpha, SD, Beta, Sharpe)
- Risk Level, Rating, Category, Sub-Category, AMC Name
Note: The dataset must be placed in the same directory as the script to run the dashboard.

Installation
To run the project locally, follow these steps:
1. Clone the Repository:
   git clone https://github.com/your-username/mutual-funds-india.git
   cd mutual-funds-india
2. Install Dependencies:
   Ensure you have Python installed, then run:
   pip install -r requirements.txt
   If requirements.txt is not provided, install:
   pip install streamlit pandas plotly
3. Add Dataset: Place mutual_funds.csv in the project directory.

Usage
1. Run the Dashboard:
   streamlit run mutual_fund_dashboard.py
   This will open the dashboard in your default web browser.
2. Explore the Dashboard:
   - Use the sidebar filters to narrow down funds by category, AMC, risk level, or rating.
   - Navigate through tabs: Overview, Performance, Risk Analysis, Fund Details, and Investment Calculator.
   - In the Investment Calculator tab, input an amount and select a fund/time period to estimate future value.
3. Read the Guide: Refer to the project documentation (e.g., this README or a separate text file) for detailed insights.

Project Structure
mutual-funds-india/
|
|-- mutual_fund_dashboard.py  # Streamlit dashboard script
|-- mutual_funds.csv          # Dataset of Indian mutual funds
|-- README_dashboard.txt      # Project documentation (this file)
|-- requirements.txt          # Python dependencies (optional)

Evaluation Metrics
Key metrics for evaluating mutual funds:
- CAGR: Measures annualized growth rate.
- Sharpe Ratio: Indicates risk-adjusted returns.
- Alpha: Excess return over the benchmark.
- Beta: Volatility relative to the market.
- Standard Deviation: Measures fund volatility.

Tax Implications
- Equity Funds:
  - LTCG (> ₹1 lakh) taxed at 10%.
  - STCG taxed at 15%.
- Debt Funds:
  - LTCG taxed at 20% with indexation.
  - STCG taxed per income slab.
- ELSS: Tax deduction under Section 80C up to ₹1.5 lakh.

Resources
- AMFI: https://www.amfiindia.com/ - Association of Mutual Funds in India
- SEBI: https://www.sebi.gov.in/ - Securities and Exchange Board of India
- Moneycontrol - Mutual Funds: https://www.moneycontrol.com/mutualfundindia/
- Morningstar India: https://www.morningstar.in/

Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch (git checkout -b feature-branch).
3. Make your changes and commit (git commit -m "Add feature").
4. Push to the branch (git push origin feature-branch).
5. Open a Pull Request.
Please ensure your code follows PEP 8 guidelines and includes appropriate documentation.

License
This project is licensed under the MIT License. See the LICENSE file for details.