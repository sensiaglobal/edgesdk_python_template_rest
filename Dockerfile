# Build Stage 1 (Builder)
FROM python:3.13-bullseye as builder

WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir --compile --target=/install -r requirements.txt

# Optimised Stage 2 (Final Image - Optimised & distroless)
FROM nvcr.io/nvidia/distroless/python:3.13-v3.0.8

# Create /app using python
RUN ["python", "-c", "import os; os.makedirs('/app', exist_ok=True)"]
WORKDIR /app

# Copy installed dependencies from the builder stage
COPY --from=builder /install /usr/local/lib/python3.13/site-packages/

COPY . .

# Explicitly use UID 0 (root)
USER 0
RUN ["python", "-c", "import os; os.makedirs('/temp', exist_ok=True)"]

CMD [ "python", "-u", "./run.py" ]

LABEL org.opencontainers.image.vendor="Sensia Global" \
      org.opencontainers.image.url="https://www.sensiaglobal.com/" \
      org.opencontainers.image.license="Propietary" \
      com.sensiaglobal.image.artifacts.source="sensia-edge-docker-dev"