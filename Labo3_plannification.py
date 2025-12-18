from ollama import chat



# -- define some functions 
#  geving info about a topic
def basket_info():
    return ("""Le basketball est un sport collectif opposant deux équipes de cinq joueurs.
            Il se joue sur un terrain avec un panier à chaque extrémité, et l’objectif est de marquer des points en lançant le ballon dans le panier adverse.
            Le jeu implique dribbles, passes, tirs et stratégies d’équipe.
            Il existe des ligues professionnelles comme la NBA et des compétitions internationales comme les Jeux Olympiques.""")

def stock_info():
    return ("""La bourse est un marché financier où s’échangent des actions, obligations et autres instruments financiers.
            Elle permet aux entreprises de lever des fonds et aux investisseurs d’acheter ou vendre des titres.
            Les prix varient selon l’offre, la demande et les informations économiques, ce qui peut générer des gains ou des pertes.""")

# sommerize the topic
def summarize(text):
    prompt = f"Résume ce texte de façon concise : {text}"
    resp = chat(
        model="mistral:latest",
        messages=[{"role": "user", "content": prompt}],
        stream=False
    )
    return resp["message"]["content"]

# send email
def send_email( content,  recipient = "team@email.com"):
    return f"Email envoyé à {recipient} avec le contenu : {content[:50]}..."


# func mapping
func_mapping = {
    "basket_info": {"func": basket_info, "description": "cette function retourne un paragraphe sur le basket."},
    "stock_info": {"func": stock_info, "description": "cette function retourne un paragraphe sur la bourse."},
    "summarize": {"func": summarize, "description": "cette function résume un texte."},
    "send_email": {"func": send_email, "description": "cette function envoie un texte par email."}
}


#  define the tools containing the functions
tools = [
    {
        "type": "function",
        "function": {
            "name": "basket_info",
            "description": "une function qui cherche des infos sur le basket.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "stock_info",
            "description": "une function qui cherche des infos sur la bourse.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "summarize",
            "description": "une function qui résume un texte.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"}
                },
                "required": ["text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "une function qui envoye un email",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {"type": "string"},
                    "recipient": {"type": "string"}
                },
                "required": ["content"]
            }
        }
    }
]





# calling the agent with tools
def Call_Agent_With_Tools(prompt, tools):
    resp = chat(
            model="gpt-oss:latest",
            messages=[{"role":"user","content":prompt}],
            tools=tools,
            stream=False
        )
    return resp



# the Planner
def planner(goal):
    return ["Chercher", "Résumer", "Envoyer"] 


# the Executor
def executor(goal, query , recipient):
    plan = planner(goal)
    results = []
    output = ""
    fn_name = None

    for step in plan:
        # ask LLM wich action to call
        # prompt = (
        #     f"Étape : {step}\n"
        #     f"Question : {query}\n"
        # )
        prompt = (
            f"Étape : {step}\n"
            f"Question : {query}\n"
            f"Résultat précédent : {output}\n"
            "Utilise les outils disponibles pour accomplir cette étape.\n"
            "Réponds en appelant UNE fonction."
        )

        try:
            resp = Call_Agent_With_Tools(prompt , tools)
            fn_name= resp.message.tool_calls[0].function["name"]
        except Exception as e:
            print(e)
            print(resp)
        if not resp.message.tool_calls:
            content = resp.message.content
            print(content)
            # raise ValueError("Aucune fonction appelée par le modèle")
        if fn_name == "basket_info" or  fn_name == "stock_info":
            output = func_mapping[fn_name]["func"]()

        elif len(output)>0 and fn_name == "summarize":
            output = func_mapping[fn_name]["func"](output)
        elif len(output)>0 and fn_name == "send_email":
            output = func_mapping[fn_name]["func"]( output, recipient)
        else:
            output = f"Aucune fonction correspondante trouvée pour l'étape {step}."

        results.append((step, fn_name, output))
        print(f"Étape : {step}\nFonction choisie : {fn_name}\nRésultat : {output}\n")

    return results



# Exemple d'utilisation
goal = "Préparer un résumé sur le sujet partagé et l'envoyer"
query = """basket ball tu connais ?"""
recipient = "blabla@email.com"

result = executor(goal, query , recipient)
