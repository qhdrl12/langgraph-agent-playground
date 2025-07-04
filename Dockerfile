FROM python:3.12-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependency files
COPY pyproject.toml .
COPY README.md .

# Install dependencies
RUN uv sync --no-dev

# Copy source code
COPY src/ ./src/
COPY main.py .

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "run_streamlit.py"]