from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from neo4j import GraphDatabase
from models import Base, User, Relationship

# Configuration
POSTGRES_URI = "postgresql://postgres:Mm%40%4082651@localhost/socialdb"
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "mm82651mm82651"

def migrate_postgres_to_neo4j():
    # Connect to PostgreSQL using ORM session
    pg_engine = create_engine(POSTGRES_URI)
    Session = sessionmaker(bind=pg_engine)
    pg_session = Session()

    # Connect to Neo4j
    neo4j_driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    try:
        # Get all users with ORM
        users = pg_session.query(User).all()
        
        # Convert SQLAlchemy objects to dictionaries
        user_dicts = [{
            "user_id": u.user_id,
            "username": u.username,
            "full_name": u.full_name
        } for u in users]

        # Create Neo4j nodes
        with neo4j_driver.session() as neo4j_session:
            neo4j_session.run("""
            UNWIND $users AS user
            MERGE (u:User {user_id: user.user_id})
            SET u += user
            """, users=user_dicts)

            # Get all relationships
            relationships = pg_session.query(Relationship).all()
            rel_dicts = [{
                "follower_id": r.follower_id,
                "followed_id": r.followed_id
            } for r in relationships]

            # Create Neo4j relationships
            neo4j_session.run("""
            UNWIND $rels AS rel
            MATCH (follower:User {user_id: rel.follower_id})
            MATCH (followed:User {user_id: rel.followed_id})
            MERGE (follower)-[:FOLLOWS]->(followed)
            """, rels=rel_dicts)

        print("Migration completed successfully!")

    finally:
        pg_session.close()
        neo4j_driver.close()

if __name__ == "__main__":
    migrate_postgres_to_neo4j()