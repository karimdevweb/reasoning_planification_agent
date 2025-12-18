from ollama import chat



# call the agent wit hdifferent query: 
def Agent_Call(basic_query):
    # call the model ollama
    basic_res = chat(
        model="mistral:latest",
        messages=[{"role": "user", "content": basic_query}],
        stream=False
    )
    print("--- reponse with basic query ----------")
    print(basic_res.message.content)
    
def Imporved_Query(improved_query):
    improved_res = chat(
        model="mistral:latest",
        messages=[{"role": "user", "content": improved_query}],
        stream=False
    )
    print("--- reponse with improved query ----------")
    print(improved_res.message.content)



# simple query
basic_query = "2 + 3 × 2 = ?"
improved_query = "Raisonne étape par étape avant de donner la réponse finale, combien cela fait 2 + 3 × 2 = ?"

Agent_Call(basic_query)
Imporved_Query(improved_query)