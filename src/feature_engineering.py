import pandas as pd
import re
from textblob import TextBlob

def analyze_post_text(post_text):
    """Analyze actual LinkedIn post text and extract features"""
    features = {}
    
    # Basic text metrics
    features['word_count'] = len(post_text.split())
    features['char_count'] = len(post_text)
    features['line_breaks'] = post_text.count('\n')
    features['sentences'] = len(post_text.split('.'))
    
    # Engagement triggers
    features['hashtag_count'] = len(re.findall(r'#\w+', post_text))
    features['mention_count'] = len(re.findall(r'@\w+', post_text))
    features['emoji_count'] = len([c for c in post_text if c in '😀😃😄😁😆😅🤣😂🙂🙃😉😊😇🥰😍🤩😘😗☺️😚😙🥲😋😛😜🤪😝🤑🤗🤭🤫🤔🤐🤨😐😑😶😏😒🙄😬🤥😌😔😪🤤😴😷🤒🤕🤢🤮🤧🥵🥶🥴😵🤯🤠🥳🥸😎🤓🧐😕😟🙁☹️😮😯😲😳🥺😦😧😨😰😥😢😭😱😖😣😞😓😩😫🥱😤😡😠🤬😈👿💀☠️💩🤡👹👺👻👽👾🤖😺😸😹😻😼😽🙀😿😾🙈🙉🙊💋💌💘💝💖💗💓💞💕💟❣️💔❤️🧡💛💚💙💜🤎🖤🤍💯💢💥💫💦💨🕳️💣💬🗨️🗯️💭💤👋🤚🖐️✋🖖👌🤌🤏✌️🤞🤟🤘🤙👈👉👆🖕👇☝️👍👎✊👊🤛🤜👏🙌👐🤲🤝🙏✍️💅🤳💪🦾🦿🦵🦶👂🦻👃🧠🫀🫁🦷🦴👀👁️👅👄🫦'])
    features['url_count'] = len(re.findall(r'http[s]?://\S+', post_text))
    features['question_marks'] = post_text.count('?')
    features['exclamation_marks'] = post_text.count('!')
    
    # Sentiment analysis
    try:
        sentiment = TextBlob(post_text).sentiment
        features['polarity'] = sentiment.polarity  # -1 to 1
        features['subjectivity'] = sentiment.subjectivity  # 0 to 1
    except:
        features['polarity'] = 0
        features['subjectivity'] = 0.5
    
    # Hook analysis (first line/100 chars)
    first_line = post_text.split('\n')[0] if '\n' in post_text else post_text[:100]
    features['hook_length'] = len(first_line)
    features['hook_has_number'] = 1 if re.search(r'\d', first_line) else 0
    features['hook_has_emoji'] = 1 if any(c in first_line for c in '🔥💡✅🚀💪👉📈🎯') else 0
    features['hook_has_question'] = 1 if '?' in first_line else 0
    
    # Call-to-action detection
    cta_keywords = ['comment', 'share', 'like', 'follow', 'click', 'check', 'learn', 'read', 'watch', 'join', 'dm', 'thoughts', 'agree']
    features['has_cta'] = 1 if any(keyword in post_text.lower() for keyword in cta_keywords) else 0
    
    # List/bullet points
    features['has_list'] = 1 if any(marker in post_text for marker in ['1.', '2.', '•', '-', '→']) else 0
    
    return features

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

