from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI, RateLimitError

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

BUSINESS_INFO = """
You are a helpful assistant for SZ Plumbers in Harare.

Services:
- Call out: $20
- Toilet installation: $10
- Borehole fixes: $25

Open: Monday–Saturday, 8am–6pm
Location: Harare CBD
"""

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": BUSINESS_INFO},
                {"role": "user", "content": user_message}
            ]
        )

        reply = response.choices[0].message.content
        return jsonify({"reply": reply})
    except RateLimitError:
        return jsonify({"reply": "Sorry, I'm currently unavailable due to API limits. Please try again later."})

if __name__ == "__main__":
    app.run(debug=True)