#Routes user requests or tasks to the appropriate agents based on routing rules.
class TaskRouter:

    def route(self, query):

        query = query.lower()

        selected_agents = []

        # -----------------------------
        # Research Agent
        # -----------------------------
        if any(word in query for word in [
            "research",
            "latest",
            "trend",
            "news",
            "technology",
            "cybersecurity",
            "cyber",
            "ai",
            "attack",
            "overview",
            "explain",
            "what is",
            "information"
        ]):
            selected_agents.append("ResearchAgent")

        # -----------------------------
        # Threat Agent
        # -----------------------------
        if any(word in query for word in [
            "threat",
            "risk",
            "severity",
            "malware",
            "ransomware",
            "phishing",
            "exploit",
            "vulnerability",
            "mitigation",
            "defense",
            "analysis"
        ]):

            if "ThreatAgent" not in selected_agents:
                selected_agents.append("ThreatAgent")

        # -----------------------------
        # Planning Agent
        # -----------------------------
        if any(word in query for word in [
            "plan",
            "roadmap",
            "workflow",
            "strategy",
            "steps"
        ]):

            selected_agents.append("PlanningAgent")

        # -----------------------------
        # Memory Reconstruction
        # -----------------------------
        if any(word in query for word in [
            "remember",
            "previous",
            "before",
            "last",
            "earlier",
            "continue"
        ]):

            selected_agents.append("ReconstructionAgent")

        # -----------------------------
        # Report Agent
        # -----------------------------
        if any(word in query for word in [
            "report",
            "summary",
            "summarize",
            "document",
            "presentation"
        ]):

            selected_agents.append("ReportAgent")

        # -----------------------------
        # Default Pipeline
        # -----------------------------
        if len(selected_agents) == 0:

            selected_agents = [
                "ResearchAgent",
                "ThreatAgent",
                "ReportAgent"
            ]

        return list(dict.fromkeys(selected_agents))