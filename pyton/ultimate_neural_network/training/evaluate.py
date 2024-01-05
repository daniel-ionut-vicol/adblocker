import os
import pickle
import pandas as pd

# Define the same file path where you saved the data
input_file = f'{os.environ["DATA"]}/cnn_training/models/{current_model_folder_name}/test_data.pkl'

# Open the file in read mode
with open(input_file, 'rb') as file:
    # Load the data from the file
    test_steps, start_datetime, finish_datetime = pickle.load(file)

# Define the same file path where you saved the history
hist_csv_file = f'{os.environ["DATA"]}/cnn_training/models/{current_model_folder_name}/history.csv'

# Read the CSV file into a pandas DataFrame
history_df = pd.read_csv(hist_csv_file)
