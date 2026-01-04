# ---- build stage ----
FROM python:3.10-slim AS build
WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential gcc gfortran \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# discard build stage for faster pulling

# ---- runtime stage ----
FROM python:3.10-slim
WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY --from=build /wheels /wheels

RUN pip install --no-cache-dir \
    --no-index \
    --find-links=/wheels \
    -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]