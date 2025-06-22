import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

def prepare_features(df):
    # Feature engineering
    features = df[['category_name', 'duration_sec', 'tag_count', 'publish_hour']]
    features = pd.get_dummies(features, columns=['category_name'])
    
    # Target - define "trending" as top 20% by views
    target = (df['view_count'] > df['view_count'].quantile(0.8)).astype(int)
    
    return features, target

def train_model(df):
    X, y = prepare_features(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Model accuracy: {acc:.2f}")
    
    # Save model
    joblib.dump(model, 'models/trending_predictor.pkl')
    return model

def predict_trending(model, df):
    X, _ = prepare_features(df)
    preds = model.predict(X)
    proba = model.predict_proba(X)[:, 1]
    return pd.DataFrame({'pred': preds, 'proba': proba}, index=df.index)