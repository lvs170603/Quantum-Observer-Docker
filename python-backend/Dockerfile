# Use mambaforge to avoid building Aer on Windows hosts; installs from conda-forge
FROM mambaorg/mambaforge:latest

WORKDIR /app

# Copy files
COPY . /app

# Create environment and install dependencies from conda-forge
RUN mamba install -y -c conda-forge python=3.11 qiskit flask flask-cors python-dotenv && \
    mamba clean -afy

# Expose port
EXPOSE 5000

ENV PORT=5000
ENV PYTHONUNBUFFERED=1

CMD ["python", "app.py"]