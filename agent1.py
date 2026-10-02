import os
from datetime import datetime as dt
from pydantic_ai import Agent as ag
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider
model=OllamaModel("qwen2.5:1.5b",
                  provider=OllamaProvider(base_url="http://localhost:11434/v1"),)
def get_curr_time():
    return dt.now().strftime("%A,%B %d,%Y at %I:%M %p")
NOTES_FILE="notes.txt"
# def save_note(note:str) ->str:
#     with open(NOTES_FILE,"a",encoding="utf-8") as file:
#         file.write(f"-{note}\n")
#     return "Note Saved."    

def read_notes()->str:
    if not os.path.exists(NOTES_FILE):
        return "No Notes"
    with open(NOTES_FILE,encoding="utf-8") as file:
        return file.read()
agent=ag(
    model,tools=[get_curr_time,save_note,read_notes],
    instructions=(
        "you are a helful persoanl assistant running locally."
        "use your tools whenever they can help the question."
        "keep your answers short and friendly"
        "when the user asks you to save a note, you MUST call the save_note tool."
        "do not write tool calls as text or JSON."),
    )
def main():
    print("I am ready SIR !!!!!!! TYPE quit or exit for tata byebye \n")
    hist=[]
    while True:
        usrinp=input("YOU -> ")
        if usrinp.strip().lower() in ("quit","exit"):
            break
        result=agent.run_sync(usrinp,message_history=hist)
        hist=result.all_messages()
        print(f"\nAGENTS -> {result.output}\n")
if __name__=="__main__":
    main()