#Combines or finalizes agent outputs. In your current updated version, it preserves the Report Agent's output directly.
from collaboration.agent_messenger import AgentMessenger
from utils.logger import logger


class ConsensusAgent:

    def __init__(self):
        self.messenger = AgentMessenger()

    def generate_consensus(
        self,
        research_output,
        threat_output,
        report_output,
    ):
        logger.info("ConsensusAgent: Processing agent outputs...")

        # The Report Agent already combines the research and threat
        # analysis. Preserve its completed report instead of asking
        # another model call to regenerate and potentially truncate it.
        report = str(report_output or "").strip()

        if report:
            logger.info(
                "ConsensusAgent: Preserving Report Agent output "
                "(%s characters).",
                len(report),
            )

            try:
                self.messenger.send_message(
                    "Consensus Agent",
                    "Orchestrator",
                    "Consensus completed by preserving the Report Agent output.",
                )
            except Exception:
                logger.exception(
                    "Consensus Agent messaging failed."
                )

            return report

        # Fallback if the Report Agent did not return a usable report.
        research = str(research_output or "").strip()
        threat = str(threat_output or "").strip()

        logger.warning(
            "ConsensusAgent: Report Agent output is empty. "
            "Using available agent findings as a fallback."
        )

        sections = [
            "## Report Generation Incomplete",
            (
                "The Report Agent did not provide a final report. "
                "The available agent findings are shown below."
            ),
        ]

        if research:
            sections.extend([
                "",
                "## Research Findings",
                research,
            ])

        if threat:
            sections.extend([
                "",
                "## Threat Analysis",
                threat,
            ])

        if not research and not threat:
            sections.extend([
                "",
                (
                    "Neither research nor threat analysis output "
                    "was available. A complete report could not "
                    "be assembled from the agent results."
                ),
            ])

        fallback_report = "\n\n".join(sections)

        try:
            self.messenger.send_message(
                "Consensus Agent",
                "Orchestrator",
                "Consensus fallback completed using available agent outputs.",
            )
        except Exception:
            logger.exception(
                "Consensus Agent messaging failed."
            )

        logger.info(
            "ConsensusAgent: Returning fallback output (%s characters).",
            len(fallback_report),
        )

        return fallback_report
