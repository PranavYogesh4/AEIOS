#Adjusts the execution strategy based on the task or execution conditions, according to the implemented rules.
from utils.logger import logger
from engine.intent_classifier import IntentClassifier


class AdaptiveExecutionEngine:

    def __init__(self):

        self.intent_classifier = IntentClassifier()

    def optimize_execution(self, selected_agents, user_input):

        logger.info("Adaptive Execution Engine Activated")

        intent = self.intent_classifier.classify(user_input)

        logger.info(f"Execution Intent : {intent}")

        execution_plan = []

        # --------------------------------------------------
        # GREETING
        # --------------------------------------------------

        if intent == "GREETING":

            execution_plan = [
                "ReportAgent"
            ]

        # --------------------------------------------------
        # RESEARCH
        # --------------------------------------------------

        elif intent == "RESEARCH":

            if "ResearchAgent" in selected_agents:
                execution_plan.append("ResearchAgent")

            execution_plan.append("ReportAgent")

        # --------------------------------------------------
        # THREAT ANALYSIS
        # --------------------------------------------------

        elif intent == "THREAT_ANALYSIS":

            if "ResearchAgent" in selected_agents:
                execution_plan.append("ResearchAgent")

            if "ThreatAgent" in selected_agents:
                execution_plan.append("ThreatAgent")

            execution_plan.append("ReportAgent")

        # --------------------------------------------------
        # REPORT
        # --------------------------------------------------

        elif intent == "REPORT":

            execution_plan = [
                "ReportAgent"
            ]

        # --------------------------------------------------
        # MULTI AGENT
        # --------------------------------------------------

        elif intent == "MULTI_AGENT":

            execution_plan = selected_agents.copy()

            if "ReportAgent" not in execution_plan:
                execution_plan.append("ReportAgent")

        # --------------------------------------------------
        # GENERAL
        # --------------------------------------------------

        else:

            execution_plan = selected_agents.copy()

            if "ReportAgent" not in execution_plan:
                execution_plan.append("ReportAgent")

        logger.info("=" * 60)
        logger.info("FINAL EXECUTION PLAN")
        logger.info(str(execution_plan))
        logger.info("=" * 60)

        return execution_plan