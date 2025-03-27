import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).parent.absolute()))



import math
from flask import Flask, render_template, jsonify
from sqlalchemy import func, or_
from db_manager import DatabaseManager
from models import User, Relationship



app = Flask(__name__)

def get_graph_data():
    """Fetch nodes and edges with connection-based sizing and coloring"""
    db = DatabaseManager()
    nodes = []
    edges = []
    
    # Calculate connection counts (followers + following)
    users = db.session.query(
        User.user_id,
        User.username,
        User.full_name,
        (func.count(Relationship.follower_id) + 
        func.count(Relationship.followed_id)).label('degree')
    ).outerjoin(Relationship, or_(
        User.user_id == Relationship.follower_id,
        User.user_id == Relationship.followed_id
    )).group_by(User.user_id).all()

    # Find maximum degree for normalization
    max_degree = max(user.degree for user in users) if users else 1
    
    # Create nodes with size and color based on connection count
    for user in users:
        # Size between 20-50 based on degree
        normalized_size = 20 + (user.degree / max_degree) * 30
        
        # Color intensity based on degree (darker for more connections)
        color_intensity = min(0.7, user.degree / max_degree * 0.7)
        color = f"hsl(210, 60%, {50 - color_intensity*30}%)"  # Darker blue for more connections
        
        nodes.append({
            'id': user.user_id,
            'label': user.username,
            'title': f"{user.full_name}\nConnections: {user.degree}",
            'value': normalized_size,
            'color': color
        })
    
    # Create edges with mutual detection
    relationships = db.session.query(Relationship).all()
    for rel in relationships:
        is_mutual = db.session.query(Relationship).filter_by(
            follower_id=rel.followed_id,
            followed_id=rel.follower_id
        ).first() is not None
        
        edges.append({
            'from': rel.follower_id,
            'to': rel.followed_id,
            'arrows': 'to',
            'color': {'color': '#00b4d8'} if is_mutual else {'color': '#ff6d00'},  # Fixed color format
            'width': 4 if is_mutual else 2
        })
    
    db.close()
    return {'nodes': nodes, 'edges': edges}

@app.route('/')
def index():
    return render_template('network.html')

@app.route('/api/graph')
def graph_data():
    return jsonify(get_graph_data())

if __name__ == '__main__':
    app.run(debug=True)