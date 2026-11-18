#Generates the final structured report, including your six sections.
from groq import Groq

from config import GROQ_API_KEY
from collaboration.agent_messenger import AgentMessenger
from utils.logger import logger


client = Groq(api_key=GROQ_API_KEY)


class ReportAgent:

    def __init__(self):
        self.messenger = AgentMessenger()
        self.model = "openai/gpt-oss-120b"

    def generate_report(self, content):

        try:
            self.messenger.send_message(
                "Report Agent",
                "Orchestrator",
                "Final report generation started.",
            )
        except Exception:
            logger.exception("Agent messaging failed.")

        logger.info("ReportAgent: Generating final report...")

        input_text = str(content or "").strip()

        # Fallback when no input is supplied.
        if not input_text:
            logger.warning(
                "Empty report input. Using a general cloud security request."
            )

            input_text = """
Generate a report on data privacy and security risks in cloud computing.
Include threats, causes, impacts, risk assessment, five security measures,
an implementation plan, agent execution summary, decision trace,
confidence assessment, and conclusion.
Use established cybersecurity knowledge and do not invent evidence.
"""

        # Preserve the beginning and end of large inputs.
        max_input_chars = 16000

        if len(input_text) > max_input_chars:
            marker = "\n\n[Middle content omitted]\n\n"
            available = max_input_chars - len(marker)
            head_size = int(available * 0.65)
            tail_size = available - head_size

            input_text = (
                input_text[:head_size]
                + marker
                + input_text[-tail_size:]
            )

            logger.warning(
                "Report input shortened to %s characters.",
                len(input_text),
            )

        
        prompt = f"""
You are the AEIOS Report Generation Agent.

USER REQUEST AND AGENT OUTPUTS:
{input_text}

Generate a SHORT, clear, complete response using exactly six sections.

1. EXECUTIVE SUMMARY
Summarize the situation, main risks, and key findings in 3-4 sentences.

2. MAJOR THREATS
Explain the three most important threats, their causes, and impacts.
Use concise bullet points.

3. THREAT AND RISK ASSESSMENT
Rate each threat as High, Medium, or Low for likelihood and impact.
Briefly explain the priority. Do not invent numerical scores.

4. FIVE SECURITY RECOMMENDATIONS
Give exactly five practical security measures.
Explain each in one or two sentences.

5. IMPLEMENTATION PLAN AND AGENT EXECUTION
Give a short prioritized plan with timelines:
- Immediate: 0-7 days
- Short term: weeks 2-4
- Medium term: months 2-3
Briefly summarize available agent execution details, evaluation,
decision trace, and confidence. Do not invent missing metadata.

6. CONCLUSION
Write a concise final paragraph summarizing the main risks
and the most important next action.

RULES:
- Keep the entire response around 500-700 words.
- Complete all six sections.
- Keep every section brief and useful.
- Never ask the user for more information.
- If agent findings are unavailable, use established general knowledge.
- Clearly distinguish general knowledge from verified findings.
- Do not invent statistics, citations, evidence, or agent activity.
- Do not create large tables or repeat the same information.
- The Conclusion must be the final section.
- Never omit the Conclusion to shorten the response.
- Return only the completed response.
"""

        try:
            completion = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                temperature=0.2,
                max_tokens=9000,
            )

            choice = completion.choices[0]
            report = (choice.message.content or "").strip()
            finish_reason = getattr(choice, "finish_reason", None)

            logger.info(
                "ReportAgent generated %s characters; finish_reason=%s",
                len(report),
                finish_reason,
            )

            if not report:
                logger.error("ReportAgent returned an empty response.")

                return (
                    "## Report Generation Failed\n\n"
                    "The model returned an empty response. "
                    "Check the application logs."
                )

            if finish_reason == "length":
                logger.warning(
                    "ReportAgent reached its output-token limit."
                )

                report += (
                    "\n\n**Generation warning:** The model reached "
                    "its output-token limit. The report may be incomplete."
                )

            return report

        except Exception as error:
            logger.exception("ReportAgent failed during generation.")

            return (
                "## Report Generation Failed\n\n"
                f"Error type: {type(error).__name__}\n\n"
                "Check the application logs for details. "
                "The report could not be generated."
            )