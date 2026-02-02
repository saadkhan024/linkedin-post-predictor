import pickle
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

def load_model():
    """Load the trained model and scaler"""
    with open('models/predictor_model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('models/scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    with open('models/feature_columns.pkl', 'rb') as f:
        feature_columns = pickle.load(f)
    return model, scaler, feature_columns

def predict_post_performance(post_type, month, impressions=1000, reach=1200, clicks=100):
    """
    Predict engagement score for a LinkedIn post
    
    Args:
        post_type: 'Text', 'Image', 'Video', 'Link', or 'Reel'
        month: Month name (e.g., 'January', 'May')
        impressions: Expected impressions (default: 1000)
        reach: Expected reach (default: 1200)
        clicks: Expected clicks (default: 100)
    
    Returns:
        dict with score and recommendations
    """
    
    model, scaler, feature_columns = load_model()
    
    # Create feature dictionary
    features = {
        'is_text': 1 if post_type == 'Text' else 0,
        'is_image': 1 if post_type == 'Image' else 0,
        'is_video': 1 if post_type == 'Video' else 0,
        'is_link': 1 if post_type == 'Link' else 0,
        'is_reel': 1 if post_type == 'Reel' else 0,
    }
    
    # Month encoding
    month_map = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 
                 'May': 5, 'June': 6, 'July': 7, 'August': 8,
                 'September': 9, 'October': 10, 'November': 11, 'December': 12}
    features['month_num'] = month_map.get(month, 5)
    
    # Engagement metrics
    features['impressions'] = impressions
    features['reach'] = reach
    features['clicks'] = clicks
    features['impression_to_reach_ratio'] = impressions / reach if reach > 0 else 0
    features['click_through_rate'] = (clicks / impressions * 100) if impressions > 0 else 0
    
    # Create DataFrame
    features_df = pd.DataFrame([features])[feature_columns]
    
    # Scale and predict
    features_scaled = scaler.transform(features_df)
    engagement_score = model.predict(features_scaled)[0]
    
    # Generate recommendations
    recommendations = []
    
    if post_type == 'Text':
        recommendations.append("✅ Text posts perform well - keep it conversational")
    elif post_type == 'Video':
        recommendations.append("🎥 Videos get great engagement - aim for under 60 seconds")
    elif post_type == 'Image':
        recommendations.append("📸 Images work well - use eye-catching visuals")
    elif post_type == 'Link':
        recommendations.append("🔗 Links reduce engagement - consider posting link in comments")
    elif post_type == 'Reel':
        recommendations.append("📱 Reels are trending - make them shareable")
    
    if clicks / impressions < 0.05:
        recommendations.append("💡 Low CTR - strengthen your hook/CTA")
    
    if reach < impressions * 1.1:
        recommendations.append("📢 Boost reach by posting at peak times (8-10 AM, 12-1 PM)")
    
    # Performance rating
    if engagement_score < 800:
        rating = "Low"
        emoji = "🔴"
    elif engagement_score < 1400:
        rating = "Medium"
        emoji = "🟡"
    else:
        rating = "High"
        emoji = "🟢"
    
    return {
        'engagement_score': round(engagement_score, 0),
        'rating': rating,
        'emoji': emoji,
        'post_type': post_type,
        'estimated_reactions': round(engagement_score * 0.7),
        'estimated_comments': round(engagement_score * 0.15),
        'estimated_shares': round(engagement_score * 0.03),
        'recommendations': recommendations
    }

def compare_post_types(month='May', impressions=1000, reach=1200, clicks=100):
    """Compare expected performance across different post types"""
    post_types = ['Text', 'Image', 'Video', 'Link', 'Reel']
    results = []
    
    for ptype in post_types:
        result = predict_post_performance(ptype, month, impressions, reach, clicks)
        results.append({
            'Post Type': ptype,
            'Engagement Score': result['engagement_score'],
            'Rating': result['rating']
        })
    
    df = pd.DataFrame(results).sort_values('Engagement Score', ascending=False)
    return df

if __name__ == "__main__":
    # Example prediction
    print("🔮 LinkedIn Post Performance Predictor\n")
    
    result = predict_post_performance(
        post_type='Video',
        month='February',
        impressions=5000,
        reach=6000,
        clicks=400
    )
    
    print(f"{result['emoji']} Predicted Engagement Score: {result['engagement_score']}")
    print(f"Rating: {result['rating']}\n")
    print(f"Expected Engagement:")
    print(f"  • Reactions: ~{result['estimated_reactions']}")
    print(f"  • Comments: ~{result['estimated_comments']}")
    print(f"  • Shares: ~{result['estimated_shares']}\n")
    print(f"Recommendations:")
    for rec in result['recommendations']:
        print(f"  {rec}")
    
    print("\n" + "="*60)
    print("\n📊 Comparison Across Post Types:\n")
    comparison = compare_post_types(month='February', impressions=5000, reach=6000, clicks=400)
    print(comparison.to_string(index=False))

