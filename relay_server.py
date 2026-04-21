from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

orders = []

@app.route("/webhook/<store_slug>", methods=["POST"])
def webhook(store_slug):
    data = request.json

    order = {
        "store": store_slug,
        "id": data.get("id"),
        "total": data.get("total"),
        "customer": (data.get("billing", {}).get("first_name", "") + " " +
                     data.get("billing", {}).get("last_name", "")).strip(),
        "time": datetime.now().isoformat()
    }

    orders.append(order)
    return jsonify({"ok": True})

@app.route("/get_orders")
def get_orders():
    global orders
    data = orders.copy()
    orders = []
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)