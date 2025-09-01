from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "note": "Running in MOCK mode (Qiskit not installed). Replace with real Qiskit backend when ready."
    })

@app.route("/quantum", methods=["POST"])
def quantum():
    payload = request.get_json() or {}
    try:
        n_qubits = int(payload.get("n_qubits", 2))
    except Exception:
        return jsonify({"error": "n_qubits must be an integer"}), 400
    if n_qubits < 1 or n_qubits > 20:
        return jsonify({"error": "n_qubits must be between 1 and 20"}), 400

    shots = int(payload.get("shots", 1024))

    # Simple mock: GHZ-like distribution -> mostly "0...0" and "1...1"
    zero = "0" * n_qubits
    one = "1" * n_qubits

    # create deterministic-ish distribution with randomness
    prob_one = 0.5
    counts_zero = int(shots * (1 - prob_one))
    counts_one = shots - counts_zero

    # add small noise
    counts = {zero: counts_zero, one: counts_one}
    # add tiny noise to random other bitstrings
    if n_qubits <= 8:  # don't explode keys for many qubits
        for _ in range(min(3, shots // 100)):
            b = format(random.randrange(0, 2**n_qubits), f"0{n_qubits}b")
            if b not in counts:
                counts[b] = max(1, shots // 100)

    return jsonify({"source": "mock", "backend": "mock_simulator", "counts": counts})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)