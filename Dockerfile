FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot code
COPY gold_signal_bot.py .

# Run bot
CMD ["python", "-u", "gold_signal_bot.py"]
