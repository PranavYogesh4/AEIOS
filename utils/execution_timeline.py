from datetime import datetime


class ExecutionTimeline:

    def __init__(self):

        self.events = []

    def add_event(self, message):

        current_time = datetime.now().strftime(
            "%H:%M:%S"
        )

        self.events.append(
            (
                current_time,
                message
            )
        )

    def report(self):

        report = "\n========== EXECUTION TIMELINE ==========\n\n"

        for time, message in self.events:

            report += f"{time}  {message}\n"

        report += "\n========================================"

        return report