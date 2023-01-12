import plotly.graph_objects as go
import networkx as nx
import pandas as pd
from typing import Tuple


class Network:
    """Generates a network graph"""

    def __init__(self):
        pass

    def plot_networkgraph(self, df: pd.DataFrame) -> Tuple[str, object]:
        """Plots networkgraph
        Args:
            df (pd.DataFrame): takes in cosine similarity matrix
        Returns:
            Tuple[str, object]: returns the label and network plot
        """
        G = nx.from_pandas_edgelist(
            df, source="From", target="To", edge_attr="Weights", create_using=nx.Graph()
        )
        pos = nx.drawing.layout.spring_layout(G)
        nx.set_node_attributes(G, pos, "pos")

        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = G.nodes[edge[0]]["pos"]
            x1, y1 = G.nodes[edge[1]]["pos"]
            edge_x.append(x0)
            edge_x.append(x1)
            edge_x.append(None)
            edge_y.append(y0)
            edge_y.append(y1)
            edge_y.append(None)

        edge_trace = go.Scatter(
            x=edge_x,
            y=edge_y,
            line=dict(width=0.5, color="#888"),
            hoverinfo="none",
            mode="lines",
        )

        node_x = []
        node_y = []
        labels = []
        for node in G.nodes():
            x, y = G.nodes[node]["pos"]
            labels.append(node)
            node_x.append(x)
            node_y.append(y)

        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers",
            hoverinfo="text",
            marker=dict(
                showscale=True,
                # colorscale options
                #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
                #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
                #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
                colorscale="YlGnBu",
                reversescale=True,
                color=[],
                size=10,
                colorbar=dict(
                    thickness=15,
                    title="Node Connections",
                    xanchor="left",
                    titleside="right",
                ),
                line_width=2,
            ),
        )

        node_adjacencies = []
        node_text = []
        for node, adjacencies in enumerate(G.adjacency()):
            node_adjacencies.append(len(adjacencies[1]))
            node_text.append(f"{labels[node]}")

        node_trace.marker.color = node_adjacencies
        node_trace.text = node_text

        fig = go.Figure(
            data=[edge_trace, node_trace],
            layout=go.Layout(
                title=f"Network graph of top {df.shape[0]} links",
                titlefont_size=16,
                showlegend=False,
                hovermode="closest",
                margin=dict(b=20, l=5, r=5, t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            ),
        )
        return labels, fig
