class Memory:
    def __init__(self,max_history=5):
        self.history = []
        self.max_history = max_history


    def add(self, role,content):
        self.history.append({"role":role,"content":content})

        if len(self.history) > self.max_history:
            self.history.pop(0)

    def get_context(self):
        context=""
        for h in self.history:
            context+=f"{h['role']}:{h['content']}\n"
        return context

memory = Memory()