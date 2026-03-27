class Memory:
    def __init__(self, max_history=5):
        self.history = []
        self.max_history = max_history

    def add(self, role, content):
        if not content:
            return

        self.history.append({
            "role": role,
            "content": content.strip()
        })

        if len(self.history) > self.max_history:
            self.history.pop(0)

    def get_context(self):
        return "\n".join(
            f"{h['role']}: {h['content']}"
            for h in self.history
        )

    def clear(self):
        self.history = []


memory = Memory()