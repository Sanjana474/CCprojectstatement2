FROM python:3.9

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


COPY . /app

# Set the healthcheck command
HEALTHCHECK --interval=120s --timeout=5s CMD python healthcheck.py 
 
CMD ["python", "healthcheck.py"]
