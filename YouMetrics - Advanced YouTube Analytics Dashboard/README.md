# 📊 YouMetrics - Advanced YouTube Analytics Dashboard



## 🌟 Overview

The **Advanced YouTube Analytics Dashboard** is a powerful Streamlit application that provides deep insights into YouTube trending videos. This tool helps content creators, marketers, and analysts understand video performance patterns, optimize content strategy, and track competitors through interactive visualizations and machine learning insights.

## 🚀 Why This Project Matters

- **For Content Creators**: Understand what makes videos trend  
- **For Marketers**: Identify high-performing content in your niche  
- **For Analysts**: Study engagement patterns and viewer behavior  
- **For Researchers**: Access structured YouTube data for academic studies  

## 🔑 Key Features

- 📈 Interactive visualizations with Plotly  
- 🔍 Sentiment analysis on video titles  
- ⏱ Optimal posting time recommendations  
- 📊 Channel performance benchmarking  
- 📱 Mobile-responsive design  
- 📥 PDF/Excel report generation  

## 🛠 Project Structure
```
youtube-analytics/
├── main.py # Main application
├── utils/
│ ├── data_processor.py # Data cleaning & transformation
│ ├── api_handler.py # YouTube API interactions
│ └── visualizations.py # Plotting functions
├── assets/
│ └── styles.css # Custom styling
├── requirements.txt # Dependencies
└── README.md # This file
```

## 🏁 Getting Started

### Prerequisites

- Python 3.8+  
- YouTube API key (free tier available)  

### 🔑 How to Get YouTube API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)  
2. Create a new project  
3. Enable "YouTube Data API v3"  
4. Create credentials → API key  
5. Restrict key to YouTube Data API only  

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/youtube-analytics.git
cd youtube-analytics
```
2. Install dependencies:

```
pip install -r requirements.txt
```

3. Create .env file:
```
Create .env file:
```
4. 🚦 Running the Application
```
streamlit run main.py
```

### 🎮 How to Use

1. **Enter your API key** in the sidebar

2. **Adjust parameters**:
   - Select region (US, IN, GB, etc.)
   - Choose number of videos (10–100)
   - Set minimum views filter

3. **Explore tabs**:
   - 📈 **Trends**: View growth patterns
   - 📊 **Distributions**: See statistical spreads
   - 📌 **Engagement**: Analyze interaction metrics
   - ☁️ **Content**: Examine textual patterns

4. **Generate reports**:
   - Click **"Export PDF"** or **"Export Excel"** buttons

---

### 🧠 Advanced Features

#### 💬 Sentiment Analysis

The dashboard automatically analyzes:
- Title positivity/negativity  
- Emotional tone of descriptions  
- Most common emotional words

#### 🕒 Optimal Posting Times

The heatmap shows:
- Best hours for engagement  
- Weekly patterns  
- Duration vs. engagement correlations  

---

### 🤝 Contributing

We welcome contributions! Please:

1. **Fork** the project  
2. **Create** your feature branch  
3. **Commit** your changes  
4. **Push** to the branch  
5. **Open** a pull request  

### 📜 License

MIT License – see [LICENSE](LICENSE) file for details

---

### 📧 Contact

For questions or suggestions:  
[adityamauryastudywork@gmail.com](mailto:adityamauryastudywork@gmail.com)

---

✨ **Happy Analyzing!** ✨

