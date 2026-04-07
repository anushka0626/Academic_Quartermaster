FROM python:3.11-slim

# 1. Set the working directory to /app (the root of your project)
WORKDIR /app

# 2. Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy your package folder and the DB into the container
COPY academics_agent/ ./academics_agent/
# Note: This keeps the DB inside the academics_agent folder where it belongs
COPY academics_agent/quartermaster.db ./academics_agent/

# 4. Set PYTHONPATH so Python can find the 'academics_agent' package
ENV PYTHONPATH=/app

# 5. Run uvicorn from the /app level, NOT from inside the subfolder
CMD ["uvicorn", "academics_agent.api_main:app", "--host", "0.0.0.0", "--port", "8080"]