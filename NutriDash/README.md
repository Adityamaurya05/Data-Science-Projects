
# Nutridash - Nutrition Dashboard



A **Streamlit-based Nutrition Dashboard** to analyze food items, plan meals, calculate protein intake, and track nutritional values. This interactive web application is designed to help users make informed decisions about their diet and nutrition.

---

## Features

1. **Food Item Analysis**:
   - Select a food item from the dataset to view its nutritional breakdown.
   - Visualize macronutrients (calories, protein, carbs, fat, etc.) using interactive pie charts.

2. **Meal Consumption Analysis**:
   - Select multiple food items and specify their quantities to calculate total nutritional intake.
   - View a summary of total calories, protein, carbs, fat, and other nutrients.

3. **Meal Planning**:
   - Plan meals based on specific macronutrient goals (e.g., calories, protein, carbs).
   - Get food recommendations tailored to your target macro and meal type.

4. **Protein Calculator**:
   - Calculate your daily protein requirements based on age, gender, weight, height, and activity level.
   - Learn about protein-rich foods and their nutritional values.

---

## Dataset

The application uses a CSV dataset (`daily_food_nutrition_dataset.csv`) containing nutritional information for various food items. The dataset includes the following columns:

- `Food_Item`: Name of the food item.
- `Category`: Category of the food (e.g., fruits, vegetables, dairy).
- `Calories (kcal)`: Calories per serving.
- `Protein (g)`: Protein content in grams.
- `Carbohydrates (g)`: Carbohydrate content in grams.
- `Fat (g)`: Fat content in grams.
- `Fiber (g)`: Fiber content in grams.
- `Sugars (g)`: Sugar content in grams.
- `Sodium (mg)`: Sodium content in milligrams.
- `Cholesterol (mg)`: Cholesterol content in milligrams.
- `Water_Intake (ml)`: Water content in milliliters.
- `Meal_Type`: Type of meal (e.g., breakfast, lunch, dinner).

---

## How to Use

### Prerequisites

1. **Python 3.8 or higher** installed on your system.
2. **Required Python packages** installed. You can install them using the `requirements.txt` file.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/nutrition-dashboard.git
   cd nutrition-dashboard
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Place your `daily_food_nutrition_dataset.csv` file in the `data` directory (or update the file path in the code).

4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

5. Open your browser and navigate to `http://localhost:8501` to view the dashboard.

### Application Walkthrough

1. **Food Item Analysis**  
   - Select a food item from the dropdown menu.  
   - View its nutritional values and a pie chart showing the macronutrient breakdown.

2. **Meal Consumption Analysis**  
   - Select multiple food items and specify their quantities.  
   - The app calculates the total nutritional intake and displays it in a table and pie chart.

3. **Meal Planning**  
   - Select a macronutrient (e.g., calories, protein) and a target value.  
   - Choose a meal type (e.g., breakfast, lunch).  
   - The app recommends food items that match your criteria.

4. **Protein Calculator**  
   - Enter your age, gender, weight, height, and activity level.  
   - The app calculates your daily protein requirement and provides additional information about protein-rich foods.



## Technologies Used

- **Streamlit**: For building the interactive web application.
- **Pandas**: For data manipulation and analysis.
- **Plotly**: For creating interactive charts and visualizations.



## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes.
4. Push your branch to your forked repository.
5. Submit a pull request.



## License

This project is licensed under the MIT License. See the `LICENSE` file for details.



## Acknowledgments

- **Dataset**: Nutrition Dataset (replace with actual source if available).
- **Streamlit**: For making it easy to build and share data apps.
- **Plotly**: For creating beautiful and interactive visualizations.



## Contact

For questions or feedback, feel free to reach out:

- **Your Name**: Aditya Maurya
- **GitHub**: [Adityamaurya05](https://github.com/Adityamaurya05)

