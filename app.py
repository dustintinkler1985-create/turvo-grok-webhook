from flask import Flask, request
import os
import json
import requests

app = Flask(__name__)

GROK_API_KEY = os.getenv("GROK_API_KEY")

@app.route('/', methods= )
def webhook():
    data = request.get_json()
    
    print("=== NEW WEBHOOK RECEIVED ===")
    print(json.dumps(data, indent=2))
    
    try:
        summary_prompt = f"""You are a helpful TMS analyst. Here's a Turvo shipment update webhook. Give me a clean, short summary in plain English. Focus on load number, route, status, and what changed.

JSON: {json.dumps(data)}"""
        
        response = requests.post(
            "https://api.x.ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROK_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "grok-beta",
                "messages": [{"role": "user", "content": summary_prompt}],
                "temperature": 0.7,
                "max_tokens": 400
            },
            timeout=30
        )
        
        if response.status_code == 200:
            summary = response.json() [0]  print("\n=== GROK SUMMARY ===")
            print(summary)
        else:
            print("Error from Grok:", response.text)
            
    except Exception as e:
        print("Error:", str(e))
    
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
