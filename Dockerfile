FROM python:3.12.5

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY identicons.py .

# Use this to develop inside the container
# CMD ["sleep", "infinity"]

ENTRYPOINT ["python", "identicons.py"]

