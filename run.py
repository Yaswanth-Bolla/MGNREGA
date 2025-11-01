#!/usr/bin/env python3
"""
MGNREGA Dashboard - Flask Application
A web application for visualizing MGNREGA performance data for Karnataka districts.
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    print("Starting MGNREGA Dashboard...")
    print("Access the application at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
