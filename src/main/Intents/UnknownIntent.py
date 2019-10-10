from src.main.Intents.IntentBase import IntentBase

class UnknownIntent(IntentBase):
    def __init__(self, request):
        self.request = request

    def ProcessRespone(self):
        response = "Sorry, I did not understand your question, could you please ask a different question?"
        return response