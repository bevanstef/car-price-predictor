# Sri Lanka Used Car Price Predictor

An ongoing end-to-end machine learning portfolio project predicting used car market prices in Sri Lanka (LKR) based on brand, model, manufacturing year, mileage, fuel type, transmission, and engine capacity.

---

## 🛠️ Tech Stack

- **Frontend:** React 18, Vite, JavaScript (ES6+), Modern CSS
- **Backend API:** Python, FastAPI, Pydantic, Uvicorn
- **Machine Learning & Data:** scikit-learn, pandas, NumPy, joblib
- **Environment & VCS:** Python venv, Git, GitHub

---

## 🏗️ Architecture & Project Structure

The project follows a Clean Architecture approach with clear separation between data engineering, machine learning modeling, API serving, and the frontend presentation layer:

```text
car-price-predictor/
├── generate_data.py        # Synthetic dataset generator with intentional real-world noise
├── cars_raw.csv            # Raw dataset (tracked as before-cleaning proof)
├── inspectdata.py          # Data inspection & IQR outlier exploration
├── clean_data.py           # Modular data cleaning pipeline (.pipe())
├── cars_clean.csv          # Cleaned dataset (tracked as after-cleaning proof)
│
├── train.py                # ML pipeline (ColumnTransformer, OneHotEncoder, Linear vs RF)
├── model.joblib            # Serialized trained scikit-learn pipeline (git-ignored)
│
├── app.py                  # FastAPI server (lifespan model loader, Pydantic validation)
│
├── frontend/               # React 18 + Vite SPA
│   ├── vite.config.js      # Dev server configured with proxy to backend (/predict)
│   ├── package.json
│   └── src/
│       ├── App.jsx         # Form state, dependent brand/model dropdowns, predictions
│       ├── components/
│       │   └── SelectField.jsx # Reusable select component
│       └── index.css       # Clean styling
│
├── requirements.txt        # Python backend dependencies
└── README.md
```

---

## 📊 Dataset & Honesty Disclosure

- **Synthetic Data:** The dataset used in this project is synthetically generated using NumPy and pandas. It deliberately introduces real-world messiness (inconsistent brand text casing, missing mileage and fuel values, duplicate entries, and planted sensor/human entry outliers) to practice and demonstrate production-level data cleaning.
- **Simplifications:** Feature distributions for transmission, fuel type, and engine capacity are generated independently of vehicle model. High model accuracy on this dataset reflects clean synthetic relationships and is not presented as real-world market accuracy.

---

## 🚀 How It Works (Request Flow)

1. **User input:** User selects vehicle specifications in the React frontend.
2. **Dependent Filtering:** The frontend ensures valid brand-model pairs (e.g., Honda -> Vezel; prevents invalid combinations like Toyota -> Vezel).
3. **API Request:** `POST /predict` sends a JSON payload to the FastAPI backend.
4. **Validation:** Pydantic strictly validates types, allowed categorical values, and numeric ranges.
5. **Inference:** Pre-loaded scikit-learn pipeline transforms features and predicts price in LKR.

---

## 📈 Model Performance & Evaluation

Both models were evaluated on an 80/20 train-test split (`random_state=42`) using the cleaned dataset:

| Model | $R^2$ Score | Mean Absolute Error (MAE) |
|---|---|---|
| **Linear Regression (Baseline)** | 0.8086 | LKR 792,045.77 |
| **Random Forest Regressor** (Winner) | **0.9517** | **LKR 353,225.00** |

The best model is bundled directly with the scikit-learn `ColumnTransformer` (One-Hot Encoder + Passthrough) into `model.joblib`.

---

## 💻 Running the Project Locally

### 1. Backend (FastAPI)
```powershell
# Create & activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt

# Run the data cleaning pipeline
python clean_data.py

# Train the model and generate model.joblib
python train.py

# Start the API server
uvicorn app:app --reload --port 8000
```
Swagger API docs available at: `http://127.0.0.1:8000/docs`

### 2. Frontend (React + Vite)
```powershell
cd frontend
npm install
npm run dev
```
Open application at: `http://localhost:5173`

