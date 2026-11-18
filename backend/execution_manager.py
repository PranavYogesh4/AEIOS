#Manages background execution jobs, including starting work and handling job failures.
import threading
import uuid
import logging

logger = logging.getLogger(__name__)


class ExecutionManager:

    def __init__(self):
        self.jobs = {}
        self.lock = threading.Lock()

    # -----------------------------------------
    # Start a new execution in background
    # -----------------------------------------

    def start(self, target, *args):
        job_id = str(uuid.uuid4())

        with self.lock:
            self.jobs[job_id] = {
                "status": "running",
                "result": None,
                "error": None,
                "thread": None,
            }

        def wrapper():
            try:
                result = target(*args)

                with self.lock:
                    self.jobs[job_id]["result"] = result
                    self.jobs[job_id]["status"] = "completed"

                logger.info("Job %s completed successfully.", job_id)

            except Exception as exc:
                logger.exception("Job %s failed.", job_id)

                with self.lock:
                    self.jobs[job_id]["error"] = str(exc)
                    self.jobs[job_id]["status"] = "failed"

        thread = threading.Thread(
            target=wrapper,
            daemon=True,
            name=f"AEIOS-Job-{job_id[:8]}",
        )

        with self.lock:
            self.jobs[job_id]["thread"] = thread

        thread.start()
        return job_id

    # -----------------------------------------
    # Get Status
    # -----------------------------------------

    def get_status(self, job_id):
        with self.lock:
            job = self.jobs.get(job_id)

            if job is None:
                return "not_found"

            return job["status"]

    # -----------------------------------------
    # Get Result
    # -----------------------------------------

    def get_result(self, job_id):
        with self.lock:
            job = self.jobs.get(job_id)

            if job is None:
                return None

            return job["result"]

    # -----------------------------------------
    # Get Error
    # -----------------------------------------

    def get_error(self, job_id):
        with self.lock:
            job = self.jobs.get(job_id)

            if job is None:
                return "Job not found."

            return job["error"]
