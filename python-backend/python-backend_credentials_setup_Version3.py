#!/usr/bin/env python3
"""
Small helper to validate IBM Quantum token (does not store it).
Usage:
  Set IBM_QUANTUM_TOKEN in env and run: python credentials_setup.py
"""
import os
import sys

token = os.environ.get("IBM_QUANTUM_TOKEN")
if not token:
    print("IBM_QUANTUM_TOKEN not set. Set it in your environment and re-run.")
    print("Example (bash): export IBM_QUANTUM_TOKEN='your-token'")
    sys.exit(1)

try:
    from qiskit_ibm_runtime import QiskitRuntimeService
except Exception as e:
    print("qiskit-ibm-runtime not installed or failed to import:", e)
    print("Install via pip or conda (recommended: conda-forge).")
    sys.exit(1)

try:
    service = QiskitRuntimeService(token=token)
    backends = service.backends()
    print("Token valid. Found the following accessible backends (first 20):")
    for b in backends[:20]:
        print(" -", b.name)
    print("\nDone. Keep IBM_QUANTUM_TOKEN secret. DO NOT commit it to git.")
except Exception as e:
    print("Failed to validate token:", e)
    sys.exit(2)