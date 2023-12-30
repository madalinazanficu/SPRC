FROM python:3.8

# Copy the requirments file and install deps
COPY requirements.txt .
RUN pip install -r requirements.txt

# Expose the port on which the adapter will listen
EXPOSE 1883

# Copy the source code of the adapter into the container
COPY adapter.py .

# Define the command to run the adapter
CMD ["python3", "adapter.py"]