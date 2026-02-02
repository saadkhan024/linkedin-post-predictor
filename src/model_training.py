import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score
import pickle
import os

from feature_engineering import prepare_dataset

def train_model(data_path='data/linkedin_posts.csv'):
    """Train the LinkedIn post predictor model"""
    
    print("📊 Loading and preparing data...")
    X, y, df = prepare_dataset(data_path)
    
    print(f"Dataset: {X.shape[0]} posts, {X.shape[1]} features")
    print(f"Target range: {y.min()} to {y.max()}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"\nTrain set: {len(X_train)} posts")
    print(f"Test set: {len(X_test)} posts")
    
    # Scale features
    print("\n⚙️ Scaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Random Forest model
    print("\n🤖 Training Random Forest model...")
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train_scaled, y_train)
    
    # Evaluate
    print("\n📈 Evaluating model...")
    y_pred_train = model.predict(X_train_scaled)
    y_pred_test = model.predict(X_test_scaled)
    
    train_r2 = r2_score(y_train, y_pred_train)
    test_r2 = r2_score(y_test, y_pred_test)
    train_mae = mean_absolute_error(y_train, y_pred_train)
    test_mae = mean_absolute_error(y_test, y_pred_test)
    
    print(f"\nTrain R² Score: {train_r2:.3f}")
    print(f"Test R² Score: {test_r2:.3f}")
    print(f"Train MAE: {train_mae:.2f}")
    print(f"Test MAE: {test_mae:.2f}")
    
    # Feature importance
    print("\n🔍 Top 5 Important Features:")
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    for idx, row in feature_importance.head(5).iterrows():
        print(f"  {row['feature']}: {row['importance']:.3f}")
    
    # Save model and scaler
    print("\n💾 Saving model...")
    os.makedirs('models', exist_ok=True)
    
    with open('models/predictor_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    with open('models/scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    
    # Save feature columns for prediction
    with open('models/feature_columns.pkl', 'wb') as f:
        pickle.dump(X.columns.tolist(), f)
    
    print("✅ Model saved to models/")
    
    return model, scaler, feature_importance

if __name__ == "__main__":
    model, scaler, importance = train_model()

