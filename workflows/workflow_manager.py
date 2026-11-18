
class WorkflowManager:

    def determine_workflow(self, user_input):

        user_input = user_input.lower()

        if "report" in user_input:
            return "FULL_WORKFLOW"

        elif "attack" in user_input:
            return "THREAT_WORKFLOW"

        elif "threat" in user_input:
            return "THREAT_WORKFLOW"

        elif "malware" in user_input:
            return "THREAT_WORKFLOW"

        else:
            return "RESEARCH_WORKFLOW"

