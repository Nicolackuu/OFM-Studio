"""
Token Usage & Cost Tracker for Google Gemini API
Tracks input/output tokens and calculates costs per session
"""
import json
import os
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime

class UsageTracker:
    """Track API usage and costs for Gemini"""
    
    # Gemini API Pricing (as of 2026)
    COST_INPUT_PER_1M = 1.25  # $ per 1M input tokens
    COST_OUTPUT_PER_1M = 3.75  # $ per 1M output tokens
    COST_IMAGE_GEN = 0.03  # $ per image generation
    
    def __init__(self):
        self.usage_file = Path(__file__).parent.parent / "usage.json"
        self.reset()
        self._load_usage()
    
    def reset(self):
        """Reset all counters"""
        self.input_tokens = 0
        self.output_tokens = 0
        self.images_generated = 0
        self.session_start = datetime.now()
    
    def _load_usage(self):
        """Load usage data from file"""
        default_data = {
            "total_tokens": 47310,  # Valeur de départ de l'utilisateur
            "input_tokens": 0,
            "output_tokens": 0,
            "images_generated": 0,
            "last_updated": datetime.now().isoformat()
        }
        
        if self.usage_file.exists():
            try:
                with open(self.usage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Ensure all fields exist
                    return {**default_data, **data}
            except Exception as e:
                print(f"Error loading usage file: {e}")
                return default_data
        else:
            self._save_usage(default_data)
            return default_data
    
    def _save_usage(self, data: Dict = None):
        """Save usage data to file"""
        if data is None:
            data = {
                "total_tokens": self.get_total_tokens(),
                "input_tokens": self.input_tokens,
                "output_tokens": self.output_tokens,
                "images_generated": self.images_generated,
                "last_updated": datetime.now().isoformat()
            }
        
        try:
            self.usage_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.usage_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving usage file: {e}")
    
    def add_tokens(self, input_tokens: int = 0, output_tokens: int = 0):
        """
        Add tokens to the counter
        
        Args:
            input_tokens: Number of input tokens used
            output_tokens: Number of output tokens generated
        """
        self.input_tokens += input_tokens
        self.output_tokens += output_tokens
        self._save_usage()
    
    def update_usage(self, tokens_used: int):
        """
        Update total tokens directly (for precise tracking)
        
        Args:
            tokens_used: Total tokens used in the API call
        """
        self.total_tokens = tokens_used
        self._save_usage()
    
    def add_image(self):
        """Increment image generation counter"""
        self.images_generated += 1
    
    def get_input_cost(self) -> float:
        """Calculate cost for input tokens"""
        return (self.input_tokens / 1_000_000) * self.COST_INPUT_PER_1M
    
    def get_output_cost(self) -> float:
        """Calculate cost for output tokens"""
        return (self.output_tokens / 1_000_000) * self.COST_OUTPUT_PER_1M
    
    def get_image_cost(self) -> float:
        """Calculate cost for image generations"""
        return self.images_generated * self.COST_IMAGE_GEN
    
    def get_total_cost(self) -> float:
        """Calculate total session cost"""
        return self.get_input_cost() + self.get_output_cost() + self.get_image_cost()
    
    def get_total_tokens(self) -> int:
        """Get total tokens (input + output)"""
        # Load from persistent storage to get current value
        try:
            if self.usage_file.exists():
                with open(self.usage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('total_tokens', self.input_tokens + self.output_tokens)
        except:
            pass
        return self.input_tokens + self.output_tokens
    
    def get_stats(self) -> Dict:
        """
        Get comprehensive usage statistics
        
        Returns:
            Dictionary with all stats
        """
        return {
            'input_tokens': self.input_tokens,
            'output_tokens': self.output_tokens,
            'total_tokens': self.get_total_tokens(),
            'images_generated': self.images_generated,
            'input_cost': self.get_input_cost(),
            'output_cost': self.get_output_cost(),
            'image_cost': self.get_image_cost(),
            'total_cost': self.get_total_cost(),
            'session_duration': (datetime.now() - self.session_start).total_seconds() / 60  # minutes
        }
    
    def format_cost(self, cost: float) -> str:
        """Format cost as currency string"""
        return f"${cost:.4f}"
    
    def format_tokens(self, tokens: int) -> str:
        """Format tokens with K/M suffix"""
        if tokens >= 1_000_000:
            return f"{tokens / 1_000_000:.2f}M"
        elif tokens >= 1_000:
            return f"{tokens / 1_000:.1f}K"
        else:
            return str(tokens)
    
    def get_summary(self) -> str:
        """
        Get formatted summary string
        
        Returns:
            Human-readable summary
        """
        stats = self.get_stats()
        
        summary = f"""
Session Usage Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tokens:
  • Input:  {self.format_tokens(stats['input_tokens'])} (${stats['input_cost']:.4f})
  • Output: {self.format_tokens(stats['output_tokens'])} (${stats['output_cost']:.4f})
  • Total:  {self.format_tokens(stats['total_tokens'])}

Images Generated: {stats['images_generated']} (${stats['image_cost']:.2f})

Total Cost: ${stats['total_cost']:.4f}
Duration: {stats['session_duration']:.1f} min
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """
        return summary.strip()
