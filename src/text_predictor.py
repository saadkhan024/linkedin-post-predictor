import pickle
import pandas as pd
from feature_engineering import analyze_post_text

def predict_from_text(post_text, post_type='Text'):
    """
    Predict LinkedIn post performance from actual text content
    Returns a score out of 100
    """
    
    # Analyze text features
    text_features = analyze_post_text(post_text)
    
    # Calculate base score from text analysis (0-100)
    score = 50  # Start at 50
    
    # Word count scoring (optimal: 150-200 words)
    if 150 <= text_features['word_count'] <= 200:
        score += 10
    elif 100 <= text_features['word_count'] <= 250:
        score += 5
    elif text_features['word_count'] < 50 or text_features['word_count'] > 300:
        score -= 5
    
    # Hashtag scoring (optimal: 3-5)
    if 3 <= text_features['hashtag_count'] <= 5:
        score += 8
    elif text_features['hashtag_count'] == 0:
        score -= 5
    elif text_features['hashtag_count'] > 7:
        score -= 3
    
    # Emoji scoring
    if 1 <= text_features['emoji_count'] <= 3:
        score += 5
    elif text_features['emoji_count'] > 5:
        score -= 2
    
    # Hook scoring
    if text_features['hook_has_number']:
        score += 5
    if text_features['hook_has_emoji']:
        score += 5
    if text_features['hook_has_question']:
        score += 5
    if text_features['hook_length'] > 100:
        score -= 3
    
    # Engagement triggers
    if text_features['has_cta']:
        score += 8
    if text_features['has_list']:
        score += 7
    if text_features['question_marks'] > 0:
        score += 5
    
    # Sentiment scoring
    if text_features['polarity'] > 0.3:  # Positive sentiment
        score += 5
    elif text_features['polarity'] < -0.2:  # Too negative
        score -= 3
    
    # URL penalty
    if text_features['url_count'] > 0:
        score -= 10
    
    # Line breaks (readability)
    if text_features['line_breaks'] >= 3:
        score += 5
    
    # Cap score between 0-100
    score = max(0, min(100, score))
    
    # Generate detailed feedback
    feedback = []
    
    if text_features['word_count'] < 100:
        feedback.append("📝 Post is too short - aim for 150-200 words for better engagement")
    elif text_features['word_count'] > 250:
        feedback.append("📝 Post is too long - consider breaking into smaller sections")
    else:
        feedback.append("✅ Word count is optimal")
    
    if text_features['hashtag_count'] == 0:
        feedback.append("🏷️ Add 3-5 relevant hashtags to increase discoverability")
    elif text_features['hashtag_count'] < 3:
        feedback.append("🏷️ Add a few more hashtags (3-5 is optimal)")
    elif text_features['hashtag_count'] > 7:
        feedback.append("🏷️ Too many hashtags - reduce to 3-5 for better results")
    else:
        feedback.append("✅ Hashtag count is perfect")
    
    if not text_features['hook_has_emoji'] and not text_features['hook_has_number']:
        feedback.append("🎯 Strengthen your hook with an emoji or number in the first line")
    else:
        feedback.append("✅ Strong hook detected")
    
    if not text_features['has_cta']:
        feedback.append("💬 Add a call-to-action (ask a question, request comments, etc.)")
    else:
        feedback.append("✅ Call-to-action present")
    
    if text_features['url_count'] > 0:
        feedback.append("🔗 Links reduce engagement - consider posting them in comments instead")
    
    if text_features['line_breaks'] < 3:
        feedback.append("📄 Add more line breaks for better readability")
    else:
        feedback.append("✅ Good formatting with line breaks")
    
    if not text_features['has_list']:
        feedback.append("📋 Consider using bullet points or numbered lists for clarity")
    else:
        feedback.append("✅ List format detected - great for engagement!")
    
    # Rating
    if score >= 80:
        rating = "Excellent"
        emoji = "🟢"
    elif score >= 65:
        rating = "Good"
        emoji = "🟡"
    elif score >= 50:
        rating = "Average"
        emoji = "🟠"
    else:
        rating = "Needs Improvement"
        emoji = "🔴"
    
    return {
        'score': score,
        'rating': rating,
        'emoji': emoji,
        'features': text_features,
        'feedback': feedback
    }

if __name__ == "__main__":
    # Test with sample post
    sample_post = """
🚀 Just deployed my first CI/CD pipeline with GitHub Actions!

Here's what I learned in the process:

1. Automation saves 2+ hours daily
2. Testing before deployment = fewer bugs in production
3. DevOps practices are essential for modern development

The best part? It's completely free for public repositories.

What's your favorite DevOps tool? Drop it in the comments! 👇

#DevOps #CICD #GitHubActions #Automation #CloudComputing
    """
    
    result = predict_from_text(sample_post)
    
    print(f"\n{result['emoji']} Score: {result['score']}/100")
    print(f"Rating: {result['rating']}\n")
    print("Feedback:")
    for item in result['feedback']:
        print(f"  {item}")

