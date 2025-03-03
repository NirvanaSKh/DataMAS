import matplotlib.pyplot as plt

def generate_graph(dataframe, graph_type):
    plt.figure(figsize=(8, 5))

    if graph_type == "bar_chart":
        dataframe.plot(kind="bar")
    elif graph_type == "line_chart":
        dataframe.plot(kind="line")
    elif graph_type == "pie_chart":
        dataframe.iloc[:, 1].plot(kind="pie", labels=dataframe.iloc[:, 0])

    plt.title("Generated Graph")
    plt.grid(True)
    plt.show()
