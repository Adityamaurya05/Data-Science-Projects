import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="NutriDash-Nutrition based Dashboard", layout="wide")

# Load the local CSV file
@st.cache_data
def load_data():
    try:
        csv_path = r"daily_food_nutrition_dataset.csv"
        df = pd.read_csv(csv_path)
        return df
    except FileNotFoundError:
        st.error("CSV file not found. Please check the file path and ensure the file exists.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading the CSV file: {str(e)}")
        return pd.DataFrame()

# Load the data
df = load_data()

# If the dataset is empty or not loaded, show an error and exit
if df.empty:
    st.error("Failed to load the dataset. Please ensure the CSV file exists and is accessible.")
    st.stop()

# Title of the dashboard
st.title("NutriDash - Nutrition based Dashboard")

# Create tabs
tab_titles = ["Food Item Analysis", "Meal Consumption Analysis", "Meal Planning", "Protein Calculator"]
tabs = st.tabs(tab_titles)

# 1st Tab: Food Item Analysis
with tabs[0]:
    st.subheader("Select a Food Item to Analyze")
    
    # Dropdown for food items
    if 'Food_Item' in df.columns:
        unique_food_items = df['Food_Item'].unique()
        selected_food = st.selectbox("Select a Food Item", unique_food_items)
        
        # Filter data for the selected food item
        food_data = df[df['Food_Item'] == selected_food].iloc[0]  # Take the first occurrence if duplicates exist
        
        # Use columns for layout: left for text, right for graph
        col1, col2 = st.columns([2, 1])  # 2 parts for text, 1 part for graph (right side)
        
        with col1:
            # Display food category and nutritional values
            st.write("**Category:**", food_data['Category'] if pd.notna(food_data['Category']) else 'N/A')
            st.write("**Nutritional Values:**")
            nutritional_cols = ['Calories (kcal)', 'Protein (g)', 'Carbohydrates (g)', 'Fat (g)', 'Fiber (g)', 'Sugars (g)', 'Sodium (mg)', 'Cholesterol (mg)', 'Water_Intake (ml)', 'Meal_Type']
            for col in nutritional_cols:
                if col in df.columns:
                    value = food_data[col] if pd.notna(food_data[col]) else 0  # Use 0 instead of 'N/A' for numeric display
                    if isinstance(value, (int, float)):
                        st.write(f"{col}: {value:.2f}")
                    else:
                        st.write(f"{col}: {value}")
        
        with col2:
            # Create a pie chart (or donut chart) of nutritional values (macros and key nutrients)
            macro_cols = ['Calories (kcal)', 'Protein (g)', 'Carbohydrates (g)', 'Fat (g)', 'Fiber (g)', 'Sugars (g)']
            nutrient_values = {}
            for col in macro_cols:
                if col in df.columns and pd.notna(food_data[col]) and isinstance(food_data[col], (int, float)):
                    nutrient_values[col] = float(food_data[col])  # Include all numeric values, even if zero
            
            if nutrient_values:  # Check if there are any valid nutrient values
                nutrient_df = pd.DataFrame([nutrient_values])
                # Create a donut chart (pie chart with hole), showing actual values in labels
                fig = px.pie(nutrient_df, values=list(nutrient_values.values()), names=list(nutrient_values.keys()), 
                             title=f"Nutritional Breakdown for {selected_food}", hole=0.4)
                fig.update_traces(textposition='inside', textinfo='label+value')  # Show labels and actual values
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No valid numerical macro data available for this food item to display a graph.")
    else:
        st.error("Food_Item column not found in the dataset. Please check your CSV file.")

# 2nd Tab: Meal ConsumptionAnalysis
with tabs[1]:
    st.subheader("What Are You Consuming?")
    
    # Input for food items and quantities
    if 'Food_Item' in df.columns:
        unique_food_items = df['Food_Item'].unique()
        food_inputs = st.multiselect("Select the food items you’re consuming", unique_food_items, default=[])
        quantities = {}
        total_macros = {col: 0 for col in ['Calories (kcal)', 'Protein (g)', 'Carbohydrates (g)', 'Fat (g)', 'Fiber (g)', 'Sugars (g)', 'Sodium (mg)', 'Cholesterol (mg)', 'Water_Intake (ml)']}
        
        for food in food_inputs:
            quantities[food] = st.number_input(f"Enter quantity for {food} (in grams or servings, e.g., 100 for 100g)", min_value=1, value=100, key=f"qty_{food}")
        
        # Calculate total macros based on quantities (assuming values are per 100g)
        for food in food_inputs:
            food_data = df[df['Food_Item'] == food].iloc[0]
            quantity = quantities[food]
            for col in total_macros.keys():
                if col in df.columns and pd.notna(food_data[col]) and isinstance(food_data[col], (int, float)):
                    total_macros[col] += (float(food_data[col]) * quantity) / 100  # Adjust for 100g basis
        
        # Use columns for layout: left for text, right for graph
        col1, col2 = st.columns([2, 1])  # 2 parts for text, 1 part for graph (right side)
        
        with col1:
            # Display total nutritional values
            st.write("**Total Nutritional Values for Your Consumption:**")
            for col, value in total_macros.items():
                display_value = value if value > 0 else 0  # Use 0 instead of 'N/A' for numeric display
                if isinstance(display_value, (int, float)):
                    st.write(f"{col}: {display_value:.2f}")
                else:
                    st.write(f"{col}: {display_value}")
            
            # Display Meal_Type if available (combine Meal_Types if multiple foods)
            meal_types = [df[df['Food_Item'] == food]['Meal_Type'].iloc[0] for food in food_inputs if 'Meal_Type' in df.columns and pd.notna(df[df['Food_Item'] == food]['Meal_Type'].iloc[0])]
            if meal_types:
                st.write(f"Meal Type(s): {', '.join(set(meal_types))}")
        
        with col2:
            # Create a pie chart (or donut chart) of total macros (if food items are selected)
            macro_values = {}
            for col in ['Calories (kcal)', 'Protein (g)', 'Carbohydrates (g)', 'Fat (g)', 'Fiber (g)', 'Sugars (g)']:
                if col in total_macros and pd.notna(total_macros[col]) and isinstance(total_macros[col], (int, float)):
                    macro_values[col] = float(total_macros[col])  # Include all numeric values, even if zero
            
            if macro_values:  # Check if there are any valid macro values
                macro_df = pd.DataFrame([macro_values])
                # Create a donut chart (pie chart with hole), showing actual values in labels
                fig = px.pie(macro_df, values=list(macro_values.values()), names=list(macro_values.keys()), 
                             title="Total Macros for Consumed Foods", hole=0.4)
                fig.update_traces(textposition='inside', textinfo='label+value')  # Show labels and actual values
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No valid numerical macro data available for consumed foods to display a graph.")
    else:
        st.error("Food_Item column not found in the dataset. Please check your CSV file.")

# 3rd Tab: Meal Planning
with tabs[2]:
    st.subheader("Meal Planning Based on Macros and Meal Type")
    
    # Select macro and meal type for meal planning
    macro_options = ['Calories (kcal)', 'Protein (g)', 'Carbohydrates (g)', 'Fat (g)', 'Fiber (g)', 'Sugars (g)', 'Sodium (mg)', 'Cholesterol (mg)']
    selected_macro = st.selectbox("Select a macro to plan your meal around", macro_options)
    
    if 'Meal_Type' in df.columns:
        unique_meal_types = df['Meal_Type'].unique()
        selected_meal_type = st.selectbox("Select Meal Type", unique_meal_types)
    else:
        st.warning("Meal_Type column not found. Using all meal types.")
        selected_meal_type = None
    
    # Input target value for the selected macro
    target_value = st.number_input(f"Enter target {selected_macro} value", min_value=0.0, value=1000.0)
    
    # Filter foods based on the target macro and meal type
    if selected_macro in df.columns:
        # Filter by meal type if selected
        filtered_df = df.copy()
        if selected_meal_type and 'Meal_Type' in df.columns:
            filtered_df = filtered_df[filtered_df['Meal_Type'] == selected_meal_type]
        
        # Calculate the absolute difference between each food's macro value and the target
        filtered_df['Macro_Diff'] = abs(filtered_df[selected_macro] - target_value)
        
        # Sort by difference and get top 5 recommendations
        recommended_foods = filtered_df.sort_values('Macro_Diff').head(5)
        
        # Use columns for layout: left for text, right for graph
        col1, col2 = st.columns([2, 1])  # 2 parts for text, 1 part for graph (right side)
        
        with col1:
            st.write("**Recommended Foods for Your Target:**")
            for _, row in recommended_foods.iterrows():
                st.write(f"- **Food Item:** {row['Food_Item']}")
                st.write(f"  - {selected_macro}: {row[selected_macro]}")
                st.write(f"  - Category: {row['Category']}")
                st.write(f"  - Meal Type: {row['Meal_Type'] if pd.notna(row['Meal_Type']) else 'N/A'}")
                st.write("---")
        
        with col2:
            # Create a pie chart (or donut chart) of recommended foods' macro values
            if not recommended_foods.empty:
                macro_values = recommended_foods[[selected_macro]].rename(columns={selected_macro: 'Value'})
                macro_values['Food_Item'] = recommended_foods['Food_Item']
                fig = px.pie(macro_values, values='Value', names='Food_Item', 
                             title=f"Recommended Foods for {selected_macro} ({selected_meal_type if selected_meal_type else 'All Meals'})",
                             hole=0.4)  # hole=0.4 makes it a donut chart
                fig.update_traces(textposition='inside', textinfo='label+value')  # Show labels and actual values
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.error(f"{selected_macro} column not found in the dataset. Please check your CSV file.")

# 4th Tab: Protein Calculator
with tabs[3]:
    st.subheader("Protein Calculator")
    
    st.write("""
    This Protein Calculator estimates the daily amount of dietary protein adults require to remain healthy. Children, those who are highly physically active, and pregnant and nursing women typically require more protein. The calculator is also useful for monitoring protein intake for those with kidney disease, liver disease, diabetes, or other conditions in which protein intake is a factor.
    """)
    
    # Input parameters
    st.write("### Input Parameters")
    
    # Age
    age = st.number_input("Age (18 - 80 years)", min_value=18, max_value=80, value=25)
    
    # Gender
    gender = st.radio("Gender", ["Male", "Female"])
    
    # Unit selection (US or Metric)
    unit_system = st.radio("Unit System", ["US Units", "Metric Units"])
    
    # Height and Weight inputs based on unit system
    if unit_system == "US Units":
        height_feet = st.number_input("Height (feet)", min_value=0, max_value=8, value=5)
        height_inches = st.number_input("Height (inches)", min_value=0, max_value=11, value=10)
        weight_lb = st.number_input("Weight (pounds)", min_value=0, value=160)
        height_cm = (height_feet * 30.48) + (height_inches * 2.54)  # Convert to cm
        weight_kg = weight_lb * 0.45359237  # Convert to kg
    else:  # Metric Units
        height_cm = st.number_input("Height (cm)", min_value=0, value=180)
        weight_kg = st.number_input("Weight (kg)", min_value=0, value=60)
    
    # Activity level
    activity_options = {
        "Sedentary: little or no exercise": 1.2,
        "Light: exercise 1-3 times/week": 1.375,
        "Moderate: exercise 4-5 times/week": 1.465,
        "Active: daily exercise or intense exercise 3-4 times/week": 1.55,
        "Very Active: intense exercise 6-7 times/week": 1.725,
        "Extra Active: very intense exercise daily, or physical job": 1.9
    }
    activity = st.selectbox("Activity Level", list(activity_options.keys()))
    activity_factor = activity_options[activity]
    
    # BMR estimation formula
    st.write("### BMR Estimation Settings")
    bmr_formula = st.radio("BMR Estimation Formula", ["Mifflin St Jeor", "Revised Harris-Benedict", "Katch-McArdle"])
    
    if bmr_formula == "Mifflin St Jeor":
        # Mifflin St Jeor Formula: BMR = 10 * weight(kg) + 6.25 * height(cm) - 5 * age(y) + 5 (men) or -161 (women)
        if gender == "Male":
            bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
        else:
            bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
    elif bmr_formula == "Revised Harris-Benedict":
        # Revised Harris-Benedict Formula: BMR = 13.397W + 4.799H - 5.677A + 88.362 (men) or 9.247W + 3.098H - 4.330A + 447.593 (women)
        if gender == "Male":
            bmr = 13.397 * weight_kg + 4.799 * height_cm - 5.677 * age + 88.362
        else:
            bmr = 9.247 * weight_kg + 3.098 * height_cm - 4.330 * age + 447.593
    else:  # Katch-McArdle
        body_fat_pct = st.number_input("Body Fat Percentage (%)", min_value=0.0, max_value=100.0, value=20.0)
        lean_body_mass = weight_kg * (1 - (body_fat_pct / 100))
        bmr = 370 + (21.6 * lean_body_mass)
    
    # Calculate total daily energy expenditure (TDEE)
    tdee = bmr * activity_factor
    
    # Calculate protein needs (simplified, as a reference)
    base_protein = 0.8 * weight_kg  # Default RDA
    adjusted_protein = base_protein * activity_factor  # Adjust for activity level
    
    # Display results
    st.write("### Results")
    st.write(f"**Basal Metabolic Rate (BMR):** {bmr:.2f} kcal/day")
    st.write(f"**Total Daily Energy Expenditure (TDEE):** {tdee:.2f} kcal/day")
    st.write(f"**Recommended Protein Intake:** {adjusted_protein:.2f} g/day (adjusted for activity)")

    # Display age-based RDA table (static, as in HTML)
    st.write("### Recommended Dietary Allowance (RDA) of Protein, Based on Age")
    rda_data = {
        "Age Range": ["1 - 3", "4 - 8", "9 - 13", "14 - 18 (Girls)", "14 - 18 (Boys)", "19 - 70+ (Women)", "19 - 70+ (Men)"],
        "Protein Needed (g/day)": [13, 19, 34, 46, 52, 46, 56]
    }
    rda_df = pd.DataFrame(rda_data)
    st.table(rda_df)
    
    # Display pregnancy and lactation table (static, as in HTML)
    st.write("### Extra Protein Requirements for Pregnancy and Lactation")
    pregnancy_data = {
        "Stage": ["Pregnancy trimester 1", "Pregnancy trimester 2", "Pregnancy trimester 3", "Lactation First 6 months", "Lactation After 6 months"],
        "Safe Intake (g/day)": [1, 10, 31, 19, 13],
        "Additional Energy (kJ/day)": [375, 1200, 1950, 2800, 1925],
        "Protein:Energy Ratio": [0.04, 0.11, 0.23, 0.11, 0.11]
    }
    pregnancy_df = pd.DataFrame(pregnancy_data)
    st.table(pregnancy_df)
    
    # Additional information from HTML
    st.write("### What are proteins?")
    st.write("""
    Proteins are one of three primary macronutrients that provide energy to the human body, along with fats and carbohydrates. Proteins are also responsible for a large portion of the work that is done in cells; they are necessary for proper structure and function of tissues and organs, and also act to regulate them. They are comprised of a number of amino acids that are essential to proper body function, and serve as the building blocks of body tissue.

    There are 20 different amino acids in total, and the sequence of amino acids determines a protein's structure and function. While some amino acids can be synthesized in the body, there are 9 amino acids that humans can only obtain from dietary sources (insufficient amounts of which may sometimes result in death), termed essential amino acids. Foods that provide all of the essential amino acids are called complete protein sources, and include both animal (meat, dairy, eggs, fish) as well as plant-based sources (soy, quinoa, buckwheat).

    Proteins can be categorized based on the function they provide to the body. Below is a list of some types of proteins:
    - Antibody—proteins that protect the body from foreign particles, such as viruses and bacteria, by binding to them
    - Enzyme—proteins that help form new molecules as well as perform the many chemical reactions that occur throughout the body
    - Messenger—proteins that transmit signals throughout the body to maintain body processes
    - Structural component—proteins that act as building blocks for cells that ultimately allow the body to move
    - Transport/storage—proteins that move molecules throughout the body
    """)
    
    st.write("### How much protein do I need?")
    st.write("""
    The amount of protein that the human body requires daily is dependent on many conditions, including overall energy intake, growth of the individual, and physical activity level. It is often estimated based on body weight, as a percentage of total caloric intake (10-35%), or based on age alone. 0.8g/kg of body weight is a commonly cited recommended dietary allowance (RDA). This value is the minimum recommended value to maintain basic nutritional requirements, but consuming more protein, up to a certain point, maybe beneficial, depending on the sources of the protein.

    The recommended range of protein intake is between 0.8 g/kg and 1.8 g/kg of body weight, dependent on the many factors listed above. People who are highly active, or who wish to build more muscle should generally consume more protein. Some sources suggest consuming between 1.8 to 2 g/kg for those who are highly active. The amount of protein a person should consume, to date, is not an exact science, and each individual should consult a specialist, be it a dietitian, doctor, or personal trainer, to help determine their individual needs.
    """)
    
    st.write("### Foods High in Protein")
    st.write("""
    There are many different combinations of food that a person can eat to meet their protein intake requirements. For many people, a large portion of protein intake comes from meat and dairy, though it is possible to get enough protein while meeting certain dietary restrictions you might have. Generally, it is easier to meet your RDA of protein by consuming meat and dairy, but an excess of either can have a negative health impact. There are plenty of plant-based protein options, but they generally contain less protein in a given serving. Ideally, a person should consume a mixture of meat, dairy, and plant-based foods in order to meet their RDA and have a balanced diet replete with nutrients.

    If possible, consuming a variety of complete proteins is recommended. A complete protein is a protein that contains a good amount of each of the nine essential amino acids required in the human diet. Examples of complete protein foods or meals include:

    **Meat/Dairy examples**  
    - Eggs  
    - Chicken breast  
    - Cottage cheese  
    - Greek yogurt  
    - Milk  
    - Lean beef  
    - Tuna  
    - Turkey breast  
    - Fish  
    - Shrimp  

    **Vegan/plant-based examples**  
    - Buckwheat  
    - Hummus and pita  
    - Soy products (tofu, tempeh, edamame beans)  
    - Peanut butter on toast or some other bread  
    - Beans and rice  
    - Quinoa  
    - Hemp and chia seeds  
    - Spirulina  

    Generally, meat, poultry, fish, eggs, and dairy products are complete protein sources. Nuts and seeds, legumes, grains, and vegetables, among other things, are usually incomplete proteins. There is nothing wrong with incomplete proteins however, and there are many healthy, high protein foods that are incomplete proteins. As long as you consume a sufficient variety of incomplete proteins to get all the required amino acids, it is not necessary to specifically eat complete protein foods. In fact, certain high fat red meats for example, a common source of complete proteins, can be unhealthy. Below are some examples of high protein foods that are not complete proteins:
    - Almonds  
    - Oats  
    - Broccoli  
    - Lentils  
    - Ezekiel bread  
    - Chia seeds  
    - Pumpkin seeds  
    - Peanuts  
    - Brussels sprouts  
    - Grapefruit  
    - Green peas  
    - Avocados  
    - Mushrooms  
    """)
    
    st.write("### Amount of Protein in Common Foods")
    protein_food_data = {
        "Food": ["Milk (1 cup/8 oz)", "Egg (1 large/50 g)", "Meat (1 slice / 2 oz)", "Seafood (2 oz)", "Bread (1 slice/64 g)", "Corn (1 cup/166 g)", "Rice (1 cup/195 g)", "Dry Bean (1 cup/92 g)", "Nuts (1 cup/92 g)", "Fruits and Vegetables (1 cup)", "Pizza (1 slice/107 g)", "Hamburger (McDonald Medium)"],
        "Protein Amount (g)": [8, 6, 14, 16, 8, 16, 5, 16, 20, "0-1", 12, 20]
    }
    protein_food_df = pd.DataFrame(protein_food_data)
    st.table(protein_food_df)
    


