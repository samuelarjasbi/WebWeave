# visualization.py
from pyvis.network import Network
from db_manager import DatabaseManager
from typing import Optional, Tuple
from models import User, Relationship 
import os

# Add this path configuration before creating the Network
template_dir = os.path.join(os.path.dirname(net.__file__), 'templates')
os.environ["PYVIS_TEMPLATE_PATH"] = template_dir
class SocialGraph:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self.net = Network(
            height="750px",
            width="100%",
            bgcolor="#222222",
            font_color="white",
            directed=True,
            notebook=False
            
        )
        self._configure_physics()

    def _configure_physics(self):
        """Configure the physics simulation for better layout"""
        self.net.set_options("""
        {
            "physics": {
                "barnesHut": {
                    "gravitationalConstant": -80000,
                    "springLength": 250,
                    "springConstant": 0.001
                },
                "minVelocity": 0.75
            }
        }
        """)

    def build_graph(self, mutual_color: str = "#00b4d8", 
                   unidirectional_color: str = "#ff6d00"):
        """
        Build the network graph from database relationships
        Args:
            mutual_color: Color for mutual follows
            unidirectional_color: Color for one-way follows
        """
        self._add_nodes()
        self._add_edges(mutual_color, unidirectional_color)

    def _add_nodes(self):
        """Add all users as nodes to the graph"""
        users = self.db.session.query(User).all()
        for user in users:
            self.net.add_node(
                n_id=user.user_id,
                label=user.username,
                title=f"{user.full_name}\n@{user.username}",
                color="#adb5bd"
            )

    def _add_edges(self, mutual_color: str, unidirectional_color: str):
        """Add relationship edges with appropriate coloring"""
        relationships = self.db.session.query(Relationship).all()
        
        for rel in relationships:
            mutual = self._is_mutual_relationship(rel.follower_id, rel.followed_id)
            color = mutual_color if mutual else unidirectional_color
            width = 3 if mutual else 2
            
            self.net.add_edge(
                source=rel.follower_id,
                to=rel.followed_id,
                color=color,
                width=width,
                title=self._get_edge_title(rel, mutual)
            )

    def _is_mutual_relationship(self, user_a_id: int, user_b_id: int) -> bool:
        """Check if two users follow each other mutually"""
        return self.db.session.query(Relationship).filter_by(
            follower_id=user_b_id,
            followed_id=user_a_id
        ).first() is not None

    def _get_edge_title(self, rel: Relationship, mutual: bool) -> str:
        """Generate tooltip text for edges"""
        follower = self.db.get_user_by_id(rel.follower_id)
        followed = self.db.get_user_by_id(rel.followed_id)
        relation_type = "Mutual follow" if mutual else "One-way follow"
        return f"{relation_type}\n{follower.username} → {followed.username}"

    def visualize(self, output_file: str = "social_network.html"):
        """Generate and save the interactive visualization"""
        self.net.show(output_file)
        print(f"Visualization saved to {output_file}")

    def get_node_and_edge_counts(self) -> Tuple[int, int]:
        """Return counts for nodes and edges"""
        return len(self.net.nodes), len(self.net.edges)