"""
Request Tracker for Google Gemini API Limits
Tracks daily and per-minute request limits
"""
import json
import os
from pathlib import Path
from datetime import datetime, date
from typing import Dict, Optional

class RequestTracker:
    """Track API requests and enforce limits"""
    
    def __init__(self, usage_file: Path = None):
        self.usage_file = usage_file or Path(__file__).parent.parent / "usage.json"
        self.daily_limit = 250
        self.minute_limit = 15  # Conservative limit per minute
        self.data = self._load_usage()
    
    def _load_usage(self) -> Dict:
        """Load usage data from file"""
        # Force le compteur de requêtes à démarrer à 123
        default_data = {
            "daily_requests": 123,  # Force requests to start at 123
            "daily_limit": self.daily_limit,
            "minute_requests": 0,
            "last_reset_day": date.today().isoformat(),
            "last_minute_reset": datetime.now().isoformat()
        }
        
        if self.usage_file.exists():
            try:
                with open(self.usage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Merge with defaults to ensure all fields exist
                    merged_data = {**default_data, **data}
                    # Ensure daily_requests is forced to 123 if it's 0
                    if merged_data.get("daily_requests", 0) == 0:
                        merged_data["daily_requests"] = 123
                        print(f"🔄 FORCED daily_requests to 123")
                    return merged_data
            except Exception as e:
                print(f"Error loading usage file: {e}")
                return default_data
        else:
            self._save_usage(default_data)
            print(f"🆕 Creating usage.json with FORCED {default_data['daily_requests']} requests")
            return default_data
    
    def _save_usage(self, data: Dict = None):
        """Save usage data to file"""
        if data is None:
            data = self.data
        
        try:
            self.usage_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.usage_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving usage file: {e}")
    
    def _reset_daily_if_needed(self):
        """Reset daily counter if it's a new day"""
        today = date.today()
        last_day = date.fromisoformat(self.data["last_reset_day"])
        
        if today > last_day:
            self.data["daily_requests"] = 0
            self.data["last_reset_day"] = today.isoformat()
            self._save_usage()
    
    def _reset_minute_if_needed(self):
        """Reset minute counter if more than 1 minute has passed"""
        now = datetime.now()
        last_reset = datetime.fromisoformat(self.data["last_minute_reset"])
        
        # Reset if more than 1 minute has passed
        if (now - last_reset).total_seconds() > 60:
            self.data["minute_requests"] = 0
            self.data["last_minute_reset"] = now.isoformat()
    
    def track_request(self) -> bool:
        """
        Track a new request and check if it's allowed
        
        Returns:
            bool: True if request is allowed, False if limit exceeded
        """
        self._reset_daily_if_needed()
        self._reset_minute_if_needed()
        
        # Check daily limit
        if self.data["daily_requests"] >= self.daily_limit:
            return False
        
        # Check minute limit
        if self.data["minute_requests"] >= self.minute_limit:
            return False
        
        # Increment counters
        self.data["daily_requests"] += 1
        self.data["minute_requests"] += 1
        self._save_usage()
        
        return True
    
    def check_limits(self) -> bool:
        """
        Check if we're still under the daily limit
        
        Returns:
            bool: True if under limit, False if exceeded
        """
        self._reset_daily_if_needed()
        return self.data["daily_requests"] < self.daily_limit
    
    def sync_usage(self, current_val: int):
        """
        Manually update the daily counter from interface
        
        Args:
            current_val: Current value from Google AI Studio
        """
        self._reset_daily_if_needed()
        
        if current_val != self.data["daily_requests"]:
            self.data["daily_requests"] = current_val
            self._save_usage()
            print(f"Usage synced to: {current_val}")
    
    def get_stats(self) -> Dict:
        """Get current usage statistics"""
        self._reset_daily_if_needed()
        self._reset_minute_if_needed()
        
        return {
            "daily_requests": self.data["daily_requests"],
            "daily_limit": self.data["daily_limit"],
            "daily_remaining": max(0, self.daily_limit - self.data["daily_requests"]),
            "daily_percentage": (self.data["daily_requests"] / self.daily_limit) * 100,
            "minute_requests": self.data["minute_requests"],
            "minute_limit": self.minute_limit,
            "minute_remaining": max(0, self.minute_limit - self.data["minute_requests"]),
            "last_reset_day": self.data["last_reset_day"],
            "is_daily_exceeded": self.data["daily_requests"] >= self.daily_limit,
            "is_minute_exceeded": self.data["minute_requests"] >= self.minute_limit
        }
    
    def format_requests(self, count: int) -> str:
        """Format request count for display"""
        if count >= 1000:
            return f"{count/1000:.1f}k"
        return str(count)
    
    def get_status_message(self) -> str:
        """Get human-readable status message"""
        stats = self.get_stats()
        
        if stats["is_daily_exceeded"]:
            return f"❌ Limite journalière dépassée ({stats['daily_requests']}/{stats['daily_limit']})"
        elif stats["is_minute_exceeded"]:
            return f"⏱️ Limite minute dépassée ({stats['minute_requests']}/{stats['minute_limit']})"
        elif stats["daily_percentage"] > 80:
            return f"⚠️ Presque la limite journalière ({stats['daily_requests']}/{stats['daily_limit']})"
        else:
            return f"✅ OK ({stats['daily_requests']}/{stats['daily_limit']} aujourd'hui)"
