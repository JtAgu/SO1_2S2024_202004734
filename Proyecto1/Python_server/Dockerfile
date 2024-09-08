# 
FROM python:3.9-slim

# 
WORKDIR /code

# 
COPY  . /code

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
EXPOSE 8080

CMD ["fastapi", "run", "main.py", "--port", "8080"]