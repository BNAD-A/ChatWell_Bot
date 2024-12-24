import json
import random

class ChatbotEnv:
    def __init__(self, intents_file):
        with open(intents_file, 'r', encoding='utf-8') as file:
            self.data = json.load(file)
        self.actions = [intent["tag"] for intent in self.data["intents"]]
        self.state = None

    def reset(self):
        self.state = "waiting"
        return self.state

    def step(self, user_input):

        for intent in self.data["intents"]:
            for pattern in intent["patterns"]:
                if pattern.lower() in user_input.lower():
                    reward = 1  # Bonne correspondance
                    next_state = intent["tag"]
                    response = random.choice(intent["responses"])
                    return next_state, reward, response

        # Si aucune intention ne correspond
        reward = -1
        next_state = "confused"
        response = "Sorry, I can't understand. Could you rephrase?"
        return next_state, reward, response

    def get_possible_actions(self):
        return self.actions
