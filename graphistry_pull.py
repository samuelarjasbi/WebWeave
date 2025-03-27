# visualize.py - Corrected version
import graphistry
from fetch_data import get_users, get_relationships

graphistry.register(api=3, personal_key_id="F4OB1DPX05", personal_key_secret="4AX5RNHF4CE168PY")

def visualize_network():
    users_df = get_users().rename(columns={'user_id': 'id', 'username': 'label'})
    edges_df = get_relationships()
    
    # Create explicit edge type labels
    edges_df['connection_type'] = edges_df['edge_color'].map({
        'blue': 'Mutual Follow',
        'orange': 'One-way Follow'
    })
    
    # Create the plotter with proper encodings
    plotter = (
        graphistry
        .bind(
            source='src',
            destination='dst',
            node='id',
            point_title='label'
        )
        .nodes(users_df)
        .edges(edges_df)
        .encode_edge_color(
            'connection_type',
            categorical_mapping={
                'Mutual Follow': 'blue',
                'One-way Follow': 'orange'
            }
        )
        .settings(url_params={
            'showLegend': True,
            'edgeStyle': 'dotted',
            'edgeOpacity': 0.7,
            'pointSize': 2.5
        })
    )
    
    return plotter.plot()

if __name__ == "__main__":
    visualize_network()