# F1 Fantasy Team Planner 🏎️

This is a Python hobby project created to optimize team selection in the official F1 Fantasy game. The script fetches real-time player and constructor data from the F1 Fantasy REST API and calculates the highest-scoring team combination within a given budget.

## Features
* **Live Data Fetching:** Connects to the F1 Fantasy API to get the latest driver and constructor prices and points.
* **Data Processing:** Cleans and formats the incoming JSON data for analysis.
* **Optimization Algorithm:** Uses Python's `itertools` to evaluate hundreds of thousands of combinations, finding the absolute best lineup (5 drivers, 2 constructors) under a $100M budget.

## Technologies Used
* **Python 3**
* `requests` (API integration)
* `itertools` (Combinatorics and logic)
* JSON data handling

## How to Run
1. Clone this repository or download the `F!TeamPlanner.py` file.
2. Ensure you have Python installed.
3. Install the required `requests` library by running: 
   `pip install requests`
4. Run the script:
   `python "F!TeamPlanner.py"`

## About the Author
Created as a personal project to practice data pipelines, API integration, and algorithm optimization in Python.
