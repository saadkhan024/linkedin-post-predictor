#!/usr/bin/env python3
"""
LinkedIn Post Performance Predictor - CLI Tool
"""

import sys
sys.path.append('src')
from predictor import predict_post_performance, compare_post_types

def main():
    print("=" * 60)
    print("🔮 LinkedIn Post Performance Predictor")
    print("=" * 60)
    print()
    
    # Get user input
    print("Post Types: Text, Image, Video, Link, Reel")
    post_type = input("Enter post type (default: Video): ").strip() or "Video"
    
    print("\nMonths: January, February, March, April, May, etc.")
    month = input("Enter month (default: February): ").strip() or "February"
    
    impressions = input("\nExpected impressions (default: 5000): ").strip()
    impressions = int(impressions) if impressions else 5000
    
    reach = input("Expected reach (default: 6000): ").strip()
    reach = int(reach) if reach else 6000
    
    clicks = input("Expected clicks (default: 400): ").strip()
    clicks = int(clicks) if clicks else 400
    
    print("\n" + "=" * 60)
    print("📊 PREDICTION RESULTS")
    print("=" * 60)
    
    # Get prediction
    result = predict_post_performance(post_type, month, impressions, reach, clicks)
    
    print(f"\n{result['emoji']} Engagement Score: {result['engagement_score']:.0f}")
    print(f"Performance Rating: {result['rating']}")
    print(f"\n📈 Expected Engagement Breakdown:")
    print(f"  • Reactions: ~{result['estimated_reactions']}")
    print(f"  • Comments: ~{result['estimated_comments']}")
    print(f"  • Shares: ~{result['estimated_shares']}")
    
    print(f"\n💡 Recommendations:")
    for rec in result['recommendations']:
        print(f"  {rec}")
    
    print("\n" + "=" * 60)
    
    # Ask if user wants comparison
    compare = input("\nCompare all post types? (y/n): ").strip().lower()
    if compare == 'y':
        print("\n📊 Performance Comparison Across All Post Types:\n")
        comparison = compare_post_types(month, impressions, reach, clicks)
        print(comparison.to_string(index=False))
        print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
