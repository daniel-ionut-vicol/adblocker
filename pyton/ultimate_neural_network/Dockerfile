# Use an official TensorFlow GPU image as the base image
FROM tensorflow/tensorflow:latest-gpu

# Set the working directory in the container
WORKDIR /app

# Install any additional dependencies your project requires
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN python3 -m pip install --upgrade pip
COPY requirements.txt /home
RUN pip install -r /home/requirements.txt

# Expose any necessary ports if your project runs a service
EXPOSE 8080

# Command to run your TensorFlow project (modify this as needed)
CMD ["python", "clip_gpt-training.py"]
