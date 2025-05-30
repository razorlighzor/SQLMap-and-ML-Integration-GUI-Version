import joblib
import pandas as pd

current_model = None
vectorizer = joblib.load("modelfile/tfidf_vectorizer.pkl")

def load_model(model_path):
    global current_model
    current_model = joblib.load(model_path)
    return f"Model {model_path} loaded successfully."

def extract_url_feature_set(url, aggressive=False):
    features = {
        "Query_Length": len(url),
        "Special_Char_Count": sum(url.count(char) for char in ['--', '#', ';', '\'', '"', '/*', '*/']),
        "Keyword_Count": sum(url.upper().count(k) for k in ['SELECT', 'UNION', 'INSERT', 'DELETE', 'UPDATE', 'DROP', 'OR', 'AND']),
        "Has_SQLi_Pattern": int(any(p in url.lower() for p in ['or 1=1', 'and 1=1', 'pg_sleep', 'utl_inaddr', 'char(', 'convert(', 'concat('])),
        "Has_Comment": int(any(c in url for c in ['--', '/*', '#']))
    }
    features["Special_Char_Ratio"] = features["Special_Char_Count"] / features["Query_Length"] if features["Query_Length"] != 0 else 0
    return features

def predict_sqli(url, aggressive=False):
    if current_model is None:   
        return "No ML model loaded. Please select a model first."
    try:
        features = extract_url_feature_set(url, aggressive)
        tfidf_vec = vectorizer.transform([url]).toarray()[0]
        tfidf_features = {f'TFIDF_{i}': tfidf_vec[i] for i in range(len(tfidf_vec))}

        # Ensure features match trained model columns (important!)
        all_features = {**features, **tfidf_features}
        df = pd.DataFrame([all_features])
        prediction = current_model.predict(df)[0]
        return int(prediction)
    except Exception as e:
        return f"ML Prediction Error: {e}"

