#Estimates the confidence level of the generated response.
import re


class ConfidenceAgent:
    """
    Calculates an adaptive response-quality score for AEIOS.

    The score is based on response structure, relevance, reasoning,
    actionable content, uncertainty handling, completeness, and
    execution indicators.

    This is a heuristic quality score, not a calibrated probability
    that the response is factually correct.
    """

    # Weight assigned to each quality criterion.
    WEIGHTS = {
        "relevance": 20,
        "structure": 10,
        "reasoning": 15,
        "risk_analysis": 10,
        "actionable_guidance": 15,
        "uncertainty_handling": 10,
        "conclusion": 10,
        "completeness": 10,
    }

    def evaluate(self, user_query, response):
        query = str(user_query or "").strip()
        text = str(response or "").strip()
        lower_text = text.lower()
        word_count = len(text.split())

        # An empty or failed response must never receive
        # an artificially high score.
        if not text:
            return self._format_result(
                0,
                "LOW",
                ["No response was generated."],
                {},
            )

        # --------------------------------------------------
        # 1. Evaluate response quality
        # --------------------------------------------------

        criteria = {
            "relevance": self._relevance(query, lower_text),
            "structure": self._has_structure(text),
            "reasoning": self._has_any(
                lower_text,
                [
                    "because",
                    "reason",
                    "reasoning",
                    "evidence",
                    "analysis",
                    "findings",
                    "based on",
                    "indicates",
                    "suggests",
                    "therefore",
                ],
            ),
            "risk_analysis": self._has_any(
                lower_text,
                [
                    "risk",
                    "impact",
                    "threat",
                    "severity",
                    "likelihood",
                    "vulnerability",
                    "mitigation",
                ],
            ),
            "actionable_guidance": self._has_any(
                lower_text,
                [
                    "recommend",
                    "recommendation",
                    "should",
                    "steps",
                    "actions",
                    "action plan",
                    "implement",
                    "prevent",
                    "solution",
                ],
            ),
            "uncertainty_handling": self._has_any(
                lower_text,
                [
                    "uncertain",
                    "unknown",
                    "not confirmed",
                    "may",
                    "might",
                    "could",
                    "cannot determine",
                    "insufficient information",
                    "limitation",
                    "assumption",
                ],
            ),
            "conclusion": self._has_any(
                lower_text,
                [
                    "conclusion",
                    "in summary",
                    "overall",
                    "to summarize",
                    "final recommendation",
                    "next steps",
                ],
            ),
            "completeness": self._has_completeness(
                text,
                word_count,
            ),
        }

        # --------------------------------------------------
        # 2. Calculate weighted score
        # --------------------------------------------------

        actual_score = sum(
            self.WEIGHTS[name]
            for name, passed in criteria.items()
            if passed
        )

        # --------------------------------------------------
        # 3. Apply quality penalties
        # --------------------------------------------------

        penalties = []

        if word_count < 15:
            actual_score = min(actual_score, 35)
            penalties.append(
                "Very short response: score capped at 35."
            )
        elif word_count < 40:
            actual_score = min(actual_score, 55)
            penalties.append(
                "Short response: score capped at 55."
            )
        elif word_count < 80:
            actual_score = min(actual_score, 70)
            penalties.append(
                "Limited response length: score capped at 70."
            )

        failure_phrases = [
            "execution failed",
            "traceback (most recent call last)",
            "an error occurred during execution",
        ]

        if any(
            phrase in lower_text
            for phrase in failure_phrases
        ):
            actual_score = min(actual_score, 25)
            penalties.append(
                "Execution failure indicator detected: score capped at 25."
            )

        incomplete_phrases = [
            "report generation incomplete",
            "response was truncated",
            "output was truncated",
            "response cut off",
        ]

        if any(
            phrase in lower_text
            for phrase in incomplete_phrases
        ):
            actual_score = min(actual_score, 50)
            penalties.append(
                "Explicit incomplete-output indicator detected: "
                "score capped at 50."
            )

        actual_score = max(0, min(100, round(actual_score)))

        # --------------------------------------------------
        # 4. Assign confidence level from the score
        # --------------------------------------------------

        if actual_score >= 90:
            level = "VERY HIGH"
        elif actual_score >= 80:
            level = "HIGH"
        elif actual_score >= 65:
            level = "MODERATE"
        elif actual_score >= 40:
            level = "LOW"
        else:
            level = "VERY LOW"

        # --------------------------------------------------
        # 5. Explain the score
        # --------------------------------------------------

        reasons = []

        for name, passed in criteria.items():
            status = "PASS" if passed else "MISSING"

            reasons.append(
                f"{name.replace('_', ' ').title()}: {status} "
                f"(weight: {self.WEIGHTS[name]} points)"
            )

        reasons.append(f"Response length: {word_count} words.")

        if penalties:
            reasons.extend(penalties)
        else:
            reasons.append("No explicit quality penalties applied.")

        reasons.append(
            "The score is a heuristic assessment of response quality, "
            "not a statistically calibrated probability of correctness."
        )

        return self._format_result(
            actual_score,
            level,
            reasons,
            criteria,
        )

    # --------------------------------------------------
    # Helper methods
    # --------------------------------------------------

    @staticmethod
    def _has_any(text, phrases):
        return any(phrase in text for phrase in phrases)

    @staticmethod
    def _has_structure(text):
        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        has_headings = any(
            re.match(
                r"^(#{1,6}\s|\d+[\.\)]\s|[-*]\s|"
                r"(summary|analysis|findings|conclusion|"
                r"recommendations|assessment|introduction|"
                r"methodology)\s*:)",
                line,
                re.IGNORECASE,
            )
            for line in lines
        )

        return has_headings or len(lines) >= 3

    @staticmethod
    def _relevance(query, response):
        if not query or not response:
            return False

        query_words = {
            word.lower()
            for word in re.findall(
                r"\b[a-zA-Z0-9]+\b",
                query,
            )
            if len(word) > 3
        }

        if not query_words:
            return True

        response_words = set(
            re.findall(
                r"\b[a-zA-Z0-9]+\b",
                response,
            )
        )

        overlap = len(query_words & response_words)
        relevance_ratio = overlap / len(query_words)

        return relevance_ratio >= 0.15

    @staticmethod
    def _has_completeness(text, word_count):
        lower_text = text.lower()

        # Very short responses are unlikely to be complete
        # for a request asking for a detailed report.
        if word_count < 40:
            return False

        report_indicators = [
            "executive summary",
            "analysis",
            "recommendations",
            "conclusion",
        ]

        present = sum(
            indicator in lower_text
            for indicator in report_indicators
        )

        # A shorter answer can still be complete if it has
        # enough substance and a clear conclusion.
        has_conclusion = any(
            phrase in lower_text
            for phrase in [
                "conclusion",
                "in summary",
                "overall",
            ]
        )

        if word_count >= 150 and has_conclusion:
            return True

        return present >= 3

    @staticmethod
    def _format_result(score, level, reasons, criteria):
        reason_text = "\n".join(
            f"- {reason}" for reason in reasons
        )

        return (
            f"Confidence Score: {score}\n\n"
            f"Confidence Level:\n{level}\n\n"
            f"Reason:\n{reason_text}"
        )
