# 🏡 PriceMyHouse - House Price Prediction System - India

## 📌 Overview
This machine learning system predicts house prices across India based on key property features like size, location, amenities, and construction quality. It helps buyers, sellers, and real estate professionals estimate property values accurately.

## 🌟 Why This Project Matters
For Home Buyers:
- Get fair price estimates before purchasing
- Compare properties objectively
- Avoid overpaying for homes

For Sellers:
- Price your property competitively
- Understand key value factors
- Get data-driven valuation

For Agents/Investors:
- Quick property valuation too
- Market trend analysis
- Investment decision support

## 📂 Dataset Information
The model uses comprehensive Indian housing data including:

- Property size (living area, lot area)
- Room counts (bedrooms, bathrooms)
- Location details (postal code, coordinates)
- Quality metrics (construction grade, condition)
- Neighborhood factors (schools, airport distance)

## 🛠️ How to Use This System
Prerequisites
- Python 3.7+ installed
- Basic terminal/command prompt knowledge

## Step-by-Step Setup
1. Clone the repository:

```
git clone https://github.com/Adityamaurya05/PriceMyHouse-prediction-system.git](https://github.com/Adityamaurya05/Data-Science-Projects/tree/main/PriceMyHouse%20-%20Prediction%20system
cd PriceMyHouse-prediction-system
```
2. Set up virtual environment (recommended):

```
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```
3. Install requirements:

```
pip install -r requirements.txt
```
4. Run the application:
```
streamlit run app.py
```
5. Access the app:

- The app will automatically open in your browser
- If not, visit http://localhost:8501

## 🖥️ Using the Web Interface
1. Enter Property Details:

- Fill in basic information like living area, bedrooms, bathrooms
- Use sliders for number inputs

2. Set Quality Parameters:

- Select construction grade (1-13 scale)
- Choose property condition (1-5 scale)
- Enter year built

3. Add Location Info:

- Select postal code
- Enter latitude/longitude (or use map picker)
- Add neighborhood details

4. Get Prediction:

- Click "Predict Price" button
- View estimated value in ₹ and lakhs
- See which factors most affect the price

## 🕒 When to Use This Tool
### Best Use Cases:
- ✅ Before buying/selling property
- ✅ When evaluating investment properties
- ✅ For market research and analysis
- ✅ To check fairness of listed prices

### Limitations:
- ❌ Not for commercial properties
- ❌ Accuracy varies by region
- ❌ Doesn't account for interior decor

## 🔍 How It Works (Technical)
1. Machine Learning Model:

- Uses Random Forest algorithm
- Trained on thousands of property records
- Considers 15+ important features

2. Data Processing:

- Handles missing values automatically
- Normalizes different measurement units
- Encodes categorical data properly

3. Prediction Engine:

- Takes your inputs
- Compares with similar properties
- Calculates most probable price

## 📊 Sample Inputs for Testing
| Living Area | Bedrooms | Bathrooms | Grade | Predicted Price Range  |
|-------------|----------|-----------|-------|------------------------|
| 1200 sqft   | 2        | 2         | 7     | ₹45-55 lakhs           |
| 1800 sqft   | 3        | 3         | 9     | ₹85-95 lakhs           |
| 3000 sqft   | 4        | 4         | 11    | ₹1.8-2.2 crore         |

## ❓ Frequently Asked Questions
Q: How accurate are the predictions?  
A: The model achieves ~85% accuracy based on historical data, but actual prices may vary by 5-10%.

Q: Can I use this for any Indian city?
A: Yes, but accuracy is best for cities with sufficient training data.

Q: Do I need to know technical details to use this?
A: No! The web interface is simple and guides you through each step.

Q: How often is the model updated?
A: We recommend retraining with new data every 6 months for best results.

## 📜 License
This project is open-source under the MIT License. Feel free to use and modify it for your needs.

## 🤝 Contributing
We welcome contributions! Please fork the repository and submit pull requests.
