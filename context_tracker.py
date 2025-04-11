
from collections import deque

class ChatContext:
    def __init__(self, max_length=5):
        self.history = deque(maxlen=max_length)

    def add(self, user_input, bot_output):
        self.history.append((user_input, bot_output))

    def get(self):
        return list(self.history)
