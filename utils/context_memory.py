# utils/context_memory.py

class ContextMemory:
    def __init__(self):
        self.memory = {}

    def store(self, key, value):
        if key not in self.memory:
            self.memory[key] = []
        self.memory[key].append(value)

    def get_latest(self):
        if not self.memory:
            return None
        last_key = list(self.memory.keys())[-1]
        return self.memory[last_key][-1]

    def get_all(self, key):
        return self.memory.get(key, [])

    def summarize_history(self):
        summary = []
        for key, values in self.memory.items():
            summary.append(f"{key}: {values[-1]}")
        return "\n".join(summary)
