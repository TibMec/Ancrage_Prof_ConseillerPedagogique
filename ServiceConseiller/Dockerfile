FROM python:3.12

LABEL authors="Tibmec"

WORKDIR /app


COPY requirements.txt .


RUN pip install -r requirements.txt


COPY . .


EXPOSE 5900


CMD ["python", "service_cp.py"]