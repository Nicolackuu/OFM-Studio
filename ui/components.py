"""
Reusable UI Components for OFM IA Studio
Professional SaaS Dashboard Components
"""
import streamlit as st
from pathlib import Path
from typing import Optional, List
import psutil

try:
    import pynvml
    NVML_AVAILABLE = True
except ImportError:
    NVML_AVAILABLE = False

def stat_card(label: str, value: str, icon: str = "📊", progress: Optional[float] = None, target: Optional[int] = None):
    """
    Professional stat card with optional progress bar
    
    Args:
        label: Card title
        value: Main value to display
        icon: Emoji icon
        progress: Current progress value (0-100)
        target: Target value for progress calculation
    """
    st.markdown(f"""
    <div class="stat-card fade-in">
        <div class="stat-icon">{icon}</div>
        <div class="stat-label">{label}</div>
        <div class="stat-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)
    
    if progress is not None and target is not None:
        st.progress(progress / target if target > 0 else 0)
        st.caption(f"{int(progress)}/{target}")

def led_indicator(status: bool, label: str, color_on: str = "green", color_off: str = "red"):
    """
    LED indicator with label
    
    Args:
        status: True for on, False for off
        label: Text label
        color_on: Color when status is True
        color_off: Color when status is False
    """
    color = color_on if status else color_off
    status_text = "✅ Connecté" if status else "❌ Déconnecté"
    
    st.markdown(f"""
    <div style="display: flex; align-items: center; margin: 10px 0;">
        <span class="led-indicator led-{color}"></span>
        <span style="color: #c5cae9; font-weight: 600;">{label}:</span>
        <span style="margin-left: 10px; color: {'#00ff88' if status else '#ff4757'};">{status_text}</span>
    </div>
    """, unsafe_allow_html=True)

def system_monitor():
    """
    Real-time system monitoring (RAM, VRAM)
    """
    st.markdown("### 🖥️ System Monitor")
    
    # RAM Usage
    ram = psutil.virtual_memory()
    ram_percent = ram.percent
    ram_used = ram.used / (1024**3)  # GB
    ram_total = ram.total / (1024**3)  # GB
    
    # Color based on usage
    ram_color = "#00ff88" if ram_percent < 70 else "#ffa502" if ram_percent < 85 else "#ff4757"
    
    st.markdown(f"""
    <div class="monitor-card">
        <div class="monitor-label">💾 RAM Usage</div>
        <div class="monitor-value" style="color: {ram_color};">{ram_used:.1f} GB / {ram_total:.1f} GB ({ram_percent:.0f}%)</div>
    </div>
    """, unsafe_allow_html=True)
    st.progress(ram_percent / 100)
    
    # VRAM Usage (RTX 3070) - Linear style with 2px gauge
    if NVML_AVAILABLE:
        try:
            pynvml.nvmlInit()
            handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            info = pynvml.nvmlDeviceGetMemoryInfo(handle)
            gpu_name = pynvml.nvmlDeviceGetName(handle)
            vram_used = info.used / (1024**3)  # GB
            vram_total = info.total / (1024**3)  # GB
            vram_percent = (info.used / info.total) * 100
            
            # Color based on usage
            vram_color = "#10b981" if vram_percent < 70 else "#fbbf24" if vram_percent < 85 else "#ef4444"
            
            st.markdown(f"""
            <div class="monitor-card">
                <div class="monitor-label">🎮 VRAM ({gpu_name})</div>
                <div class="monitor-value" style="color: {vram_color};">{vram_used:.1f} GB / {vram_total:.1f} GB ({vram_percent:.0f}%)</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Linear-style 2px gauge
            st.markdown(f"""
            <div style="
                width: 100%;
                height: 2px;
                background: #1f2937;
                border-radius: 1px;
                overflow: hidden;
                margin-top: 8px;
            ">
                <div style="
                    width: {vram_percent}%;
                    height: 100%;
                    background: {vram_color};
                    transition: width 0.3s ease;
                "></div>
            </div>
            """, unsafe_allow_html=True)
            
            pynvml.nvmlShutdown()
        except Exception as e:
            st.markdown(f"""
            <div class="monitor-card">
                <div class="monitor-label">🎮 GPU Status</div>
                <div class="monitor-value" style="color: #6b7280;">Not Available</div>
            </div>
            """, unsafe_allow_html=True)
            st.caption(f"⚠️ {str(e)[:50]}")
    else:
        st.markdown(f"""
        <div class="monitor-card">
            <div class="monitor-label">🎮 GPU Status</div>
            <div class="monitor-value" style="color: #6b7280;">nvidia-ml-py not installed</div>
        </div>
        """, unsafe_allow_html=True)
        st.caption("💡 Install: pip install nvidia-ml-py")

def token_wallet(tracker):
    """
    Display token usage and cost tracking
    
    Args:
        tracker: UsageTracker instance from session_state
    """
    st.markdown("### 💰 Token Wallet")
    
    stats = tracker.get_stats()
    
    # Total cost with color coding
    total_cost = stats['total_cost']
    cost_color = "#00ff88" if total_cost < 0.10 else "#ffa502" if total_cost < 0.50 else "#ff4757"
    
    st.markdown(f"""
    <div class="monitor-card" style="border-left: 3px solid {cost_color};">
        <div class="monitor-label">Session Cost</div>
        <div class="monitor-value" style="color: {cost_color}; font-size: 1.5rem;">${total_cost:.4f}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Token breakdown
    total_tokens = stats['total_tokens']
    tokens_display = tracker.format_tokens(total_tokens)
    
    st.markdown(f"""
    <div class="monitor-card">
        <div class="monitor-label">Total Tokens</div>
        <div class="monitor-value" style="color: #4facfe;">{tokens_display}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Detailed breakdown in expander
    with st.expander("📊 Détails"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Input", tracker.format_tokens(stats['input_tokens']), 
                     delta=f"${stats['input_cost']:.4f}")
            st.metric("Images", stats['images_generated'], 
                     delta=f"${stats['image_cost']:.2f}")
        
        with col2:
            st.metric("Output", tracker.format_tokens(stats['output_tokens']), 
                     delta=f"${stats['output_cost']:.4f}")
            st.metric("Duration", f"{stats['session_duration']:.1f} min")
        
        if st.button("🔄 Reset Tracker", use_container_width=True):
            tracker.reset()
            st.success("✓ Tracker reset!")
            st.rerun()

def console_output(logs: List[str], max_lines: int = 20):
    """
    Console-style output box
    
    Args:
        logs: List of log messages
        max_lines: Maximum number of lines to display
    """
    console_html = "<div class='console-output'>"
    for log in logs[-max_lines:]:
        console_html += f"<div>{log}</div>"
    console_html += "</div>"
    
    st.markdown(console_html, unsafe_allow_html=True)

def image_preview(image_path: Path, caption: str = "", zoom: bool = True):
    """
    Image preview with optional zoom effect
    
    Args:
        image_path: Path to image
        caption: Image caption
        zoom: Enable hover zoom effect
    """
    if image_path.exists():
        css_class = "image-preview" if zoom else ""
        st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
        st.image(str(image_path), caption=caption, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error(f"Image not found: {image_path}")

def info_box(message: str, box_type: str = "info"):
    """
    Styled info/success/error/warning box
    
    Args:
        message: Message to display
        box_type: One of 'info', 'success', 'error', 'warning'
    """
    icons = {
        "info": "ℹ️",
        "success": "✅",
        "error": "❌",
        "warning": "⚠️"
    }
    
    icon = icons.get(box_type, "ℹ️")
    
    st.markdown(f"""
    <div class="{box_type}-box">
        <strong>{icon} {message}</strong>
    </div>
    """, unsafe_allow_html=True)

def tinder_card(image_path: Path, current_idx: int, total: int):
    """
    Tinder-style card for image curation with absolute path handling
    
    Args:
        image_path: Path to image (can be Path object or string)
        current_idx: Current image index
        total: Total number of images
    """
    # Ensure we have a Path object with absolute path
    if isinstance(image_path, str):
        image_path = Path(image_path)
    
    # Convert to absolute path if relative
    if not image_path.is_absolute():
        image_path = image_path.resolve()
    
    st.markdown(f"""
    <div class="tinder-card fade-in">
        <div class="tinder-counter">{current_idx + 1} / {total}</div>
    </div>
    """, unsafe_allow_html=True)
    
    if image_path.exists():
        try:
            st.image(str(image_path), use_container_width=True)
        except Exception as e:
            st.error(f"Error loading image: {e}")
            st.code(f"Path: {image_path}")
    else:
        st.error(f"❌ Image not found")
        st.code(f"Path: {image_path}")
        st.info("💡 Vérifiez que le chemin est correct et que le fichier existe")

def copy_button(text: str, label: str = "📋 Copy"):
    """
    Copy to clipboard button
    
    Args:
        text: Text to copy
        label: Button label
    """
    if st.button(label, key=f"copy_{hash(text)}"):
        st.code(text, language="text")
        st.success("✓ Copied to clipboard (select and copy above)")

def progress_tracker(current: int, total: int, label: str = "Progress"):
    """
    Progress tracker with percentage
    
    Args:
        current: Current progress
        total: Total items
        label: Progress label
    """
    percent = (current / total * 100) if total > 0 else 0
    
    st.markdown(f"""
    <div style="margin: 20px 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
            <span style="color: #8b92a7; font-weight: 600;">{label}</span>
            <span style="color: #4facfe; font-weight: 700;">{current}/{total} ({percent:.1f}%)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.progress(percent / 100)

def gallery_grid(image_paths: List[Path], columns: int = 4, max_display: int = 20):
    """
    Lazy-loading gallery grid
    
    Args:
        image_paths: List of image paths
        columns: Number of columns
        max_display: Maximum images to display
    """
    if not image_paths:
        st.info("No images to display")
        return
    
    display_paths = image_paths[:max_display]
    
    cols = st.columns(columns)
    for idx, img_path in enumerate(display_paths):
        with cols[idx % columns]:
            if img_path.exists():
                st.markdown('<div class="gallery-item">', unsafe_allow_html=True)
                st.image(str(img_path), use_container_width=True, caption=img_path.name[:15])
                st.markdown('</div>', unsafe_allow_html=True)
    
    if len(image_paths) > max_display:
        st.caption(f"Showing {max_display} of {len(image_paths)} images")

def phase_button(phase: int, enabled: bool = True, completed: bool = False):
    """
    Styled phase button with status
    
    Args:
        phase: Phase number (1, 2, 3)
        enabled: Whether button is enabled
        completed: Whether phase is completed
    """
    status_icon = "✅" if completed else "🚀"
    status_text = "Completed" if completed else "Launch"
    
    if not enabled:
        st.button(f"⏸️ Phase {phase} (Locked)", disabled=True, use_container_width=True)
    else:
        return st.button(f"{status_icon} PHASE {phase}: {status_text}", use_container_width=True, type="primary")
    
    return False
