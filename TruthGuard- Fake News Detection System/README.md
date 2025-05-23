# 📰 TrustGuard: AI-Powered Fake News Detection System
## 🌟 Overview
TrustGuard is an intelligent tool that helps you verify whether a news article is real or fake using artificial intelligence. In today's world of misinformation, this app acts as your digital truth-checker, analyzing news content and providing confidence scores for its authenticity.


## 🚀 Why This Matters
- 1 in 3 people encounter fake news weekly (Reuters Institute)
- 60% of shared fake news is spread unintentionally
- Protect yourself and others from misinformation
- Make informed decisions about what to trust online

## 🛠️ How It Works
### 🔍 The Technology Behind It
- Text Analysis: Breaks down news articles word-by-word
- AI Model: Uses machine learning trained on thousands of real/fake news examples
- Database: Stores results to improve future accuracy
- Verification: Allows user feedback to make the system smarter

## ⚙️ Technical Components

| Component               | Technology Used          | Purpose                                                                 |
|-------------------------|--------------------------|-------------------------------------------------------------------------|
| **Machine Learning Model** | Scikit-learn (TF-IDF + PassiveAggressiveClassifier) | Analyzes linguistic patterns, word choices, and writing styles to identify potential fake news |
| **PostgreSQL Database**   | PostgreSQL 14+           | Stores all predictions with timestamps, confidence scores, and user feedback for model retraining |
| **Streamlit Interface**   | Streamlit 1.22+          | Creates an intuitive web app that requires no coding knowledge to operate |

## 🖥️ How to Use TrustGuard
### 🏁 Getting Started
1. Install requirements:
```
pip install -r requirements.txt
```
2. Set up database:
```
python scripts/setup_database.py
```
3. Run the app:
```
streamlit run src/app/main.py
```
## 🔎 Using the Application
- Paste news text or enter a URL
- Click "Predict" button
- Review the AI's analysis
- Provide feedback on accuracy


## 📊 Understanding Results

| Result Icon | Meaning |
|-------------|---------|
| ✅ **REAL** | The news is likely authentic (high confidence) |
| ❌ **FAKE** | The news appears suspicious or fabricated |
| **Confidence %** | How certain the AI is about its prediction (higher % = more confident) |

---

## 👍 Best Practices

### Do:
✔ **Verify from multiple sources** - Cross-check important news with other reliable outlets  
✔ **Report incorrect predictions** - Help improve the system's accuracy  
✔ **Check confidence percentage** - Higher % means more reliable results  
✔ **Share responsibly** - Only share verified information  

### Don't:
✖ **Don't rely solely on this tool** - Always use human judgment for critical decisions  
✖ **Don't use for medical/legal advice** - Consult professionals for important matters  
✖ **Don't assume 100% accuracy** - AI systems have limitations and can make mistakes  

---

## 🛡️ Privacy & Security

- 🔒 **Temporary storage** - Analyzed texts are stored only to improve the system  
- 👤 **No personal data** - We never collect or store your personal information  
- 🔐 **Secure connections** - All database communications are encrypted  
- 📜 **Transparent code** - Open-source allows anyone to inspect how it works  

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. 🐛 **Report bugs** - Help us identify issues  
2. 💡 **Suggest improvements** - Share your ideas for new features  
3. 💻 **Contribute code** - Submit pull requests via GitHub  
4. 🧠 **Help train models** - Contribute to our training datasets  


## 📜 License

**MIT License**  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for full details.

### Key Permissions:
✅ Commercial use  
✅ Modification  
✅ Distribution  
✅ Private use  

### Requirements:
ℹ️ Include original license/copyright notice  

### Limitations:
❌ No liability  
❌ No warranty  
