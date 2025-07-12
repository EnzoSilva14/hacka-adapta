from crew import create_crew
from streaming_handler import StreamingHandler
from langchain.chat_models import ChatOpenAI

if __name__ == "__main__":
    crew = create_crew()
    
    resultado = crew.kickoff(inputs={
        "tema": "Inteligência Artificial na Educação"
    })

    print("\n🧠 Resultado final da Crew:\n")
    print(resultado)
