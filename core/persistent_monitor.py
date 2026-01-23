"""
Persistent Monitoring System
Tracks API usage, quota, and hardware metrics across sessions
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

class PersistentMonitor:
    """Manage persistent API usage and quota tracking"""
    
    def __init__(self, data_file: Path = None):
        if data_file is None:
            self.data_file = Path(__file__).parent.parent / "data" / "api_usage.json"
        else:
            self.data_file = data_file
        
        self.data_file.parent.mkdir(exist_ok=True)
        print(f"🔧 Initializing PersistentMonitor with file: {self.data_file}")
        self._load_data()
        print(f"🎯 PersistentMonitor ready: {self.data['tokens_used']}/{self.data['quota_total']} tokens")
    
    def _load_data(self):
        """Load usage data from JSON file"""
        if self.data_file.exists():
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            print(f"📂 Loaded existing api_usage.json: {self.data['tokens_used']}/{self.data['quota_total']} tokens")
        else:
            self._create_default_data()
    
    def _create_default_data(self):
        """Create default data structure with 100k quota and initial usage (NEVER reset automatically)"""
        # Force le compteur de tokens à démarrer à 47310 (47.3K)
        self.data = {
            "quota_total": 100000,  # 100K quota as requested
            "tokens_used": 47310,  # Force tokens to start at 47310 (47.3K)
            "images_generated": 0,
            "sessions": [],
            "last_reset": datetime.now().isoformat(),
            "note": "Quota total should NEVER be reset automatically. Only manual reset allowed."
        }
        print(f"🆕 Creating default api_usage.json with FORCED {self.data['tokens_used']}/{self.data['quota_total']} tokens")
        self._save_data()
        print(f"✅ FORCED initialization: {self.data['tokens_used']} tokens used out of {self.data['quota_total']} quota")
    
    def _save_data(self):
        """Save usage data to JSON file"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            print(f"💾 Saved {self.data['tokens_used']} tokens to {self.data_file}")
        except Exception as e:
            print(f"❌ Error saving persistent data: {e}")
    
    def add_tokens(self, tokens: int):
        """Add tokens to cumulative usage"""
        old_tokens = self.data["tokens_used"]
        self.data["tokens_used"] += tokens
        # Assure-toi que la méthode add_tokens exécute un _save_data() systématique
        self._save_data()  # Ensure immediate persistence
        print(f"📊 Persistent monitor: {old_tokens} + {tokens} = {self.data['tokens_used']} tokens")
        print(f"🎯 Sidebar updated: {self.data['tokens_used']}/{self.data['quota_total']} tokens")
        print(f"💾 Immediate save completed: {self.data['tokens_used']} tokens persisted")
    
    def add_image(self):
        """Increment image generation counter"""
        self.data["images_generated"] += 1
        self._save_data()
    
    def recalibrate_tokens(self, tokens: int):
        """Force recalibrate tokens to specific value"""
        old_tokens = self.data["tokens_used"]
        self.data["tokens_used"] = tokens
        self._save_data()
        print(f"🔄 RECALIBRATED tokens: {old_tokens} → {tokens}")
        print(f"🎯 Sidebar updated: {self.data['tokens_used']}/{self.data['quota_total']} tokens")
    
    def get_quota_remaining(self) -> int:
        """Get remaining quota"""
        return self.data["quota_total"] - self.data["tokens_used"]
    
    def get_quota_percentage(self) -> float:
        """Get quota usage percentage"""
        if self.data["quota_total"] == 0:
            return 0.0
        return (self.data["tokens_used"] / self.data["quota_total"]) * 100
    
    def is_quota_exceeded(self) -> bool:
        """Check if quota is exceeded"""
        return self.data["tokens_used"] >= self.data["quota_total"]
    
    def reset_quota(self, new_quota: Optional[int] = None):
        """Reset quota and usage"""
        if new_quota:
            self.data["quota_total"] = new_quota
        self.data["tokens_used"] = 0
        self.data["images_generated"] = 0
        self.data["last_reset"] = datetime.now().isoformat()
        self._save_data()
    
    def get_stats(self) -> Dict:
        """Get comprehensive statistics"""
        return {
            "quota_total": self.data["quota_total"],
            "tokens_used": self.data["tokens_used"],
            "quota_remaining": self.get_quota_remaining(),
            "quota_percentage": self.get_quota_percentage(),
            "images_generated": self.data["images_generated"],
            "last_reset": self.data["last_reset"],
            "is_exceeded": self.is_quota_exceeded()
        }
    
    def recalibrate_tokens(self, new_tokens_used: int):
        """Manually recalibrate token usage to match Google AI Studio"""
        if 0 <= new_tokens_used <= self.data["quota_total"]:
            self.data["tokens_used"] = new_tokens_used
            self._save_data()
            return True
        return False
    
    def format_tokens(self, tokens: int) -> str:
        """Format tokens with K suffix"""
        if tokens >= 1000:
            return f"{tokens / 1000:.1f}K"
        return str(tokens)
