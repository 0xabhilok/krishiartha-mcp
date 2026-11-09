import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from streamlit.testing.v1 import AppTest

# Test with OFFLINE_STAGE_SAFE_MODE=false
os.environ["OFFLINE_STAGE_SAFE_MODE"] = "false"
app_path = str(REPO_ROOT / "frontend" / "app.py")

print("Initializing AppTest with OFFLINE_STAGE_SAFE_MODE=false...")
at = AppTest.from_file(app_path, default_timeout=15.0)
at.run(timeout=15.0)

print("AppTest exception check:", at.exception)
assert not at.exception, f"App execution failed with exception: {at.exception}"

# Check session state
print("Session state offline_safe_mode:", at.session_state.offline_safe_mode)
assert at.session_state.offline_safe_mode is False

# Check markdown for Live Badge
markdown_texts = [m.value for m in at.markdown]
live_badge_found = any(
    "LIVE APMC & FASTMCP ACTIVE" in t and ("Zero-Mock Production APIs" in t or "Rule 4" in t)
    for t in markdown_texts
)
print(f"Live API Badge ('🟢 LIVE APMC & FASTMCP ACTIVE') found: {live_badge_found}")
assert live_badge_found, "Live APMC badge not found in markdown output!"

# Now test toggling to OFFLINE mode
print("Toggling sidebar toggle to True (Offline mode)...")
at.sidebar.toggle[0].set_value(True).run()
assert not at.exception
markdown_texts_offline = [m.value for m in at.markdown]
offline_badge_found = any("OFFLINE STAGE FALLBACK" in t for t in markdown_texts_offline)
print(f"Offline Badge ('💾 OFFLINE STAGE FALLBACK') found: {offline_badge_found}")
assert offline_badge_found, "Offline badge not found when toggled to True!"

print("\nALL UI BADGE CHECKS PASSED SUCCESSFULLY!")
