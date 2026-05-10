FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY agent.py train.py mini_dataset.csv ./

RUN python train.py

CMD ["python", "agent.py"]