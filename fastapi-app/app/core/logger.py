import logging

# Create a custom logger
logger = logging.getLogger("fastapi_llm_app")
logger.setLevel(logging.INFO) # Set the default logging level

# Create handlers (e.g., console handler)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create formatters and add it to handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(console_handler)

# Example usage (can be removed or modified later)
# logger.info("Logger initialized successfully.")