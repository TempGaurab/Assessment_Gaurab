# Healthcare AI Assistant

This project aims to build a **healthcare AI assistant** that can generate customized treatment plans based on patient symptoms, medical conditions, and geographic location. The system integrates with the **Gemini API** to provide content generation capabilities.

## Requirements

### Python 3.8+

### Required Libraries:

- `datetime`
- `unittest`
- `google-genai`
- `os`
- `pandas`
- `numpy`
- `json`
- `dotenv`
- `geopy`

### Environment Variables:

Ensure that your environment variables (API keys, etc.) are correctly set in `.env`. You will need to create **two API keys** for it to work. Add them to the `.env` file.

## Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/TempGaurab/Assessment_Gaurab.git
   cd Assessment_Gaurab
   ```

2. **Install Python dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Install NPM dependencies:**

   ```bash
   npm install
   ```

4. **Set up the environment:**

   - Create a `.env` file in the root directory and add the following (replace with your actual API keys):

   ```env
   GEMINI_API_KEY=your-api-key-here
   ANOTHER_API_KEY=your-other-api-key-here
   ```

## Code and Files

- **Python Code:**

  - `assessment.py` contains the main Python code for generating treatment plans.
  - **Sample Cases:** `3-samples.py` contains sample input data for testing.
  - **Test Cases:** `testtreatmentplanassistant.py` contains test cases to evaluate the assistant.

- **Frontend:**
  - There is a **React** frontend that you can run using **Vite** and **npm**. The frontend is already hosted, and you can view it at [https://assessment-gaurab.vercel.app/](https://assessment-gaurab.vercel.app/).
  - The frontend components are managed in the `src` folder and can be modified as needed.

## Known Issues

Any issues encountered with the Gemini API can be found in the `learning_the_problem&gemini.ipynb` notebook.

## Authors

- **Gaurab** – Project lead and developer.
