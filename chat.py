import random
from environment import ChatbotEnv
from agent import ChatbotAgent
import numpy as np

env = ChatbotEnv("data.json")  

agent = ChatbotAgent(actions=env.actions)

try:
    agent.load_q_table("q_table.npy")
    print("Q-table loaded successfully.")
except FileNotFoundError:
    print("Q-table not found. The agent will start without prior training.")

state = env.reset()

print("\nWelcome to ChatWell - Your mental health companion.")
print("Type 'quit' to end the conversation.\n")

while True:
    user_input = input(" You : ").strip()
    if user_input.lower() == "quit":
        print("ChatWell : Take care ! See you soon..")
        break

    if not user_input:
        print("ChatWell : Please enter a valid message.")
        continue

    action = agent.choose_action(state)

    next_state, reward, response = env.step(user_input)

    print(f"ChatWell : {response}")

    agent.update_q_table(state, action, reward, next_state)

    try:
        agent.save_q_table("q_table.npy")
    except Exception as e:
        print(f"Error while saving the Q-table. : {e}")

    # Mettre à jour l'état
    state = next_state
