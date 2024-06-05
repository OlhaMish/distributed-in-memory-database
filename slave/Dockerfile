# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the maintainer label
LABEL authors="oleksandr"

# Set the working directory in the container
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy the pyproject.toml and poetry.lock files to the container
COPY pyproject.toml poetry.lock ./

# Install the dependencies
RUN poetry install --no-root

# Copy the rest of the application code to the container
COPY . .

# Expose the port the app runs on
EXPOSE 5001

# Define the command to run the application
CMD ["poetry", "run", "python", "slave/edge_node.py"]
