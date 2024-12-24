from flask import Flask, render_template, request, jsonify
from environment import ChatbotEnv
from agent import ChatbotAgent
import os

app = Flask(__name__)

env = ChatbotEnv('data.json')
agent = ChatbotAgent(actions=env.actions)

q_table_file = "q_table.npy"
if os.path.exists(q_table_file):
    agent.load_q_table(q_table_file)

state = env.reset()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def get_response():
    global state
    user_input = request.json.get("message", "")

    action = agent.choose_action(state)

    next_state, reward, response = env.step(user_input)

    agent.update_q_table(state, action, reward, next_state)

    agent.save_q_table(q_table_file)

    state = next_state

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
