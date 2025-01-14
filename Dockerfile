FROM python:3.8.12-slim

# Install jupyter, nbconvert, and other dependencies from requirements.txt
RUN pip install jupyter nbconvert

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt for dependencies
COPY requirements.txt .

# Install dependencies using pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Jupyter notebooks from the 'notebooks' folder to the container
COPY notebooks/ ./notebooks/

COPY employee_churn_data.csv .

COPY run_notebooks.py .

# Execute the Jupyter notebooks using nbconvert (to ensure preprocessing or data preparation is complete)
RUN python run_notebooks.py

# Copy the training script to the container
COPY train.py .

# Execute the training script to generate the model file
RUN python train.py

# Copy the application files (Flask app and tests) to the container
COPY ["predict.py", "predict-test.py", "./"]

# Expose the application port
EXPOSE 9696

# Set the entry point to start Flask with Gunicorn
ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:9696", "predict:app"]
