import random 
from environment import ChatbotEnv
from agent import ChatbotAgent

env = ChatbotEnv("data.json")  

agent = ChatbotAgent(actions=env.actions)

num_episodes = 1000
max_steps = 10

print("Début de l'entraînement...\n")

for episode in range(num_episodes):
    state = env.reset()
    total_reward = 0

    for _ in range(max_steps):
        user_input = random.choice(
            [pattern for intent in env.data["intents"] for pattern in intent["patterns"]]
        )

        action = agent.choose_action(state)

        next_state, reward, response = env.step(user_input)

        agent.update_q_table(state, action, reward, next_state)
        
        state = next_state
        total_reward += reward

        if state in ["confused", "unknown"]:
            break

    # Décroître le taux d'exploration après chaque épisode
    agent.decay_exploration()

    # Afficher le progrès tous les 100 épisodes
    if (episode + 1) % 100 == 0:
        print(f"Épisode {episode + 1}/{num_episodes} - Récompense totale : {total_reward}")

print("\nEntraînement terminé.")
print("Sauvegarde de la Q-table...")

agent.save_q_table("q_table.npy")
print("Q-table sauvegardée avec succès sous le nom 'q_table.npy'.")
