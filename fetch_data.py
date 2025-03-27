import pandas as pd
from sqlalchemy import create_engine

POSTGRES_URI = "postgresql://postgres:Mm%40%4082651@localhost/socialdb"
engine = create_engine(POSTGRES_URI)

def get_users():
    # Only select necessary columns for Graphistry
    return pd.read_sql("SELECT user_id, username FROM users", engine)

# Updated fetch_data.py (improved relationship analysis)
def get_relationships():
    # Get all relationships
    df = pd.read_sql("SELECT follower_id as src, followed_id as dst FROM relationships", engine)
    
    # Create mirrored version for mutual check
    reversed_df = df.rename(columns={'src': 'dst', 'dst': 'src'})
    
    # Find mutual connections using merge
    mutual = df.merge(reversed_df, on=['src', 'dst'], how='inner')
    mutual['connection_type'] = 'mutual'
    
    # Create full edge list with types
    final_df = df.merge(mutual[['src', 'dst', 'connection_type']], 
                      on=['src', 'dst'], 
                      how='left')
    
    # Classify connections
    final_df['edge_color'] = final_df['connection_type'].map({
        'mutual': 'blue',
        None: 'orange'
    }).fillna('orange')
    
    return final_df.drop(columns=['connection_type'])
