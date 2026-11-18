#Coordinates the agents and manages the overall workflow.
import time

from agents.research_agent import ResearchAgent
from agents.threat_agent import ThreatAgent
from agents.report_agent import ReportAgent
from agents.consensus_agent import ConsensusAgent
from agents.planning_agent import PlanningAgent
from agents.reconstruction_agent import ReconstructionAgent
from agents.retry_engine import RetryEngine
from agents.self_evaluation_agent import SelfEvaluationAgent
from agents.reflection_agent import ReflectionAgent
from agents.confidence_agent import ConfidenceAgent
from agents.explainability_agent import ExplainabilityAgent

from collaboration.task_router import TaskRouter
from engine.adaptive_execution import AdaptiveExecutionEngine
from execution.parallel_executor import ParallelExecutor
from memory.memory_manager import MemoryManager

from utils.execution_timeline import ExecutionTimeline
from utils.performance_monitor import PerformanceMonitor
from utils.logger import logger


class OrchestratorAgent:

    def __init__(self, progress_tracker=None):
        self.progress_tracker = progress_tracker

        self.research_agent = ResearchAgent()
        self.threat_agent = ThreatAgent()
        self.report_agent = ReportAgent()
        self.consensus_agent = ConsensusAgent()

        self.planning_agent = PlanningAgent()
        self.timeline = ExecutionTimeline()
        self.reconstruction_agent = ReconstructionAgent()

        self.self_evaluation_agent = SelfEvaluationAgent()
        self.reflection_agent = ReflectionAgent()
        self.confidence_agent = ConfidenceAgent()
        self.explainability_agent = ExplainabilityAgent()

        self.memory_manager = MemoryManager()

        self.task_router = TaskRouter()
        self.execution_engine = AdaptiveExecutionEngine()
        self.retry_engine = RetryEngine()
        self.parallel_executor = ParallelExecutor()
        self.performance_monitor = PerformanceMonitor()

    # --------------------------------------------------
    # Progress helper
    # --------------------------------------------------

    def _mark_step(self, name):
        if self.progress_tracker:
            self.progress_tracker.add_step(name)

    # --------------------------------------------------
    # Safely format metadata for the decision trace
    # --------------------------------------------------

    @staticmethod
    def _to_text(value):
        if value is None:
            return ""
        if isinstance(value, str):
            return value
        return str(value)

    @staticmethod
    def _get_recommendation(evaluation):
        text = str(evaluation or "").upper()

        for line in text.splitlines():
            line = line.strip()

            if line.startswith("RECOMMENDATION:"):
                value = line.split(":", 1)[1].strip()

                if value in ("KEEP", "IMPROVE"):
                    return value

        for line in text.splitlines():
            if line.strip() in ("KEEP", "IMPROVE"):
                return line.strip()

        return "KEEP"

    @staticmethod
    def _get_confidence_score(confidence):
        text = str(confidence or "")

        for line in text.splitlines():
            if "confidence score" in line.lower():
                try:
                    value = line.split(":", 1)[1].strip()
                    return int(float(value))
                except (IndexError, ValueError):
                    pass

        return 0

    # --------------------------------------------------
    # Main orchestration
    # --------------------------------------------------

    def process_request(self, user_input):
        start_time = time.perf_counter()

        self.timeline = ExecutionTimeline()

        execution_stages = []
        reflection_attempted = False
        revision_performed = False

        research_output = ""
        threat_output = ""
        report_output = ""
        performance_report = None

        def record_stage(stage):
            execution_stages.append(stage)
            self.timeline.add_event(stage)

        # ----------------------------------------------
        # Memory reconstruction
        # ----------------------------------------------

        logger.info("Memory Reconstruction Agent Activated")
        self._mark_step("Memory Reconstruction")
        record_stage("Memory Reconstruction Started")

        try:
            memory_context = self.memory_manager.retrieve_memory(
                user_input
            )

            reconstructed_context = (
                self.reconstruction_agent.reconstruct_memory(
                    user_input,
                    memory_context
                )
            )

            if reconstructed_context is None:
                reconstructed_context = ""

            reconstructed_context = str(reconstructed_context)

            memory_used = (
                bool(reconstructed_context.strip())
                and "no relevant memory"
                not in reconstructed_context.lower()
            )

            record_stage("Memory Reconstruction Completed")

        except Exception as exc:
            logger.exception("Memory reconstruction failed")
            memory_used = False
            reconstructed_context = ""
            record_stage("Memory Reconstruction Failed")
            logger.warning("Memory error: %s", exc)

        # ----------------------------------------------
        # Planning
        # ----------------------------------------------

        logger.info("Planning Agent Activated")
        self._mark_step("Planning Agent")
        record_stage("Planning Started")

        execution_plan = self.planning_agent.create_plan(user_input)

        record_stage("Planning Completed")

        # ----------------------------------------------
        # Task routing
        # ----------------------------------------------

        selected_agents = self.task_router.route(user_input)

        logger.info("Selected agents: %s", selected_agents)

        self._mark_step("Task Routing")
        record_stage("Task Routing Completed")

        # ----------------------------------------------
        # Adaptive execution
        # ----------------------------------------------

        logger.info("Adaptive Execution Engine Activated")
        self._mark_step("Adaptive Execution")
        record_stage("Adaptive Execution Started")

        selected_agents = self.execution_engine.optimize_execution(
            selected_agents,
            user_input
        )

        logger.info(
            "Agents selected for execution: %s",
            selected_agents
        )

        record_stage("Adaptive Execution Completed")

        # ----------------------------------------------
        # Parallel execution
        # ----------------------------------------------

        self._mark_step("Parallel Agent Execution")
        record_stage("Parallel Agent Execution Started")

        (
            research_output,
            threat_output,
            report_output,
            performance_report
        ) = self.parallel_executor.execute(
            selected_agents=selected_agents,
            research_agent=self.research_agent,
            threat_agent=self.threat_agent,
            report_agent=self.report_agent,
            user_input=user_input
        )

        # Record output availability rather than assuming
        # that every agent produced usable results.
        if research_output:
            record_stage("Research Output Available")
        else:
            record_stage("Research Output Missing")

        if threat_output:
            record_stage("Threat Output Available")
        else:
            record_stage("Threat Output Missing")

        if report_output:
            record_stage("Report Output Available")
        else:
            record_stage("Report Output Missing")

        # ----------------------------------------------
        # Consensus
        # ----------------------------------------------

        logger.info("Consensus Agent Activated")
        self._mark_step("Consensus Agent")
        record_stage("Consensus Started")

        current_output = self.consensus_agent.generate_consensus(
            research_output,
            threat_output,
            report_output
        )

        current_output = self._to_text(current_output)

        if current_output.strip():
            record_stage("Consensus Output Available")
        else:
            record_stage("Consensus Output Empty")

        # ----------------------------------------------
        # Initial self-evaluation
        # ----------------------------------------------

        logger.info("Self Evaluation Agent Activated")
        self._mark_step("Self Evaluation Agent")
        record_stage("Self Evaluation Started")

        evaluation = self.self_evaluation_agent.evaluate(
            user_input,
            current_output
        )

        record_stage("Self Evaluation Completed")

        recommendation = self._get_recommendation(evaluation)

        # ----------------------------------------------
        # Optional single retry
        # ----------------------------------------------

        retry_triggered = False

        if self.retry_engine.should_retry(evaluation):
            retry_triggered = True

            logger.info("Autonomous retry triggered")
            self._mark_step("Retry Triggered")
            record_stage("Retry Triggered")

            # Preserve the original workflow: regenerate once.
            report_output = self.report_agent.generate_report(
                current_output
            )

            current_output = self._to_text(report_output)

            logger.info("Running final self-evaluation")
            self._mark_step("Self Evaluation Retry")
            record_stage("Retry Self Evaluation Started")

            evaluation = self.self_evaluation_agent.evaluate(
                user_input,
                current_output
            )

            recommendation = self._get_recommendation(evaluation)

            record_stage("Retry Self Evaluation Completed")

        # ----------------------------------------------
        # Reflection
        # ----------------------------------------------

        if recommendation == "IMPROVE":
            logger.info("Reflection Agent Activated")

            self._mark_step("Reflection Agent")
            reflection_attempted = True

            record_stage("Reflection Started")

            previous_output = current_output

            reflected_output = self.reflection_agent.reflect(
                user_input,
                current_output,
                evaluation
            )

            if reflected_output is not None:
                current_output = self._to_text(reflected_output)

                revision_performed = (
                    bool(current_output.strip())
                    and current_output != previous_output
                )

            record_stage("Reflection Completed")

            if revision_performed:
                record_stage("Response Changed After Reflection")
            else:
                record_stage("Response Change Not Confirmed")

        else:
            logger.info("Reflection skipped (KEEP recommendation)")
            record_stage("Reflection Skipped")

        # ----------------------------------------------
        # Confidence assessment
        # ----------------------------------------------

        logger.info("Confidence Agent Activated")
        self._mark_step("Confidence Agent")
        record_stage("Confidence Analysis Started")

        confidence = self.confidence_agent.evaluate(
            user_input,
            current_output
        )

        confidence_score = self._get_confidence_score(confidence)

        record_stage("Confidence Analysis Completed")

        # ----------------------------------------------
        # Explainability
        # ----------------------------------------------

        logger.info("Explainability Agent Activated")
        self._mark_step("Explainability Agent")
        record_stage("Explainability Started")

        decision_trace = self.explainability_agent.generate_trace(
            memory_used=memory_used,
            execution_plan=execution_plan,
            selected_agents=selected_agents,
            consensus_used=True,
            evaluation=evaluation,
            recommendation=recommendation,
            confidence=confidence
        )

        record_stage("Explainability Completed")

        # ----------------------------------------------
        # Store memory once
        # ----------------------------------------------

        logger.info("Storing interaction in memory")
        self._mark_step("Memory Storage")

        try:
            self.memory_manager.store_memory(
                user_input,
                current_output
            )

            record_stage("Memory Stored")

        except Exception as exc:
            logger.exception("Memory storage failed")
            record_stage("Memory Storage Failed")
            logger.warning("Memory storage error: %s", exc)

        # ----------------------------------------------
        # Final logs and result
        # ----------------------------------------------

        logger.info("Performance report: %s", performance_report)
        logger.info(self.timeline.report())

        execution_time = round(
            time.perf_counter() - start_time,
            2
        )

        logger.info(
            "Request completed in %s seconds",
            execution_time
        )

        # This trace describes recorded workflow stages.
        # It does not claim to contain private model reasoning.
        trace_metadata = {
            "execution_stages": execution_stages,
            "execution_plan": self._to_text(execution_plan),
            "selected_agents": selected_agents,
            "memory_used": memory_used,
            "research_output_available": bool(research_output),
            "threat_output_available": bool(threat_output),
            "report_output_available": bool(report_output),
            "consensus_output_available": bool(current_output.strip()),
            "retry_triggered": retry_triggered,
            "evaluation": self._to_text(evaluation),
            "recommendation": recommendation,
            "reflection_attempted": reflection_attempted,
            "revision_performed": revision_performed,
            "confidence_score": confidence_score,
        }

        return {
            "query": user_input,
            "response": current_output,
            "execution_time": execution_time,
            "confidence_score": confidence_score,
            "confidence_details": confidence,
            "memory_used": memory_used,
            "selected_agents": selected_agents,
            "evaluation": evaluation,
            "recommendation": recommendation,
            "decision_trace": decision_trace,
            "execution_stages": execution_stages,
            "trace_metadata": trace_metadata,
            "revision_performed": revision_performed,
            "reflection_attempted": reflection_attempted,
            "retry_triggered": retry_triggered,
            "execution_plan": self._to_text(execution_plan),
            "performance_report": performance_report,
        }
