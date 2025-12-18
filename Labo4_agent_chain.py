from langchain_core.prompts import PromptTemplate
from langchain_ollama.llms import OllamaLLM



llm =OllamaLLM(model = "gemma2:2b")

prompt_1 = PromptTemplate.from_template("Résume ce texte : {text}") 
prompt_2 = PromptTemplate.from_template("Traduis en allemand : {text}") 
prompt_3 = PromptTemplate.from_template("Reformule en anglais : {text}") 

# assign model to each prompt
chain_1 = prompt_1 | llm
chain_2 = prompt_2 | llm
chain_3 = prompt_3 | llm

# chain the workflows
workflow = chain_1 | chain_2 | chain_3

result = workflow.invoke({"text": "Les agents IA transforment l’automatisation des entreprises."})
print(result)
