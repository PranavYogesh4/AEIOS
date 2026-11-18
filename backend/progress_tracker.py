#Tracks execution progress so the frontend can show the current status of a task.
from threading import Lock


class ProgressTracker:

    def __init__(self):

        self.steps = []
        self.listeners = []

        self.lock = Lock()

    # ----------------------------------
    # Register Frontend Listener
    # ----------------------------------

    def subscribe(self, callback):

        self.listeners.append(callback)

    # ----------------------------------
    # Remove Listener
    # ----------------------------------

    def unsubscribe(self, callback):

        if callback in self.listeners:
            self.listeners.remove(callback)

    # ----------------------------------
    # Add New Step
    # ----------------------------------

    def add_step(self, step):

        with self.lock:

            data = {
                "step": step,
                "status": "completed"
            }

            self.steps.append(data)

            # Notify every listener
            for callback in self.listeners:

                callback(data)

    # ----------------------------------
    # Return All Steps
    # ----------------------------------

    def get_steps(self):

        return list(self.steps)

    # ----------------------------------
    # Clear Progress
    # ----------------------------------

    def clear(self):

        with self.lock:

            self.steps.clear()