#Connects the frontend to the AEIOS backend and orchestrates access to the system's functionality.
from agents.orchestrator import OrchestratorAgent
from backend.progress_tracker import ProgressTracker
from backend.execution_manager import ExecutionManager
from backend.analytics_manager import AnalyticsManager


class AEIOSService:

    def __init__(self):
        self.progress = ProgressTracker()

        self.orchestrator = OrchestratorAgent(
            progress_tracker=self.progress
        )

        self.execution_manager = ExecutionManager()
        self.analytics = AnalyticsManager()

    # ----------------------------------------------------
    # Background Execution
    # ----------------------------------------------------

    def start_processing(self, query):
        self.progress.clear()

        job_id = self.execution_manager.start(
            self.orchestrator.process_request,
            query
        )

        return job_id

    # ----------------------------------------------------
    # Job Status
    # ----------------------------------------------------

    def get_status(self, job_id):
        return self.execution_manager.get_status(job_id)

    # ----------------------------------------------------
    # Final Result
    # ----------------------------------------------------

    def get_result(self, job_id):
        result = self.execution_manager.get_result(job_id)

        if result is None:
            return None

        # Return the full result dictionary so the
        # Chat and Explainability pages receive all fields.
        if isinstance(result, dict):
            self.record_analytics(
                query=result.get("query", ""),
                execution_time=result.get("execution_time", 0),
                confidence_score=result.get("confidence_score", 0),
                memory_used=result.get("memory_used", False),
                selected_agents=result.get("selected_agents", [])
            )

            return result

        # Handle unexpected string results safely.
        return {
            "query": "",
            "response": str(result),
            "execution_time": None,
            "confidence_score": None,
            "memory_used": False,
            "selected_agents": []
        }

    # ----------------------------------------------------
    # Progress
    # ----------------------------------------------------

    def get_progress(self):
        return self.progress.get_steps()

    # ----------------------------------------------------
    # Progress Subscribers
    # ----------------------------------------------------

    def subscribe(self, callback):
        self.progress.subscribe(callback)

    def unsubscribe(self, callback):
        self.progress.unsubscribe(callback)

    # ----------------------------------------------------
    # Analytics
    # ----------------------------------------------------

    def record_analytics(
        self,
        query,
        execution_time,
        confidence_score,
        memory_used,
        selected_agents
    ):
        self.analytics.record_query(
            query=query,
            execution_time=execution_time,
            confidence_score=confidence_score,
            memory_used=memory_used,
            selected_agents=selected_agents
        )

    def get_analytics(self):
        return self.analytics.get_statistics()
