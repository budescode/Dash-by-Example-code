FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8050
# For the Chapter 8 FastAPI app use uvicorn instead of gunicorn:
# CMD ["uvicorn", "app:app.server",
#      "--host", "0.0.0.0", "--port", "8050"]
CMD ["gunicorn", "app:server", "--bind", "0.0.0.0:8050", "--workers", "2"]
 
 
