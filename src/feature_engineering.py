import pandas as pd
import re

def extract_features(row):
    """Extract features from a LinkedIn post row"""
    features = {}
    
    # Post type encoding (one-hot)
    post_types = ['Text', 'Image', 'Video', 'Link', 'Reel']
    for ptype in post_types:
        features[f'is_{ptype.lower()}'] = 1 if row['Post Type'] == ptype else 0
    
    # Month encoding (convert to numeric for seasonality)
    month_map = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 
                 'May': 5, 'June': 6, 'July': 7, 'August': 8,
                 'September': 9, 'October': 10, 'November': 11, 'December': 12}
    features['month_num'] = month_map.get(row['Month'], 0)
    
    # Engagement metrics (as features for prediction)
    features['impressions'] = row['Impressions']
    features['reach'] = row['Reach']
    features['clicks'] = row['Clicks']
    
    # Derived features
    features['impression_to_reach_ratio'] = row['Impressions'] / row['Reach'] if row['Reach'] > 0 else 0
    features['click_through_rate'] = (row['Clicks'] / row['Impressions'] * 100) if row['Impressions'] > 0 else 0
    
    return features

def prepare_dataset(csv_path):
    """Prepare the full dataset with features"""
    df = pd.read_csv(csv_path)
    
    # Calculate engagement score (our target variable)
    df['engagement_score'] = (
        df['Reactions'] * 1 + 
        df['Comments'] * 3 + 
        df['Shares'] * 5
    )
    
    # Extract features for each row
    features_list = []
    for idx, row in df.iterrows():
        features_list.append(extract_features(row))
    
    X = pd.DataFrame(features_list)
    y = df['engagement_score']
    
    return X, y, df

if __name__ == "__main__":
    X, y, df = prepare_dataset('data/linkedin_posts.csv')
    print("Features shape:", X.shape)
    print("Target shape:", y.shape)
    print("\nFeature columns:", X.columns.tolist())
    print("\nFirst few rows:")
    print(X.head())

