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
def save_note(note:str) ->str:
    with open(NOTES_FILE,"a",encoding="utf-8") as file:
        file.write(f"-{note}\n")
    return "Note Saved."    
SAVE_FOLDER="files"
def list_files() -> str:
    if not os.path.exists(SAVE_FOLDER):
        return "Folder does not exist."
    files=os.listdir(SAVE_FOLDER)
    if not files:
        return "The folder is emplty"
    result="Files in folder:\n"
    for filename in files:
        path=os.path.join(SAVE_FOLDER,filename)
        if os.path.isfile(path):
            size=os.path.getsize(path)
            result+=f"-{filename} ({size} bytes)\n"
    return result
def read_file(filename:str)->str:
    path=os.path.join(SAVE_FOLDER,filename)
    if not os.path.exists(path):
        return f"File {filename} does not existssss"
    with open(path,"r",encoding ="utf-8") as file:
        contents=file.read()
    return (f"File : {filename}\n" f"Path: {os.path.abspath(path)}\n"
            f"Size: {os.path.getsize(path)} bytes\n\n"
            f"Content:\n{contents}")
def del_file(filename:str)->str:
    path=os.path.join(SAVE_FOLDER,filename)
    if not os.path.exists(path):
        return f"File {filename} does not existsssssssssss"
    os.remove(path)
    return f"File {filename} deleted successfullyyyy"
def save_file(filename:str,content:str) ->str:
    path=os.path.join(SAVE_FOLDER,filename)
    with open(path,"w",encoding="utf-8") as file:
        file.write(content)
    return f"File '{filename}' saved successfully.\n AT path '{path}"
def read_notes()->str:
    if not os.path.exists(NOTES_FILE):
        return "No Notes"
    with open(NOTES_FILE,encoding="utf-8") as file:
        return file.read()
agent=ag(
    model,tools=[save_file,get_curr_time,save_note,read_notes,del_file,read_file,list_files],
    instructions=(
        "you are a helful persoanl assistant running locally."
        "use your tools whenever they can help the question."
        "keep your answers short and friendly"
        "when the user asks you to save a note, you MUST call the save_note tool."
        "do not write tool calls as text or JSON."
        "automatically choose a suitable filename and extension based on the requested content. "
        "if the user does not provide a filename, create a sensible filename yourself. "
        "support any file extension such as txt, py, java, c, cpp, js, html, css, json, etc. "
        "you can create multiple files when requested. "),
    )
def main():
    print("I am ready SIR !!!!!!! TYPE quit or exit or bye for tata byebye \n")
    hist=[]
    while True:
        usrinp=input("YOU -> ")
        if usrinp.strip().lower() in ("quit","exit","bye"):
            break
        result=agent.run_sync(usrinp,message_history=hist)
        hist=result.all_messages()
        print(f"\nAGENTS -> {result.output}\n")
if __name__=="__main__":
    main()