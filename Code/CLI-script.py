import os
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Set TF_CPP_MIN_LOG_LEVEL to suppress TensorFlow info and warning messages
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def load_and_preprocess_model(model_path, tokenizer_path):
    # Load the trained LSTM model
    model = load_model(model_path)

    # Load the tokenizer used during training
    with open(tokenizer_path, 'rb') as f:
        tokenizer = pd.read_pickle(f)

    return model, tokenizer

def process_file(file_path, model, tokenizer):
    # Read the file content
    with open(file_path, 'r') as file:
        file_content = file.read()

    # Tokenize and pad the text sequence
    sequence = tokenizer.texts_to_sequences([file_content])
    padded_sequence = pad_sequences(sequence, maxlen=model.input_shape[1])

    # Make predictions using the loaded model
    prediction = model.predict(padded_sequence)

    # Display the result
    probability_score = prediction[0][0]
    print(f"Probability Score: {probability_score}")
    result = "Malicious" if prediction[0][0] > 0.5 else "Benign"
    print(f"Result: {result}")

if __name__ == "__main__":

    print("Anomaly Detection Program")
    # Paths to the trained model and tokenizer
    model_path = "F:/FinalProject/new-model/model.h5"
    tokenizer_path = "F:/FinalProject/new-model/tokenizer.pkl"

    # Load the trained model and tokenizer
    lstm_model, text_tokenizer = load_and_preprocess_model(model_path, tokenizer_path)

    # Get the file path from the user
    file_path = input("Enter the path to the file for detection: ")

    # Check if the file exists
    if os.path.exists(file_path):
        # Process the file using the LSTM model
        process_file(file_path, lstm_model, text_tokenizer)
    else:
        print("File not found. Please enter a valid file path.")
