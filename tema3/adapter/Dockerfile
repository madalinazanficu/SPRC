FROM python:3.8


# Set the working directory inside the container
WORKDIR /adapter

# Copy the requirments file and install deps
COPY adapter/requirements.txt .
RUN pip install -r requirements.txt

# Copy the source code of the adapter into the container
COPY adapter/adapter.py .

# Define the command to run the adapter
CMD ["python3", "adapter.py"]