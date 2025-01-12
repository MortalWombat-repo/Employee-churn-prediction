FROM python:3.8.12-slim

# Install pipenv, jupyter, and nbconvert for managing dependencies and running notebooks
RUN pip install pipenv jupyter nbconvert

# Set the working directory in the container
WORKDIR /app

# Copy Pipfile and Pipfile.lock for dependencies
COPY ["Pipfile", "Pipfile.lock", "./"]

# Install dependencies using pipenv
RUN pipenv install --system --deploy

# Copy the Jupyter notebooks from the 'notebooks' folder to the container
COPY ["notebooks/*.ipynb", "./notebooks/"]

# Execute the Jupyter notebooks using nbconvert (this will run them as part of the build process)
RUN jupyter nbconvert --to notebook --execute --inplace notebooks/*.ipynb

# Copy the application files (Flask app and model) to the container
COPY ["predict.py", "predict-test.py", "model_C=1.0.bin", "./"]

# Expose the application port
EXPOSE 9696

# Set the entry point to start Flask with Gunicorn using predict.py
ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:9696", "predict:app"]