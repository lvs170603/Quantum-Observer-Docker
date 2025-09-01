from flask import Flask, request, jsonify
from flask_cors import CORS
from qiskit import QuantumCircuit, Aer, execute

app = Flask(_name_)
CORS(app)  # allow frontend at different origin during dev

@app.route('/quantum', methods=['POST'])
def quantum():
    data = request.get_json() or {}
    n_qubits = int(data.get('n_qubits', 2))
    # Basic safety: require >=2 qubits for this example
    if n_qubits < 2:
        return jsonify({"error": "n_qubits must be >= 2"}), 400

    qc = QuantumCircuit(n_qubits, n_qubits)
    qc.h(0)
    for i in range(1, n_qubits):
        qc.cx(0, i)
    qc.measure(range(n_qubits), range(n_qubits))

    simulator = Aer.get_backend('qasm_simulator')
    job = execute(qc, simulator, shots=1024)
    result = job.result()
    counts = result.get_counts(qc)
    return jsonify(counts)

if _name_ == '_main_':
    app.run(host='0.0.0.0', port=5000, debug=True)