from ollama import chat



# define the weather function 
def weather_call(city):
    return f"il fait 14 degrès à {city}"

# define alternative if météo is not in the query
def no_weather_call():
    return "you choose, not to ask about the weather ?  why ? don't you need me anymore"


# create a tool for the agent, helping it to choose
tools = [
    {
        "type": "function",
        "function": {
            "name": "weather_call",
            "description": "Obtenir la météo pour une ville",
            "parameters": {"type": "object", "properties": {"city": {"type": "string"}}, "required": ["city"]}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "no_weather_call",
            "description": "ne rien faire, genre glander"
        }
    }
]

# build a function to call the reAct agent
def react_agent(query):
    print("--------- query submitted ----------")
    print(query)
    print("")
    print("------------ first step (1) ----------------")
    print("Calling the LLM…")
    reasoning = chat(
        model="mistral:latest",
        messages=[{"role": "user", "content": f"réflichis à la question : {query}"}],
        stream=False
    )["message"]["content"]
    print("")
    print("------------ second step (2) ----------------")
    print("=> reasoning : ", reasoning)

    # action choisie par le LLM
    action_Res = chat(
        model="mistral:latest",
        messages=[{"role": "user", "content": f"choisis l'action à prendre pour la question : {query}"}],
        tools=tools,
        stream=False
    )
    fn_name= action_Res.message.tool_calls[0].function["name"]
    fn_args= action_Res.message.tool_calls[0].function["arguments"]
    print("")
    print("------------ third step (3) ----------------")
    print("=> Action : ", fn_name, "avec l'argument: ", fn_args)

    # observation
    observation_Res = chat(
        model="mistral:latest",
        messages=[{"role": "user", "content": f"donne une observation sur ton constat : {query}"}],
        stream=False
    )["message"]["content"]
    print("")
    print("------------ fourth step (4) ----------------")
    print("=> Observation : " , observation_Res)

    # réflexion finale du LLM
    reflection = chat(
        model="mistral:latest",
        messages=[{"role": "user", "content": f"Question : {query}\nObservation : {observation_Res}\nDonne la conclusion."}],
        stream=False
    )["message"]["content"]
    print("")
    print("------------ fifth step (5) ----------------")
    print("=> Réflexion : ", reflection)
    return reflection

query = "Question: Quelle est la météo à Paris ?"

react_agent(query)
