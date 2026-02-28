#!/usr/bin/env python3
"""
Zero-Capital Income System: Earnings Tracker
Track income from MTurk, Appen, Clickworker, Medium, Vocal, HubPages, and Freelance
"""

import json
import csv
from datetime import datetime, timedelta
from typing import List, Dict
from collections import defaultdict

class EarningsTracker:
    """Track earnings across all income streams"""
    
    PLATFORMS = {
        "mturk": {"name": "Amazon MTurk", "type": "microtask", "min_hourly": 3.0, "max_hourly": 10.0},
        "appen": {"name": "Appen", "type": "microtask", "min_hourly": 3.0, "max_hourly": 20.0},
        "clickworker": {"name": "Clickworker", "type": "microtask", "min_hourly": 3.0, "max_hourly": 10.0},
        "medium": {"name": "Medium", "type": "content", "min_daily": 0.0, "max_daily": 5.0},
        "vocal": {"name": "Vocal.Media", "type": "content", "min_daily": 0.0, "max_daily": 10.0},
        "hubpages": {"name": "HubPages", "type": "content", "min_daily": 0.0, "max_daily": 3.0},
        "freelance": {"name": "Freelance", "type": "service", "min_daily": 0.0, "max_daily": 30.0}
    }
    
    def __init__(self):
        self.earnings = []
        self.load_earnings()
    
    def load_earnings(self):
        """Load existing earnings from file"""
        try:
            with open("earnings_data.json", "r") as f:
                self.earnings = json.load(f)
            print(f"✓ Loaded {len(self.earnings)} existing records")
        except FileNotFoundError:
            self.earnings = []
            print("Starting fresh - no existing data found")
    
    def save_earnings(self):
        """Save earnings to file"""
        with open("earnings_data.json", "w") as f:
            json.dump(self.earnings, f, indent=2)
        print(f"✓ Saved {len(self.earnings)} records")
    
    def add_earning(self, platform: str, amount: float, date: str = None, 
                   hours: float = None, notes: str = ""):
        """Add a new earning record"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        record = {
            "id": len(self.earnings) + 1,
            "platform": platform,
            "amount": amount,
            "date": date,
            "hours": hours,
            "notes": notes,
            "created_at": datetime.now().isoformat()
        }
        
        self.earnings.append(record)
        self.save_earnings()
        print(f"✓ Added ${amount:.2f} from {platform}")
    
    def get_daily_summary(self, date: str = None) -> Dict:
        """Get summary for a specific date"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        day_earnings = [e for e in self.earnings if e["date"] == date]
        
        total = sum(e["amount"] for e in day_earnings)
        by_platform = defaultdict(float)
        
        for e in day_earnings:
            by_platform[e["platform"]] += e["amount"]
        
        return {
            "date": date,
            "total": total,
            "by_platform": dict(by_platform),
            "records": len(day_earnings)
        }
    
    def get_weekly_summary(self) -> Dict:
        """Get summary for the current week"""
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        
        week_earnings = [
            e for e in self.earnings 
            if datetime.strptime(e["date"], "%Y-%m-%d") >= week_start
        ]
        
        total = sum(e["amount"] for e in week_earnings)
        by_platform = defaultdict(float)
        
        for e in week_earnings:
            by_platform[e["platform"]] += e["amount"]
        
        return {
            "week_start": week_start.strftime("%Y-%m-%d"),
            "week_end": today.strftime("%Y-%m-%d"),
            "total": total,
            "daily_average": total / 7,
            "by_platform": dict(by_platform),
            "records": len(week_earnings)
        }
    
    def get_monthly_summary(self, year: int = None, month: int = None) -> Dict:
        """Get summary for a specific month"""
        if year is None:
            year = datetime.now().year
        if month is None:
            month = datetime.now().month
        
        month_str = f"{year}-{month:02d}"
        month_earnings = [e for e in self.earnings if e["date"].startswith(month_str)]
        
        total = sum(e["amount"] for e in month_earnings)
        by_platform = defaultdict(float)
        
        for e in month_earnings:
            by_platform[e["platform"]] += e["amount"]
        
        days_in_month = 31  # Simplified
        daily_avg = total / days_in_month
        
        return {
            "year": year,
            "month": month,
            "month_str": month_str,
            "total": total,
            "daily_average": daily_avg,
            "by_platform": dict(by_platform),
            "records": len(month_earnings)
        }
    
    def get_all_time_summary(self) -> Dict:
        """Get all-time earnings summary"""
        if not self.earnings:
            return {"total": 0, "by_platform": {}, "records": 0}
        
        total = sum(e["amount"] for e in self.earnings)
        by_platform = defaultdict(float)
        
        for e in self.earnings:
            by_platform[e["platform"]] += e["amount"]
        
        # Calculate by revenue stream type
        by_type = defaultdict(float)
        for platform, amount in by_platform.items():
            ptype = self.PLATFORMS.get(platform, {}).get("type", "other")
            by_type[ptype] += amount
        
        return {
            "total": total,
            "by_platform": dict(by_platform),
            "by_type": dict(by_type),
            "records": len(self.earnings)
        }
    
    def export_to_csv(self, filename: str = "earnings_export.csv"):
        """Export all earnings to CSV"""
        if not self.earnings:
            print("No earnings to export")
            return
        
        fieldnames = ["id", "platform", "amount", "date", "hours", "notes", "created_at"]
        
        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.earnings)
        
        print(f"✓ Exported {len(self.earnings)} records to {filename}")
    
    def display_dashboard(self):
        """Display a dashboard summary"""
        print("\n" + "=" * 60)
        print("ZERO-CAPITAL INCOME: EARNINGS DASHBOARD")
        print("=" * 60)
        
        # Today's summary
        daily = self.get_daily_summary()
        print(f"\n📅 TODAY ({daily['date']})")
        print(f"   Total: ${daily['total']:.2f}")
        print(f"   Records: {daily['records']}")
        
        # Weekly summary
        weekly = self.get_weekly_summary()
        print(f"\n📆 THIS WEEK ({weekly['week_start']} to {weekly['week_end']})")
        print(f"   Total: ${weekly['total']:.2f}")
        print(f"   Daily Average: ${weekly['daily_average']:.2f}")
        
        # Monthly summary
        monthly = self.get_monthly_summary()
        print(f"\n📆 THIS MONTH ({monthly['month_str']})")
        print(f"   Total: ${monthly['total']:.2f}")
        print(f"   Daily Average: ${monthly['daily_average']:.2f}")
        
        # All-time summary
        alltime = self.get_all_time_summary()
        print(f"\n💰 ALL-TIME TOTAL")
        print(f"   Total: ${alltime['total']:.2f}")
        print(f"   Records: {alltime['records']}")
        
        print("\n📊 By Platform:")
        for platform, amount in sorted(alltime.get("by_platform", {}).items(), 
                                      key=lambda x: x[1], reverse=True):
            name = self.PLATFORMS.get(platform, {}).get("name", platform)
            print(f"   {name}: ${amount:.2f}")
        
        print("\n📊 By Type:")
        for ptype, amount in alltime.get("by_type", {}).items():
            print(f"   {ptype.title()}: ${amount:.2f}")
        
        print("\n" + "=" * 60)


def main():
    """Interactive CLI for earnings tracking"""
    tracker = EarningsTracker()
    
    # Display dashboard
    tracker.display_dashboard()
    
    # Interactive menu
    while True:
        print("\nChoose an option:")
        print("  1. Add new earning")
        print("  2. View today's summary")
        print("  3. View weekly summary")
        print("  4. View monthly summary")
        print("  5. Export to CSV")
        print("  6. Add sample data (for testing)")
        print("  7. Quit")
        
        choice = input("\nEnter choice (1-7): ").strip()
        
        if choice == "1":
            print("\nAvailable platforms:")
            for key, val in tracker.PLATFORMS.items():
                print(f"  {key}: {val['name']}")
            
            platform = input("Platform: ").strip().lower()
            amount = float(input("Amount ($): "))
            date = input("Date (YYYY-MM-DD, empty for today): ").strip()
            hours = input("Hours worked (optional): ").strip()
            notes = input("Notes (optional): ").strip()
            
            tracker.add_earning(
                platform=platform,
                amount=amount,
                date=date if date else None,
                hours=float(hours) if hours else None,
                notes=notes
            )
        
        elif choice == "2":
            daily = tracker.get_daily_summary()
            print(f"\nToday: ${daily['total']:.2f}")
        
        elif choice == "3":
            weekly = tracker.get_weekly_summary()
            print(f"\nThis Week: ${weekly['total']:.2f} (avg ${weekly['daily_average']:.2f}/day)")
        
        elif choice == "4":
            monthly = tracker.get_monthly_summary()
            print(f"\nThis Month: ${monthly['total']:.2f} (avg ${monthly['daily_average']:.2f}/day)")
        
        elif choice == "5":
            tracker.export_to_csv()
        
        elif choice == "6":
            # Add sample data for the past 7 days
            import random
            for i in range(7):
                date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
                tracker.add_earning("mturk", round(random.uniform(3, 8), 2), date)
                tracker.add_earning("vocal", round(random.uniform(0.5, 3), 2), date)
            
            print("✓ Added sample data for the past 7 days")
        
        elif choice == "7":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
