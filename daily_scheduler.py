#!/usr/bin/env python3
"""
Zero-Capital Income System: Daily Task Scheduler
30-Day implementation scheduler following the plan phases
"""

import json
from datetime import datetime, timedelta
from typing import List, Dict

class DailyScheduler:
    """Schedule and track daily tasks for the 30-day income program"""
    
    # 30-Day schedule from the plan
    SCHEDULE = {
        # Week 1: Foundation & Immediate Cash
        1: {"phase": "Foundation", "tasks": [
            "Create MTurk account (mturk.com)",
            "Create Appen account (appen.com)", 
            "Create Clickworker account (clickworker.com)",
            "Complete all qualification tests on MTurk",
            "Apply to 5+ projects on Appen"
        ], "goal": "$0 (setup phase)", "hours": 2},
        2: {"phase": "Foundation", "tasks": [
            "Complete MTurk demographic survey",
            "Take English Language qualification test",
            "Take Categorization qualification test",
            "Take Data Entry qualification test",
            "Check for approved tasks"
        ], "goal": "$0-3 (qualifications)", "hours": 3},
        3: {"phase": "Foundation", "tasks": [
            "Start microtasks on MTurk ($3-5 target)",
            "Check Appen for project invites",
            "Complete UHRS assessments on Clickworker",
            "Join TurkerView community",
            "Track first earnings"
        ], "goal": "$3-5", "hours": 4},
        4: {"phase": "Foundation", "tasks": [
            "Continue MTurk microtasks",
            "Apply to more Appen projects",
            "Set up email notifications for all platforms",
            "Research high-paying task types",
            "Aim for $3-5 daily"
        ], "goal": "$3-5", "hours": 4},
        5: {"phase": "Foundation", "tasks": [
            "Morning: 2 hours microtasks",
            "Afternoon: Set up Medium account",
            "Afternoon: Set up Vocal.Media account",
            "Evening: Apply to Partner Program",
            "Track daily earnings"
        ], "goal": "$3-5 + setup", "hours": 4},
        6: {"phase": "Foundation", "tasks": [
            "Morning: 2 hours microtasks",
            "Afternoon: Set up HubPages account",
            "Create profiles on all 3 content platforms",
            "Choose 2-3 niches to focus on",
            "Evening: Research trending topics"
        ], "goal": "$3-5", "hours": 4},
        7: {"phase": "Foundation", "tasks": [
            "Morning: 2 hours microtasks",
            "Create content calendar (30 topics)",
            "Set up Stripe for Medium payments",
            "Finalize niche selection",
            "Weekly review: Total earnings"
        ], "goal": "$15-35/week", "hours": 4},
        
        # Week 2: Content Machine Launch
        8: {"phase": "Content Launch", "tasks": [
            "Morning: 1 hour microtasks",
            "Generate first article outline (use content_generator.py)",
            "Write article #1 (900-1000 words)",
            "Publish to Vocal.Media",
            "Set up Kanban board for articles"
        ], "goal": "1 article published", "hours": 3},
        9: {"phase": "Content Launch", "tasks": [
            "Morning: 1 hour microtasks",
            "Write article #2",
            "Publish to Medium",
            "Research next 5 topics",
            "Join content creator communities"
        ], "goal": "2 articles", "hours": 3},
        10: {"phase": "Content Launch", "tasks": [
            "Morning: 1 hour microtasks",
            "Write article #3",
            "Publish to HubPages",
            "Cross-promote existing articles",
            "Engage with readers"
        ], "goal": "3 articles", "hours": 3},
        11: {"phase": "Content Launch", "tasks": [
            "Morning: 1 hour microtasks",
            "Write article #4",
            "Analyze which niches perform best",
            "Adjust content strategy",
            "Start social promotion"
        ], "goal": "4 articles", "hours": 3},
        12: {"phase": "Content Launch", "tasks": [
            "Morning: 1 hour microtasks",
            "Write article #5",
            "Research: Google Trends",
            "Create more outlines in advance",
            "Engage on social media"
        ], "goal": "5 articles", "hours": 3},
        13: {"phase": "Content Launch", "tasks": [
            "Morning: 1 hour microtasks",
            "Write article #6",
            "Pitch to Medium publications",
            "Network with other writers",
            "Check analytics"
        ], "goal": "6 articles", "hours": 3},
        14: {"phase": "Content Launch", "tasks": [
            "Morning: 1 hour microtasks",
            "Write article #7",
            "Week 2 review: Total earnings",
            "Analyze top performers",
            "Plan Week 3 content"
        ], "goal": "7-10 articles", "hours": 3},
        
        # Week 3: Freelance Outreach
        15: {"phase": "Freelance", "tasks": [
            "Morning: 1 hour microtasks",
            "Create service portfolio template",
            "Design 3 service offerings",
            "Set up LinkedIn profile (if not done)",
            "Prepare outreach messages"
        ], "goal": "Service portfolio ready", "hours": 3},
        16: {"phase": "Freelance", "tasks": [
            "Morning: 1 hour content/microtasks",
            "LinkedIn outreach: 20 contacts",
            "Twitter/X: 15 potential clients",
            "Research: Companies that need content",
            "Send first outreach emails"
        ], "goal": "50+ contacts", "hours": 3},
        17: {"phase": "Freelance", "tasks": [
            "Morning: 1 hour content/microtasks",
            "LinkedIn outreach: 20 more contacts",
            "Follow up with previous outreach",
            "Apply to Upwork/freelance jobs",
            "Create case study examples"
        ], "goal": "100+ contacts", "hours": 3},
        18: {"phase": "Freelance", "tasks": [
            "Morning: 1 hour content/microtasks",
            "Continue outreach",
            "First client follow-ups",
            "Prepare service delivery process",
            "Create invoice template"
        ], "goal": "First responses", "hours": 3},
        19: {"phase": "Freelance", "tasks": [
            "Morning: 1 hour content/microtasks",
            "Deliver first paid project",
            "Request testimonials",
            "Continue outreach",
            "Optimize pricing"
        ], "goal": "First $", "hours": 3},
        20: {"phase": "Freelance", "tasks": [
            "Morning: 1 hour content/microtasks",
            "Deliver second project",
            "Negotiate retainers",
            "Week 3 review",
            "Plan Week 4"
        ], "goal": "2-3 clients", "hours": 3},
        21: {"phase": "Freelance", "tasks": [
            "Morning: 1 hour content/microtasks",
            "Continue client work",
            "Scale outreach efforts",
            "Automate follow-ups",
            "Review financial progress"
        ], "goal": "$10-20/day", "hours": 3},
        
        # Week 4: Optimization & Scale
        22: {"phase": "Optimization", "tasks": [
            "Analyze top 5 performing articles",
            "Double down on winning niches",
            "Update content strategy",
            "Continue all revenue streams",
            "A/B test headlines"
        ], "goal": "Optimize", "hours": 3},
        23: {"phase": "Optimization", "tasks": [
            "Repurpose top content",
            "Update old articles with new info",
            "Build internal links",
            "Continue microtasks",
            "Client work"
        ], "goal": "Scale", "hours": 3},
        24: {"phase": "Optimization", "tasks": [
            "Pitch to bigger publications",
            "Negotiate higher rates",
            "Create retainer packages",
            "Systematize workflow",
            "Track everything"
        ], "goal": "Retainers", "hours": 3},
        25: {"phase": "Optimization", "tasks": [
            "Morning: Client work",
            "Afternoon: Content",
            "Evening: Outreach",
            "Review monthly goals",
            "Adjust strategy"
        ], "goal": "$15-20/day", "hours": 3},
        26: {"phase": "Optimization", "tasks": [
            "Focus on highest-earning activities",
            "Outsource repetitive tasks if viable",
            "Build passive income streams",
            "Month-end review prep",
            "Plan Month 2"
        ], "goal": "Optimize", "hours": 3},
        27: {"phase": "Optimization", "tasks": [
            "Complete month 1 review",
            "Document what worked",
            "Create Month 2 goals",
            "Automate where possible",
            "Celebrate wins!"
        ], "goal": "$15-25/day", "hours": 3},
        28: {"phase": "Scale", "tasks": [
            "Scale winning content strategy",
            "Add experiments new revenue",
            "Build content pipeline",
            "Continue client acquisition",
            "Month review"
        ], "goal": "Scale", "hours": 3},
        29: {"phase": "Scale", "tasks": [
            "Full speed ahead",
            "Focus on $20-30/day goal",
            "Systematize daily routine",
            "Create SOPs for workflow",
            "Plan long-term growth"
        ], "goal": "$20-30/day", "hours": 3},
        30: {"phase": "Scale", "tasks": [
            "30-Day celebration!",
            "Full month review",
            "Set Month 2 targets",
            "Reward yourself",
            "Plan next 30 days"
        ], "goal": "Sustain $15-30/day", "hours": 2}
    }
    
    def __init__(self):
        self.completed_tasks = []
        self.load_progress()
    
    def load_progress(self):
        """Load progress from file"""
        try:
            with open("progress.json", "r") as f:
                data = json.load(f)
                self.completed_tasks = data.get("completed_tasks", [])
            print(f"✓ Loaded progress: {len(self.completed_tasks)} days completed")
        except FileNotFoundError:
            self.completed_tasks = []
    
    def save_progress(self):
        """Save progress to file"""
        with open("progress.json", "w") as f:
            json.dump({"completed_tasks": self.completed_tasks}, f, indent=2)
    
    def get_today_tasks(self) -> Dict:
        """Get tasks for today based on day number"""
        # Calculate day number from start date
        # For simplicity, just use current day of month
        day = datetime.now().day
        if day > 30:
            day = 30
        return self.SCHEDULE.get(day, {"phase": "Complete", "tasks": [], "goal": "Done"})
    
    def get_day_tasks(self, day: int) -> Dict:
        """Get tasks for a specific day"""
        return self.SCHEDULE.get(day, {"phase": "Unknown", "tasks": [], "goal": "N/A"})
    
    def complete_day(self, day: int):
        """Mark a day as completed"""
        if day not in self.completed_tasks:
            self.completed_tasks.append(day)
            self.save_progress()
            print(f"✓ Day {day} marked as complete!")
        else:
            print(f"Day {day} already completed")
    
    def get_progress_percentage(self) -> float:
        """Get overall progress percentage"""
        return (len(self.completed_tasks) / 30) * 100
    
    def display_schedule(self):
        """Display the full 30-day schedule"""
        print("\n" + "=" * 70)
        print("ZERO-CAPITAL INCOME: 30-DAY SCHEDULE")
        print("=" * 70)
        
        phases = {}
        for day, info in self.SCHEDULE.items():
            phase = info["phase"]
            if phase not in phases:
                phases[phase] = []
            phases[phase].append((day, info))
        
        for phase, days in phases.items():
            print(f"\n{'=' * 30} {phase.upper()} {'=' * 30}")
            for day, info in days:
                status = "✓" if day in self.completed_tasks else " "
                print(f"\n{status} Day {day}: {info['goal']} ({info['hours']} hrs)")
                for task in info["tasks"]:
                    print(f"   - {task}")
        
        print("\n" + "=" * 70)
        print(f"OVERALL PROGRESS: {len(self.completed_tasks)}/30 days ({self.get_progress_percentage():.1f}%)")
        print("=" * 70)
    
    def display_today(self):
        """Display today's tasks"""
        today_info = self.get_today_tasks()
        day = datetime.now().day
        
        print("\n" + "=" * 60)
        print(f"📅 TODAY - Day {day}")
        print("=" * 60)
        print(f"Phase: {today_info['phase']}")
        print(f"Goal: {today_info['goal']}")
        print(f"Hours: {today_info['hours']}")
        print("\nTasks:")
        for i, task in enumerate(today_info["tasks"], 1):
            print(f"  {i}. {task}")
        print("=" * 60)


def main():
    """Interactive CLI for daily scheduler"""
    scheduler = DailyScheduler()
    
    # Show today's tasks
    scheduler.display_today()
    
    print("\nOptions:")
    print("  1. View full 30-day schedule")
    print("  2. Mark today as complete")
    print("  3. Mark a specific day complete")
    print("  4. View progress")
    print("  5. Exit")
    
    choice = input("\nEnter choice (1-5): ").strip()
    
    if choice == "1":
        scheduler.display_schedule()
    elif choice == "2":
        day = datetime.now().day
        scheduler.complete_day(day)
    elif choice == "3":
        day = int(input("Enter day number (1-30): "))
        scheduler.complete_day(day)
    elif choice == "4":
        print(f"\nProgress: {len(scheduler.completed_tasks)}/30 days ({scheduler.get_progress_percentage():.1f}%)")
    else:
        print("Goodbye!")


if __name__ == "__main__":
    main()
