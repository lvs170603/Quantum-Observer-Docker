import logging
import hashlib
from datetime import timezone
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from qiskit_ibm_runtime import QiskitRuntimeService

# -------------------------
# Logging
# -------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("quantum-tracker")

# -------------------------
# IBM Quantum Credentials (⚠ demo)
# -------------------------
TOKEN = "7uB1rS41OFhMS_7U9HUwE1bD7ApCAvuNoXC1CpufFL1R"
INSTANCE = (
    "crn:v1:bluemix:public:quantum-computing:us-east:a/"
    "f337e67a23db46a7b912221b7e84e282:"
    "6bac78c7-3180-4d7f-9e06-1cc288de4f52::"
)
CHANNEL = "ibm_cloud"

try:
    service = QiskitRuntimeService(
        channel=CHANNEL,
        token=TOKEN,
        instance=INSTANCE,
    )
    logger.info("✅ Connected to IBM Quantum Runtime service")
except Exception as e:
    logger.exception("❌ Failed to connect to IBM Quantum: %s", e)
    raise

# -------------------------
# FastAPI app
# -------------------------
app = FastAPI(title="IBM Quantum Job Tracker")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Helpers
# -------------------------
STATUS_MAP = {
    "QUEUED": "QUEUED",
    "RUNNING": "RUNNING",
    "COMPLETED": "COMPLETED",
    "ERROR": "ERROR",
    "CANCELLED": "CANCELLED",
    "CANCELED": "CANCELED",
    "DONE": "COMPLETED",
    "UNKNOWN": "UNKNOWN",
}


def normalize_status(status_obj: Any) -> str:
    try:
        if not status_obj:
            return "UNKNOWN"

        if hasattr(status_obj, "name"):
            s = status_obj.name
        elif hasattr(status_obj, "value"):
            s = status_obj.value
        else:
            s = str(status_obj)

        s = s.split(".")[-1].upper()
        return STATUS_MAP.get(s, s.title())
    except Exception:
        return "UNKNOWN"


def mask_user_id(user_id: str) -> str:
    if not user_id:
        return "Quantum User"
    hashed = hashlib.sha256(user_id.encode()).hexdigest()
    return f"user_{hashed[:6]}"


def safe_call(obj, attr):
    try:
        val = getattr(obj, attr, None)
        return val() if callable(val) else val
    except Exception:
        return None


def job_to_dict(job) -> dict:
    # Backend
    try:
        backend = job.backend()
        backend_name = safe_call(backend, "name") if backend else None
    except Exception:
        backend_name = None

    # Status
    status = normalize_status(safe_call(job, "status"))

    # Dates
    created = safe_call(job, "creation_date")
    created_iso = created.astimezone(timezone.utc).isoformat() if created else None

    completed = safe_call(job, "end_date")
    completed_iso = completed.astimezone(timezone.utc).isoformat() if completed else None

    # Other fields
    usage_seconds = safe_call(job, "usage")
    tags = safe_call(job, "tags") or []
    error_message = safe_call(job, "error_message")
    metrics = safe_call(job, "metrics")

    # User
    raw_user = getattr(job, "instance", None) or "default"
    masked_user = mask_user_id(str(raw_user))

    return {
        "id": safe_call(job, "job_id"),
        "status": status,
        "backend": backend_name,
        "created": created_iso,
        "completed": completed_iso,
        "usage_seconds": usage_seconds,
        "metrics": metrics,
        "error_message": error_message,
        "user": masked_user,
        "tags": tags,
    }


# -------------------------
# API Routes
# -------------------------
@app.get("/api/jobs")
def list_jobs(limit: int = 20, status: str | None = None):
    try:
        jobs = service.jobs(limit=limit, status=status) if status else service.jobs(limit=limit)
        return [job_to_dict(j) for j in jobs]
    except Exception as e:
        logger.exception("Error listing jobs: %s", e)
        raise HTTPException(status_code=500, detail={"error": str(e)})


@app.get("/api/jobs/{job_id}")
def get_job(job_id: str):
    try:
        job = service.job(job_id)
        return job_to_dict(job)
    except Exception as e:
        logger.exception("Error fetching job %s: %s", job_id, e)
        raise HTTPException(status_code=404, detail={"error": str(e)})


@app.get("/api/backends")
def list_backends():
    try:
        backends = service.backends()
        out = []
        for b in backends:
            try:
                status_obj = b.status()
                out.append(
                    {
                        "name": b.name(),
                        "num_qubits": getattr(b, "num_qubits", None),
                        "operational": getattr(status_obj, "operational", None),
                        "pending_jobs": getattr(status_obj, "pending_jobs", None),
                    }
                )
            except Exception:
                continue
        return out
    except Exception as e:
        logger.exception("Error listing backends: %s", e)
        raise HTTPException(status_code=500, detail={"error": str(e)})
