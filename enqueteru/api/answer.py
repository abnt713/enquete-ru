class Answer:

    status = 1
    messages = []
    content = {}

    def to_json(self):
        return {
            'status': self.status,
            'messages': self.messages,
            'content': self.content
        }