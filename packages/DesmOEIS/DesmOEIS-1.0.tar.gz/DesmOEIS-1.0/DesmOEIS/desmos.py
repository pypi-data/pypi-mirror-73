import os
from sequence import Sequence

def create_expression(sequence, func):

    graph = open("../resources/desmos_graph_base.html")
    graph = graph.read()

    expr = func(sequence)

    # Add another placeholder comment below the expression to allow for further expressions
    graph = graph.replace("<!-- PLACEHOLDER -->", f"{expr} \n <!-- PLACEHOLDER -->")

    sequence.graph = graph

    dir = "../graphs/"
    if not os.path.exists(dir):
        os.makedirs(dir)
    filename = f"{dir}{sequence.id}.html"
    out_graph = open(filename, "w")
    out_graph.write(graph)

    return filename


def create_desmos_list(sequence):

    integers = sequence.integers

    desmos_list = str(integers)
    desmos_list = desmos_list.replace("'", "")

    name = sequence.name

    if sequence.args.get("name") is not None:
        name = name + "="
    else:
        name = ""

    expr = f"calculator.setExpression({{ id: 'graph1', latex:\"{name}{desmos_list}\" }});"
    return expr