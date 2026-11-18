import time


class PerformanceMonitor:

    def __init__(self):

        self.start_times = {}
        self.execution_times = {}

    def start(self, name):

        self.start_times[name] = time.time()

    def stop(self, name):

        if name in self.start_times:

            self.execution_times[name] = (
                time.time()
                - self.start_times[name]
            )

    def report(self):

        report = "\n========== PERFORMANCE ==========\n\n"

        total = 0

        for agent, execution_time in self.execution_times.items():

            total += execution_time

            report += (
                f"{agent} : "
                f"{execution_time:.2f} sec\n"
            )

        report += (
            f"\nTotal Time : {total:.2f} sec\n"
        )

        report += "\n=================================\n"

        return report