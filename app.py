from flask import Flask, request
import os
import json
import requests

app = Flask(__name__)

GROK_API_KEY = os.getenv("GROK_API_KEY")

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    
    print("=== NEW WEBHOOK RECEIVED ===")
    print(json.dumps(data, indent=2))
    
    if not GROK_API_KEY:
        print("ERROR: GROK_API_KEY not set")
        return "OK", 200
    
    try:
        summary_prompt = f"""You are an expert TMS Rate Analyst for Catalyst Logistics.

Analyze this Turvo shipment update and give a SHORT, professional alert.

Focus ONLY on:
- Load number / customId
- Lane (origin to destination)
- Customer rate (totalReceivableAmount)
- Margin if available

Compare the current rate to what is normal for this lane.
Be direct and flag anything unusual.

Respond in this exact style:
- First line: "Load 732867 - Batesville AR to Litchfield MN"
- Second line: One clear sentence about the rate (example: "Rate of $2500 is 15% above our 8-week average on this lane." or "Rate of $900 is significantly below normal.")
- If it's unusual, end with "Please review this one."

Keep total response to 3 lines max.

JSON: {json.dumps(data)}"""

        response = requests.post(
            "https://api.x.ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROK_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "grok-3",
                "messages": [{"role": "user", "content": summary_prompt}],
                "temperature": 0.3,
                "max_tokens": 300
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            summary = result['choices'][0]['message']['content']
            print("\n=== GROK RATE ALERT ===")
            print(summary)
        else:
            print("Error from Grok:", response.text)
            
    except Exception as e:
        print("Error:", str(e))
    
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
