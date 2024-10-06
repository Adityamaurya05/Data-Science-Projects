import streamlit as st

st.title(" Power BI DashBoard")

st.image("Dashboard Image.png")
st.markdown("---") # Horizontal rule
st.markdown("[Source Code](https://github.com/Adityamaurya05/Data-Science-Projects/tree/main/Earthquake%20Forecasting)") #link
st.markdown("---") # Horizontal rule
st.markdown("""
- **Title:** Title name given to the earthquake
- **Magnitude:** The magnitude of the earthquake
- **Date & Time:** Date and time of the event
- **CDI:** The maximum reported intensity for the event range
- **MMI:** The maximum estimated instrumental intensity for the event
- **Alert:** The alert level - “green”, “yellow”, “orange”, and “red”
- **Tsunami:** 1 for events in oceanic regions and 0 otherwise
- **SIG:** A number describing how significant the event is. Larger numbers indicate a more significant event. This value is determined by a number of factors, including magnitude, maximum MMI, felt reports, and estimated impact
- **Net:** The ID of a data contributor. Identifies the network considered to be the preferred source of information for this event
- **NST:** The total number of seismic stations used to determine earthquake location
- **Dmin:** Horizontal distance from the epicenter to the nearest station
- **Gap:** The largest azimuthal gap between azimuthally adjacent stations (in degrees). In general, the smaller this number, the more reliable is the calculated horizontal position of the earthquake. Earthquake locations in which the azimuthal gap exceeds 180 degrees typically have large location and depth uncertainties
- **MagType:** The method or algorithm used to calculate the preferred magnitude for the event
- **Depth:** The depth where the earthquake begins to rupture
- **Latitude / Longitude:** Coordinate system by means of which the position or location of any place on Earth's surface can be determined and described
- **Depth:** The depth where the earthquake begins to rupture
""")
