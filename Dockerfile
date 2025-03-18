# Use an official Python 3.10 image
FROM python:3.10-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy all project files into the container
COPY . /app

# Set Python Path for correct imports
ENV PYTHONPATH=/app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the FastAPI app port
EXPOSE 8000

# Run FastAPI with Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
