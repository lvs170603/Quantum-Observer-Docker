from flask import Flask, request, jsonify
from flask_cors import CORS
from qiskit import QuantumCircuit
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler

app = Flask(__name__)
CORS(app)

# ✅ Connect to IBM Quantum (replace with your token)
service = QiskitRuntimeService(
    channel="ibm_quantum_platform",
    token="AP_zNOxzYRZA3bCxA9jxR1CQi1h9qTEr6vCcHf1DaWFP"
)

@app.route("/quantum", methods=["POST"])
def quantum():
    data = request.get_json() or {}
    n_qubits = int(data.get("n_qubits", 2))
    backend_name = data.get("backend", "ibmq_qasm_simulator")  # ✅ frontend value

    if n_qubits < 2:
        return jsonify({"error": "n_qubits must be >= 2"}), 400

    qc = QuantumCircuit(n_qubits)
    qc.h(0)
    for i in range(1, n_qubits):
        qc.cx(0, i)

    # IBM service lo backend select
    sampler = Sampler(service=service, backend=backend_name)
    job = sampler.run([qc])
    result = job.result()

    return jsonify({
        "backend": backend_name,
        "result": {str(k): float(v) for k, v in result.quasi_dists[0].items()}
    })
