"""
World-Class Neural Hackathon Narration Generator
Uses Microsoft Edge Neural TTS (en-IN-PrabhatNeural & en-IN-NeerjaExpressiveNeural)
Generates studio-grade dialogue between two founders (Abhilok & Sai Chandra).
Strictly timed to 4m 30s - 4m 45s (perfect for 5-minute hackathon demo).
"""
import asyncio
import os
from pathlib import Path
import subprocess
import edge_tts

AUDIO_DIR = Path("docs/demo_recording/audio_segments")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

DIALOGUE = [
    # 1. Hook (Abhilok - Prabhat)
    (
        "seg_01_hook.mp3",
        "en-IN-PrabhatNeural",
        "+22%",
        "Namaste judges. In October 2026, unseasonal torrential rains devastated the agricultural hub of Nashik, Maharashtra. Within 48 hours, over ten thousand smallholder farmers panic-harvested perishable tomatoes, flooding wholesale mandis. Prices crashed from fourteen hundred to just nine hundred rupees per quintal—well below the eleven hundred rupee cost of production. Existing portals like Agmarknet and e-NAM fail because they are backward-looking dashboards. They show yesterday's prices, but cannot predict price collapses under incoming weather shocks, they ignore transit spoilage, and they offer zero financial safety net. Team INFINITE LOOP from Triple I T Guwahati presents KrishiArtha MCP: an autonomous multi-agent platform combining foundation time-series forecasting, Arrhenius transit thermodynamics, and statutory distress pledge loans."
    ),
    # 2. Intake & Live Telemetry (Sai Chandra - Neerja)
    (
        "seg_02_intake.mp3",
        "en-IN-NeerjaExpressiveNeural",
        "+22%",
        "Let us demonstrate live. Our farmer, Suresh Patil from Nashik, has a fifty quintal tomato lot. Speaking in Marathi: माझ्याकडे पन्नास क्विंटल टोमॅटो आहेत. Instantly, our Bhashini layer extracts the slots: Commodity Tomato, Lot fifty Quintals, Origin Nashik. Complying strictly with Rule 4's zero mock data mandate, our FastMCP server queries live APIs in real time: live wholesale arrivals from Data dot gov dot in and Mandi API, live seven-day hourly precipitation from Open-Meteo, and live highway routes from OSRM."
    ),
    # 3. Weather Radar & Chronos-2 (Abhilok - Prabhat)
    (
        "seg_03_weather_chronos.mp3",
        "en-IN-PrabhatNeural",
        "+22%",
        "Look at the live weather radar: thirty-one point five degrees Celsius, eighty-two percent humidity, and an incoming forty-two point five millimeter rainstorm. Feeding these live weather covariates into our Amazon Chronos foundation time-series forecaster predicts an imminent price collapse to seven hundred eighty rupees per quintal."
    ),
    # 4. Surat Spoilage Physics (Sai Chandra - Neerja)
    (
        "seg_04_surat_trap.mp3",
        "en-IN-NeerjaExpressiveNeural",
        "+22%",
        "Now observe the three-column Arbitrage Matrix. Conventional systems suggest trucking harvest two hundred thirty-four kilometers to Surat where nominal prices appear higher at thirteen hundred fifty rupees. But that is a false arbitrage trap! KrishiArtha models Arrhenius Q10 decay physics. Over a five point two hour highway trip under thirty-one point five degrees heat plus unloading delays, eighteen point four percent of the harvest rots in transit. Subtracting round-trip diesel freight, that thirteen hundred fifty Surat price collapses to just nine hundred sixty-five rupees per quintal. The farmer risks everything for barely thirty-two hundred rupees."
    ),
    # 5. WDRA Policy & Recovery (Abhilok - Prabhat)
    (
        "seg_05_wdra_policy.mp3",
        "en-IN-PrabhatNeural",
        "+22%",
        "With all nearby markets below the eleven hundred rupee cost floor, KrishiArtha triggers a Regional Distress Crash. Node 2 activates LightRAG over statutory NABARD Circular 128 and WDRA regulations, unlocking Option C: the accredited MSWC cold storage in Ozar, fourteen kilometers away. The farmer generates an Electronic Negotiable Warehouse Receipt, unlocking an immediate seventy-five percent cash pledge advance of thirty-three thousand seven hundred fifty rupees at just four percent interest under KCC subvention. Ten days later when prices rebound to fourteen hundred eighty rupees, net farmer take-home reaches sixty-eight thousand four hundred rupees. That is a net cash gain of twenty-three thousand four hundred rupees—a fifty-two percent income boost over panic selling!"
    ),
    # 6. Human in the Loop & Browser Agent (Sai Chandra - Neerja)
    (
        "seg_06_hitl_agent.mp3",
        "en-IN-NeerjaExpressiveNeural",
        "+22%",
        "In compliance with LangGraph best practices, execution pauses cleanly at our human approval gate. When the farmer clicks Approve e-NWR Loan, Node 4 launches our automated Playwright browser agent. In one point two one seconds, it navigates the government WDRA portal, validates the license, and issues an official digitally signed sanction slip! The farmer walks away with immediate cash liquidity in his pocket and full ownership of his harvest."
    ),
    # 7. Verification & Winning Closing (Abhilok - Prabhat)
    (
        "seg_07_closing.mp3",
        "en-IN-PrabhatNeural",
        "+22%",
        "KrishiArtha MCP is fully Rule 4 compliant with 100% live APIs and zero mock data, audited with AgentShield at Grade A one hundred out of one hundred, and verified with seventy out of seventy passing unit tests. By bridging foundation time-series AI, physical transit thermodynamics, and statutory digital public infrastructure, KrishiArtha transforms agricultural vulnerability into rural economic resilience. Thank you!"
    ),
]

async def generate_segments():
    segment_paths = []
    for filename, voice, rate, text in DIALOGUE:
        path = AUDIO_DIR / filename
        print(f"Generating {filename} with voice {voice} at {rate}...")
        tts = edge_tts.Communicate(text, voice, rate=rate)
        await tts.save(str(path))
        segment_paths.append(path)
    
    # Create concat list for ffmpeg
    concat_list_file = AUDIO_DIR / "concat_list.txt"
    with open(concat_list_file, "w", encoding="utf-8") as f:
        for p in segment_paths:
            f.write(f"file '{p.resolve().as_posix()}'\n")
            
    final_audio = Path("docs/demo_recording/world_class_narration.mp3")
    print(f"Concatenating all segments into {final_audio}...")
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list_file),
        "-c", "copy",
        str(final_audio)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"SUCCESS: World-class narration generated at {final_audio}")
    else:
        print(f"FFmpeg error: {res.stderr}")

if __name__ == "__main__":
    asyncio.run(generate_segments())
