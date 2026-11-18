#Manages execution analytics, such as performance metrics and recorded results.
from datetime import datetime


class AnalyticsManager:

    def __init__(self):

        self.total_queries = 0

        self.execution_times = []

        self.confidence_scores = []

        self.memory_hits = 0

        self.agent_usage = {
            "ResearchAgent": 0,
            "ThreatAgent": 0,
            "ReportAgent": 0,
            "ConsensusAgent": 0,
            "ReflectionAgent": 0,
            "RetryEngine": 0
        }

        self.query_history = []

    # -----------------------------------------

    def record_query(
        self,
        query,
        execution_time,
        confidence_score,
        memory_used,
        selected_agents
    ):

        self.total_queries += 1

        self.execution_times.append(execution_time)

        self.confidence_scores.append(confidence_score)

        if memory_used:
            self.memory_hits += 1

        for agent in selected_agents:

            if agent in self.agent_usage:
                self.agent_usage[agent] += 1

        self.query_history.insert(
            0,
            {
                "query": query,
                "time": datetime.now().strftime("%H:%M:%S")
            }
        )

        self.query_history = self.query_history[:20]

    # -----------------------------------------

    def average_execution_time(self):

        if not self.execution_times:
            return 0

        return round(
            sum(self.execution_times) /
            len(self.execution_times),
            2
        )

    # -----------------------------------------

    def average_confidence(self):

        if not self.confidence_scores:
            return 0

        return round(
            sum(self.confidence_scores) /
            len(self.confidence_scores),
            1
        )

    # -----------------------------------------

    def memory_hit_rate(self):

        if self.total_queries == 0:
            return 0

        return round(
            self.memory_hits /
            self.total_queries * 100,
            1
        )

    # -----------------------------------------

    def get_statistics(self):

        return {

            "total_queries": self.total_queries,

            "average_execution_time":
            self.average_execution_time(),

            "average_confidence":
            self.average_confidence(),

            "memory_hit_rate":
            self.memory_hit_rate(),

            "agent_usage":
            self.agent_usage,

            "query_history":
            self.query_history
        }