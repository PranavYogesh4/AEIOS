
from concurrent.futures import ThreadPoolExecutor, as_completed

from utils.logger import logger
from utils.performance_monitor import PerformanceMonitor


class ParallelExecutor:

    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=3)
        self.performance_monitor = PerformanceMonitor()

    @staticmethod
    def _extract_content(result, agent_name):
        """Safely extract an agent's text output."""
        if isinstance(result, dict):
            content = result.get("content", "")
        else:
            content = result

        if content is None:
            content = ""

        content = str(content).strip()

        if not content:
            logger.warning("%s returned empty content.", agent_name)

        return content

    def execute(
        self,
        selected_agents,
        research_agent,
        threat_agent,
        report_agent,
        user_input,
    ):
        logger.info("Parallel Executor Activated")

        research_output = ""
        threat_output = ""
        report_output = ""

        futures = {}

        if "ResearchAgent" in selected_agents:
            self.performance_monitor.start("Research Agent")
            futures[
                self.executor.submit(
                    research_agent.research_topic,
                    user_input,
                )
            ] = ("research", "Research Agent")

        if "ThreatAgent" in selected_agents:
            self.performance_monitor.start("Threat Agent")
            futures[
                self.executor.submit(
                    threat_agent.analyze_threat,
                    user_input,
                )
            ] = ("threat", "Threat Agent")

        for future in as_completed(futures):
            output_key, agent_name = futures[future]

            try:
                result = future.result()
                content = self._extract_content(result, agent_name)

                if output_key == "research":
                    research_output = content
                else:
                    threat_output = content

                logger.info(
                    "%s completed with %s characters.",
                    agent_name,
                    len(content),
                )

            except Exception:
                logger.exception("%s failed.", agent_name)

                error_message = (
                    f"{agent_name} failed during execution. "
                    "Check the execution logs for details."
                )

                if output_key == "research":
                    research_output = error_message
                else:
                    threat_output = error_message

            finally:
                self.performance_monitor.stop(agent_name)

        if "ReportAgent" in selected_agents:
            self.performance_monitor.start("Report Agent")

            try:
                report_input = (
                    "USER REQUEST:\n"
                    f"{user_input}\n\n"
                    "RESEARCH ANALYSIS:\n"
                    f"{research_output or 'Research output unavailable.'}\n\n"
                    "THREAT ANALYSIS:\n"
                    f"{threat_output or 'Threat output unavailable.'}"
                )

                report_output = report_agent.generate_report(report_input)

            except Exception:
                logger.exception("Report Agent failed.")

                report_output = (
                    "## Report Generation Failed\n\n"
                    "The Report Agent could not generate the report. "
                    "Check the execution logs for details."
                )

            finally:
                self.performance_monitor.stop("Report Agent")

        logger.info(
            "Parallel execution finished. Research=%s chars, "
            "Threat=%s chars, Report=%s chars.",
            len(research_output),
            len(threat_output),
            len(str(report_output or "")),
        )

        performance_report = self.performance_monitor.report()

        return (
            research_output,
            threat_output,
            report_output,
            performance_report,
        )
