# Use an official TensorFlow GPU image as the base image
FROM tensorflow/tensorflow:latest-gpu

# Set the working directory in the container
WORKDIR /app

# Copy your project files into the container
COPY . /app

# Set environment variables
ENV IMAGE_SIZE=256
ENV BATCH_SIZE=32
ENV LOG_DIR=logs
ENV DATASET_PATH=/app/dataset
ENV EPOCHS=10
ENV VERBOSE_LEVEL=1

# Install any additional dependencies your project requires
# For example, if you have a requirements.txt file:
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose any necessary ports if your project runs a service
# For example, if your application listens on port 8080:
EXPOSE 8080

# Command to run your TensorFlow project (modify this as needed)
CMD ["python", "ultimate_train.py"]
