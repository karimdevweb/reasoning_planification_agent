from typing import TypedDict
from IPython.display import Image, display
from langgraph.graph import StateGraph, MessagesState, START, END 
# create a class
class CalcState(TypedDict):
    amount: float

# define some functions
def multiplyTimes10(state: CalcState):
    return {"amount": state["amount"] * 10}

def divideBy4(state: CalcState):
    return {"amount": state["amount"] / 4}

graph = StateGraph(CalcState)

# add to workflow
graph.add_node("multiplyTimes10" , multiplyTimes10)
graph.add_node( "divideBy4" , divideBy4) 

# set the limits
graph.add_edge(START, "multiplyTimes10")
graph.add_edge("multiplyTimes10", "divideBy4")
graph.add_edge("divideBy4", END)

# compile the graph
app = graph.compile()

# invoke the graph
result = app.invoke({"amount": 15})
print("--------------------result as img ------------------------")
img_data = app.get_graph().draw_mermaid_png()
with open("reasoning_planification_agent/graph.png", "wb") as f:
    f.write(img_data)

print("Graph saved as graph.png")

# display(Image(app.get_graph().draw_mermaid_png()))
print("--------------------result ------------------------")
print(result)
print("---------------------------------------------------")