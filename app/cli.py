# app/cli.py

from app.agents import UrbanAgent

if __name__ == "__main__":
    agent = UrbanAgent()
    user_input = input("Type your message: ")
    response = agent.respond(user_input)
    print(response)
