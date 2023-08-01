import yaml
import plotly.graph_objects as go

def read_yaml_file(file_path):
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)
    return data

def create_sankey_diagram(data):
    sources = list(set(item["Source"] for item in data))
    destinations = list(set(item["Destination"] for item in data))
    all_nodes = sources + destinations

    node_indices = {node: index for index, node in enumerate(all_nodes)}

    source_indices = [node_indices[item["Source"]] for item in data]
    destination_indices = [node_indices[item["Destination"]] for item in data]
    values = [item["Monthly Payment"] for item in data]

    # Assigning different colors to Source and Destination nodes
    source_colors = ["blue" for _ in sources]
    destination_colors = ["red" for _ in destinations]
    node_colors = source_colors + destination_colors

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=all_nodes,
            color=node_colors
        ),
        link=dict(
            source=source_indices,
            target=destination_indices,
            value=values
        )
    )])

    fig.update_layout(title_text="Flow", font_size=10)
    fig.show()

if __name__ == "__main__":
    yaml_file_path = "flow.yaml"
    data = read_yaml_file(yaml_file_path)
    create_sankey_diagram(data)
