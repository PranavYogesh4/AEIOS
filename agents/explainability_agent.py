#Produces information explaining the system's decisions and execution.
class ExplainabilityAgent:

    def generate_trace(
        self,
        memory_used,
        execution_plan,
        selected_agents,
        consensus_used,
        evaluation,
        recommendation,
        confidence
    ):

        trace = "\n========== DECISION TRACE ==========\n\n"

        # Memory
        trace += "Memory Reconstruction\n"
        trace += "----------------------\n"
        if memory_used:
            trace += "Status : USED\n"
        else:
            trace += "Status : NOT USED\n"

        trace += "\n"

        # Planning
        trace += "Planning Agent\n"
        trace += "--------------\n"
        trace += "Status : EXECUTED\n\n"
        trace += "Execution Plan\n"
        trace += "--------------\n"
        trace += execution_plan.strip()
        trace += "\n\n"

        # Task Router
        trace += "Task Router\n"
        trace += "-----------\n"
        trace += f"Selected Agents : {', '.join(selected_agents)}\n\n"

        # Consensus
        trace += "Consensus Agent\n"
        trace += "---------------\n"

        if consensus_used:
            trace += "Status : USED\n\n"
        else:
            trace += "Status : NOT USED\n\n"

        # Self Evaluation
        trace += "Self Evaluation\n"
        trace += "---------------\n"
        trace += evaluation.strip()
        trace += "\n\n"

        # Reflection
        trace += "Reflection\n"
        trace += "----------\n"
        trace += f"Recommendation : {recommendation}\n\n"

        # Confidence
        trace += "Confidence\n"
        trace += "----------\n"
        trace += confidence.strip()
        trace += "\n"

        trace += "=====================================\n"

        return trace