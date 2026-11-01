import urllib.request
import json

req = urllib.request.Request('http://127.0.0.1:8501', headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=5) as r:
        html = r.read().decode('utf-8')
        print(f"Status: {r.status}")
        print(f"HTML Length: {len(html)}")
        print("Title tag:", [line for line in html.splitlines() if '<title>' in line])
        # Streamlit SSR or scripts
        print("Contains streamlit scripts:", 'streamlit' in html.lower())
except Exception as e:
    print("Error:", e)
