import os

# Get router URL from environment variable, with a default value
router_url = os.getenv('ROUTER_URL', 'http://llm-backend:8080')
