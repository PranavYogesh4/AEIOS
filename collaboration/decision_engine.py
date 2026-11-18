#Helps make decisions about how the system should proceed based on its configured logic.
class DecisionEngine:

    def decide_next_agent(self, current_agent, content):

        content = content.lower()

        if current_agent == "ResearchAgent":

            threat_keywords = [
                "attack",
                "malware",
                "ransomware",
                "phishing",
                "vulnerability",
                "exploit",
                "threat"
            ]

            if any(word in content for word in threat_keywords):
                return "ThreatAgent"

            return "ReportAgent"

        if current_agent == "ThreatAgent":
            return "ReportAgent"

        return None