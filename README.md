# Code Search

A code search engine that actually analyzes and follows the code.

# Run

    # Install neo4j and necessary utilities
    make install_tools
    # Process sample data
    make analyse
    # Serve the backend
    make serve-back &
    # Serve the frontend
    make serve-front &
