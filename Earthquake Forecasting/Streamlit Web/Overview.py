import streamlit as st

st.write("# Welcome to Earthquake Forecasting")
st.subheader("Stay Safe and Informed ")
st.markdown("---")
st.link_button("Power BI Dashboard", url="/Dashboard")
st.link_button("Earthquake Prediction", url="/Prediction")
st.markdown("---")

st.markdown("""
This is your ultimate companion for earthquake preparedness and safety. Designed to provide real-time alerts, essential information, and life-saving guidance, our app empowers you to be ready for any seismic event. Key Features: 
""")

st.markdown("""
* **Real-Time Earthquake Alerts:** Receive instant notifications about earthquakes happening near you, including magnitude, location, and estimated intensity.
* **Customizable Alerts:** Tailor your alert settings to your specific needs, choosing the magnitude threshold and distance radius.
* **Detailed Earthquake Information:** Access comprehensive data on recent and historical earthquakes worldwide, including location, depth, and magnitude.
* **Interactive Earthquake Map:** Visualize earthquake activity on a live map, with options to filter by magnitude, time, and location.
* **Emergency Preparedness Tips:** Learn how to prepare for an earthquake, create emergency plans, and build an earthquake kit.
* **Earthquake Safety Guidelines:** Get expert advice on what to do before, during, and after an earthquake to protect yourself and your loved ones. 
* **Shake Detector:** Automatically detects strong shaking and provides immediate safety instructions.
* **Community Updates:** Connect with others in your area, share experiences, and receive support.
""")

