"use client"
import { useState } from "react"

export default function QuantumUI() {
  const [backend, setBackend] = useState("ibmq_qasm_simulator")
  const [result, setResult] = useState<any>(null)

  // Circuit run cheyyadaniki request
  const runCircuit = async () => {
    const res = await fetch("http://127.0.0.1:5000/quantum", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ n_qubits: 3, backend })   // ✅ send backend
    })
    const data = await res.json()
    setResult(data)
  }

  return (
    <div className="p-6 space-y-4">
      <h1 className="text-2xl font-bold">Quantum Device Runner</h1>

      {/* Device Dropdown */}
      <select
        value={backend}
        onChange={(e) => setBackend(e.target.value)}
        className="border p-2 rounded"
      >
        <option value="ibmq_qasm_simulator">IBM QASM Simulator</option>
        <option value="ibm_nairobi">IBM Nairobi (5 Qubits)</option>
        <option value="ibm_oslo">IBM Oslo (7 Qubits)</option>
      </select>

      {/* Run Button */}
      <button
        onClick={runCircuit}
        className="px-4 py-2 bg-blue-600 text-white rounded"
      >
        Run Circuit
      </button>

      {/* Show Result */}
      {result && (
        <pre className="bg-gray-900 text-green-400 p-3 rounded">
          {JSON.stringify(result, null, 2)}
        </pre>
      )}
    </div>
  )
}
