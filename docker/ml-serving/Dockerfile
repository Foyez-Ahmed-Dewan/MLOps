FROM python:3.12-slim 

WORKDIR /app 

# Copy requirements.txt first for better caching
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt 

# copy application files
COPY main.py .
COPY model.pkl .

# Expose port
EXPOSE 5000

# run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]