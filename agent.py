import random
import numpy as np

class ChatbotAgent:
    def __init__(self, actions, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0, exploration_decay=0.995):
        """
        Initialise l'agent avec les hyperparamètres RL et une Q-table vide.
        """
        self.q_table = {}
        self.actions = actions
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay

    def choose_action(self, state):
        # Exploration ou exploitation
        if np.random.rand() < self.exploration_rate:
            return random.choice(self.actions)  # Exploration
        return self.get_best_action(state)  # Exploitation

    def get_best_action(self, state):

        if state not in self.q_table:
            self.q_table[state] = {action: 0 for action in self.actions}
        return max(self.q_table[state], key=self.q_table[state].get)

    def update_q_table(self, state, action, reward, next_state):

        # Initialisation des états dans la Q-table si absents
        if state not in self.q_table:
            self.q_table[state] = {action: 0 for action in self.actions}
        if next_state not in self.q_table:
            self.q_table[next_state] = {action: 0 for action in self.actions}

        # Q-learning: Mise à jour de la valeur Q
        best_next_action = self.get_best_action(next_state)
        q_value = self.q_table[state][action]
        next_q_value = self.q_table[next_state][best_next_action]
        self.q_table[state][action] = q_value + self.learning_rate * (
            reward + self.discount_factor * next_q_value - q_value
        )

    def decay_exploration(self):

        self.exploration_rate *= self.exploration_decay
        self.exploration_rate = max(0.01, self.exploration_rate)  

    def save_q_table(self, filename):

        np.save(filename, self.q_table)

    def load_q_table(self, filename):

        self.q_table = np.load(filename, allow_pickle=True).item()
