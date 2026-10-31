"""
KrishiArtha-MCP ONNX Translation Bridge Package
Provides browser/edge translation capabilities with deterministic offline fallback
for Marathi, Hindi, Telugu, and English.
"""

from frontend.onnx_bridge.translator import (
    OfflineTranslator,
    get_translator,
    translate_text,
)

__all__ = ["OfflineTranslator", "get_translator", "translate_text"]
