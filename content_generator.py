#!/usr/bin/env python3
"""
Zero-Capital Income System: Content Generator
AI-Powered Article Outline Generator for Medium, Vocal, and HubPages
"""

import json
import random
from datetime import datetime
from typing import List, Dict

class ContentGenerator:
    """Generate article outlines and content ideas for revenue-sharing platforms"""
    
    # High-earning niches from the plan
    NICHES = {
        "personal_finance": [
            "Save $1000 This Month", "Passive Income Ideas", "Budgeting Tips",
            "Emergency Fund Guide", "Side Hustle Money", "Financial Freedom",
            "Investment Basics", "Debt Payoff Strategy", "Frugal Living",
            "Money Management"
        ],
        "technology_ai": [
            "AI Tools 2025", "ChatGPT Tips", "Make Money with AI",
            "Tech Side Hustles", "Digital Nomad", "Remote Work",
            "Automation Tips", "Best AI Apps", "Productivity Hacks",
            "Future of Work"
        ],
        "health_wellness": [
            "Weight Loss Tips", "Morning Routine", "Mental Health",
            "Exercise at Home", "Healthy Eating", "Sleep Better",
            "Stress Relief", "Mindfulness Guide", "Energy Boost",
            "Wellness Habits"
        ],
        "self_improvement": [
            "Self Discipline", "Goal Setting", "Habit Formation",
            "Time Management", "Morning Motivation", "Success Mindset",
            "Productivity Hacks", "Focus Tips", "Life Improvement",
            "Personal Growth"
        ],
        "side_hustles": [
            "Make Money Online", "Freelance Tips", "Extra Income",
            "Side Hustle Ideas", "Passive Income", "Online Business",
            "Work From Home", "Gig Economy", "Independent Work",
            "Money Making Tips"
        ]
    }
    
    # Article templates
    TEMPLATES = {
        "listicle_7": {
            "name": "7-Point Listicle",
            "format": "7 {topic} Strategies That {benefit} in 2025",
            "structure": [
                "Hook with statistic or trend",
                "Brief introduction (150 words)",
                "7 points with 100 words each",
                "Conclusion with CTA (100 words)"
            ],
            "target_length": "900-1000 words"
        },
        "howto": {
            "name": "How-To Guide",
            "format": "How to {benefit} in 30 Days",
            "structure": [
                "Problem statement",
                "Why it matters",
                "Step-by-step guide",
                "Common mistakes to avoid",
                "Final tips and encouragement"
            ],
            "target_length": "1200-1500 words"
        },
        "comparison": {
            "name": "Comparison Guide",
            "format": "{Tool A} vs {Tool B}: Which is Better for {use_case}?",
            "structure": [
                "Introduction to both tools",
                "Feature comparison table",
                "Pros and cons of each",
                "Best use cases",
                "My recommendation"
            ],
            "target_length": "1000-1200 words"
        },
        "beginner": {
            "name": "Beginner's Guide",
            "format": "The Complete Beginner's Guide to {topic}",
            "structure": [
                "What is {topic}?",
                "Why should you care?",
                "Getting started",
                "Common pitfalls",
                "Next steps"
            ],
            "target_length": "1500-2000 words"
        }
    }
    
    def __init__(self):
        self.generated_articles = []
    
    def generate_outline(self, niche: str, template: str, custom_topic: str = None) -> Dict:
        """Generate a complete article outline"""
        
        # Get niche topics
        topics = self.NICHES.get(niche, self.NICHES["side_hustles"])
        topic = custom_topic if custom_topic else random.choice(topics)
        
        # Get template
        temp = self.TEMPLATES.get(template, self.TEMPLATES["listicle_7"])
        
        # Generate benefits
        benefits = [
            "Save You Money", "Boost Your Income", "Improve Your Life",
            "Increase Your Productivity", "Help You Succeed", "Change Your Mindset",
            "Double Your Results", "Accelerate Your Growth"
        ]
        benefit = random.choice(benefits)
        
        # Create title
        title = temp["format"].format(
            topic=topic,
            benefit=benefit,
            Tool A="Tool A",
            Tool B="Tool B",
            use_case="beginners"
        )
        
        # Build outline
        outline = {
            "title": title,
            "niche": niche,
            "template": temp["name"],
            "target_length": temp["target_length"],
            "structure": [],
            "seo_keywords": self._generate_keywords(topic),
            "created_at": datetime.now().isoformat()
        }
        
        # Add structure points
        for i, section in enumerate(temp["structure"], 1):
            outline["structure"].append({
                "section": i,
                "description": section,
                "word_count_estimate": self._estimate_words(section, temp["target_length"])
            })
        
        self.generated_articles.append(outline)
        return outline
    
    def _generate_keywords(self, topic: str) -> List[str]:
        """Generate SEO keywords for the topic"""
        base_keywords = [topic.lower(), f"how to {topic.lower()}"]
        
        modifiers = ["2025", "tips", "guide", "for beginners", "strategy"]
        keywords = [f"{topic.lower()} {mod}" for mod in modifiers]
        
        return base_keywords + keywords
    
    def _estimate_words(self, section: str, target: str) -> int:
        """Estimate word count for a section"""
        if "introduction" in section.lower() or "hook" in section.lower():
            return 150
        elif "conclusion" in section.lower() or "cta" in section.lower():
            return 100
        elif "step" in section.lower():
            return 200
        else:
            return 150
    
    def batch_generate(self, count: int = 5, niche: str = None) -> List[Dict]:
        """Generate multiple article outlines"""
        articles = []
        niches = [niche] if niche else list(self.NICHES.keys())
        
        for i in range(count):
            selected_niche = random.choice(niches)
            template = random.choice(list(self.TEMPLATES.keys()))
            article = self.generate_outline(selected_niche, template)
            articles.append(article)
        
        return articles
    
    def save_to_file(self, filename: str = "generated_articles.json"):
        """Save generated articles to JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.generated_articles, f, indent=2)
        print(f"✓ Saved {len(self.generated_articles)} articles to {filename}")


def main():
    """Interactive CLI for generating content"""
    generator = ContentGenerator()
    
    print("=" * 60)
    print("ZERO-CAPITAL INCOME: Content Generator")
    print("=" * 60)
    print()
    
    # Select niche
    print("Available Niches:")
    for i, niche in enumerate(ContentGenerator.NICHES.keys(), 1):
        print(f"  {i}. {niche.replace('_', ' ').title()}")
    print()
    
    # Generate sample articles
    print("Generating 10 article outlines...\n")
    articles = generator.batch_generate(count=10)
    
    for i, article in enumerate(articles, 1):
        print(f"Article {i}:")
        print(f"  Title: {article['title']}")
        print(f"  Niche: {article['niche'].replace('_', ' ').title()}")
        print(f"  Template: {article['template']}")
        print(f"  Length: {article['target_length']}")
        print(f"  Keywords: {', '.join(article['seo_keywords'][:3])}...")
        print()
    
    # Save to file
    generator.save_to_file()
    print("\n✓ Content generation complete!")
    print("\nNext steps:")
    print("  1. Pick an article outline above")
    print("  2. Write the content (use AI to assist)")
    print("  3. Publish to Medium, Vocal, and HubPages")
    print("  4. Track your earnings!")


if __name__ == "__main__":
    main()
