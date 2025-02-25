# Delhi MetroNav

**Delhi MetroNav** is a user-friendly Streamlit app that helps you explore and navigate the Delhi Metro system. Whether you want to check out metro lines and stations or find the fastest route between two stops, this interactive dashboard has you covered! It’s built with Python and uses libraries like Streamlit, pandas, and Folium to bring the metro network to life.

This README will guide you through everything you need to know—step by step—so you can set it up, use it, and even contribute if you’d like. Let’s get started!

## What Does This Project Do? (Features)

Here’s what you can do with Delhi MetroNav:

- **Dashboard**: See all the details about Delhi Metro lines, stations, and their layouts (like whether they’re elevated or underground). You can filter the info by line, layout, or even the year a station opened.
- **Route Finder**: Pick a starting station and a destination, and the app will show you the best route—including any transfers you need to make. You’ll also get a cool visual map to see your journey!

## How to Set It Up

Setting up Delhi MetroNav is super easy! Just follow these steps, and you’ll have it running in no time.

### Step 1: Install Python

- You’ll need **Python 3.7 or later**. If you don’t have it yet:
  - Download it from [python.org](https://www.python.org/downloads/).
  - Install it and make sure you can run `python --version` (or `python3 --version`) in your terminal or command prompt.

### Step 2: Install the Required Libraries

- This project uses some Python libraries. Open your terminal (or command prompt) and run this command:
  ```bash
  pip install streamlit pandas folium geopy plotly

### What do these do?

- streamlit: Runs the interactive web app.
- pandas: Handles the metro data.
- folium: Creates the map for the route finder.
- geopy: Helps with location stuff.
- plotly: Makes charts look nice.
 If you get errors, try pip3 instead of pip or update pip with pip install --upgrade pip.

### Step 3: Get the Metro Data

The app needs a CSV file with Delhi Metro station info (station names, lines, coordinates, etc.).

- You can download it from [Dataset](https://www.kaggle.com/datasets/arunjangir245/delhi-metro-dataset) (replace with the real link if you have it!).
- Or, check the project repository—it’s included there!
- Save it as `Delhi metro.csv` in the same folder as your app file.

### Step 4: Run the App

- Open your terminal, go to the project folder (use `cd` to navigate), and type:
  ```bash
  streamlit run Dashboard.py
- Replace `Dashboard.py` with the actual name of your Python file if it’s different.
- This starts the Streamlit app, and a browser window should pop up (or go to `http://localhost:8501` manually).

## How to Use It

Once the app is running, here’s how to play around with it:

1. **Open the App**: Go to `http://localhost:8501` in your browser.
2. **Explore the Two Tabs**:
   - **Dashboard**:
     - Check out metro lines, stations, and layouts.
     - Use the sidebar filters to pick a line (like Blue or Red), a layout (elevated or underground), or a year stations opened.
   - **Route Finder**:
     - Choose your starting station and destination from dropdown menus.
     - Click “Find Route” to see the best path, including transfers and a map with arrows showing your journey.

That’s it! It’s designed to be simple and intuitive.

## Where Does the Data Come From?

The app uses a file called `Delhi metro.csv`. This CSV has all the metro info, like:

- Station ID and name
- Distance from the first station
- Metro line (e.g., Blue Line, Red Line)
- Opening year
- Layout (elevated, underground, etc.)
- Latitude and longitude (for the map)

You can get this file from the link in the setup section or the project repo. Want to update it? Just edit the CSV with new data!

## Want to Help Out? (Contributing)

If you’d like to make this project even better, here’s how to contribute:

1. **Fork the Repo**: Click “Fork” on the GitHub page to make your own copy.
2. **Clone It**: Download your fork to your computer with:
   ```bash
   git clone <your-fork-url>
3. **Make Changes**: Edit the code, add features, or fix bugs.
4. **Commit & Push**: Save your changes with:
   ```bash
   git add .
   git commit -m "Added a cool new feature"
   git push
5. **Create a Pull Request:** Go to the original repo on GitHub and submit a pull request to share your changes.

## Found a Problem? (Reporting Issues)
If something’s not working or you have an idea:

- Go to the GitHub repo.
- Click “Issues” and “New Issue.”
- Describe what’s wrong or what you’d like to see—every suggestion helps!

## License

This project uses the **MIT License**. That means you’re free to use, modify, and share it—just check the `LICENSE` file in the repo for details.