# app/app.py

from app.agents import UrbanAgent

if __name__ == "__main__":
    agent = UrbanAgent()
    user_input = input("Escribe tu mensaje: ")
    response = agent.respond(user_input)
    print(response)
