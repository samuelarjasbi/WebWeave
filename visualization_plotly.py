# visualization_plotly.py
import plotly.graph_objects as go
import networkx as nx
from typing import List, Dict
from db_manager import DatabaseManager
from models import User, Relationship

class PlotlyGraphVisualizer:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self.graph = nx.DiGraph()
        self.node_positions = None
        self.edge_colors = []

    def build_graph_data(self):
        """Fetch data and prepare graph structure"""
        users: List[User] = self.db.session.query(User).all()
        relationships: List[Relationship] = self.db.session.query(Relationship).all()
        
        # Add nodes with metadata
        for user in users:
            self.graph.add_node(
                user.user_id,
                username=user.username,
                full_name=user.full_name
            )
        
        # Add edges with color coding
        for rel in relationships:
            source = rel.follower_id
            target = rel.followed_id
            is_mutual = self.graph.has_edge(target, source)
            
            color = "#00b4d8" if is_mutual else "#ff6d00"  # Blue for mutual, orange otherwise
            self.graph.add_edge(source, target, color=color)
            
        # Calculate node positions using spring layout
        self.node_positions = nx.spring_layout(self.graph, k=0.5, iterations=50, seed=42)

    def create_visualization(self, output_file: str = "social_graph.html"):
        """Generate interactive Plotly visualization"""
        # Prepare node data
        node_x = []
        node_y = []
        node_text = []
        node_hover = []
        
        for node_id in self.graph.nodes():
            x, y = self.node_positions[node_id]
            node_x.append(x)
            node_y.append(y)
            node_text.append(self.graph.nodes[node_id]['username'])
            node_hover.append(
                f"{self.graph.nodes[node_id]['full_name']}<br>"
                f"@{self.graph.nodes[node_id]['username']}"
            )

        # Create node trace
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            text=node_text,
            textposition="top center",
            hovertext=node_hover,
            hoverinfo="text",
            marker=dict(
                showscale=False,
                color='#1f77b4',
                size=20,
                line=dict(width=2, color='DarkSlateGrey')
        ))

        # Prepare edge data
        edge_traces = []
        for edge in self.graph.edges(data=True):
            x0, y0 = self.node_positions[edge[0]]
            x1, y1 = self.node_positions[edge[1]]
            
            edge_trace = go.Scatter(
                x=[x0, x1, None],
                y=[y0, y1, None],
                line=dict(width=1.5, color=edge[2]['color']),
                hoverinfo='none',
                mode='lines'
            )
            edge_traces.append(edge_trace)

        # Create figure
        fig = go.Figure(
            data=[*edge_traces, node_trace],
            layout=go.Layout(
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                xaxis=dict(showgrid=False, zeroline=False),
                yaxis=dict(showgrid=False, zeroline=False),
                plot_bgcolor='rgba(255,255,255,0.1)'
            )
        )

        # Add directional arrows
        for edge in self.graph.edges():
            fig.add_annotation(
                x=self.node_positions[edge[1]][0],
                y=self.node_positions[edge[1]][1],
                ax=self.node_positions[edge[0]][0],
                ay=self.node_positions[edge[0]][1],
                xref="x",
                yref="y",
                axref="x",
                ayref="y",
                showarrow=True,
                arrowhead=3,
                arrowsize=2,
                arrowwidth=1.5,
                arrowcolor=self.graph.edges[edge]['color']
            )

        # Save to HTML
        fig.write_html(output_file)
        print(f"Interactive visualization saved to {output_file}")