from db_manager import DatabaseManager
from visualization_plotly import PlotlyGraphVisualizer

def main():
    # Initialize database connection
    db_manager = DatabaseManager()
    
    # Build visualization
    visualizer = PlotlyGraphVisualizer(db_manager)
    visualizer.build_graph_data()
    visualizer.create_visualization()
    
    # Cleanup
    db_manager.close()
    
    
main()