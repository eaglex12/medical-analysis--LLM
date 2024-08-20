# Meal Analysis Program

## Overview

This project utilizes Google's Gemini models for meal analysis. The setup involves using a virtual environment (venv) to maintain a clean development environment.

## Setup Instructions

1. **Create a `.env` File:**

   - Save your Google GEMINI API key in a `.env` file with the key name `GEM`.

2. **Download the JSON File:**

   - Use the provided script to download the necessary JSON file. Run the following command:
     ```bash
     python download_queries.py
     ```

3. **Run the Main Program:**
   - Execute the main program using:
     ```bash
     python meal_analysis.py
     ```

## Dependencies

Make sure to install the required packages using:

```bash
pip install -r requirements.txt

```
