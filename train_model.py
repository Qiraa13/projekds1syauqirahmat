import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report
import joblib

print("Memulai proses training model Attrition...")

# 1. Load Data
try:
    df = pd.read_csv('employee_data.csv')
    print(f"Total awal: {df.shape[0]} baris.")
    
    # Hapus row yang Attrition-nya kosong (NaN)
    df = df.dropna(subset=['Attrition'])
    print(f"Setelah hapus data kosong, ada {df.shape[0]} baris siap pakai.")
except Exception as e:
    print("Error membaca dataset:", e)
    exit()

features = [
    'Department', 'Age', 'DailyRate', 'OverTime', 'WorkLifeBalance', 
    'TotalWorkingYears', 'YearsAtCompany', 'YearsInCurrentRole', 'YearsSinceLastPromotion'
]

X = df[features]
y = df['Attrition'].astype(int)

# 2. Setup Pipeline Preprocessing & Model
numeric_features = [
    'Age', 'DailyRate', 'WorkLifeBalance', 'TotalWorkingYears', 
    'YearsAtCompany', 'YearsInCurrentRole', 'YearsSinceLastPromotion'
]
categorical_features = ['Department', 'OverTime']

preprocessor = ColumnTransformer(
    transformers=[
        ('num', 'passthrough', numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, class_weight="balanced"))
])

# 3. Split Dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 4. Integrasi MLFlow ke Server Cloud DagsHub
import dagshub
dagshub.init(repo_owner='Qiraa13', repo_name='dataresignDS', mlflow=True)
mlflow.set_experiment("Employee_Attrition_Prediction_Experiment")

print("Mengeksekusi MLflow run...")
with mlflow.start_run() as run:
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    
    print("\n--- Classification Report ---")
    print(classification_report(y_test, y_pred))
    
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_depth", 10)
    mlflow.log_param("random_state", 42)
    mlflow.log_metric("accuracy", acc)
    
    mlflow.sklearn.log_model(pipeline, "random_forest_model")
    joblib.dump(pipeline, 'attrition_model.pkl')
    
    print(f"\n✅ Model berhasil dilatih dengan Akurasi: {acc*100:.2f}%")
    print("✅ Model mempelajari kelas:", pipeline.classes_)
    print("✅ File tersimpan sebagai 'attrition_model.pkl'.")
