from flask import Flask, request, jsonify
import torch
from transformers import CLIPProcessor, CLIPModel, CLIPImageProcessor
from PIL import Image
import io

app = Flask(__name__)

# Load a pre-trained CLIP model and processor
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch16")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch16")
feature_extractor = CLIPImageProcessor.from_pretrained("openai/clip-vit-base-patch16")

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file:
        image = Image.open(io.BytesIO(file.read()))

        # Preprocess the image
        image_input = feature_extractor(images=image, return_tensors="pt")

        text = ["Advertisement"]  # This should be dynamic based on your use case

        # Preprocess the text
        text_input = processor(text, return_tensors="pt")

        # Move to GPU if available
        if torch.cuda.is_available():
            model = model.to('cuda')
            image_input = {k: v.to('cuda') for k, v in image_input.items()}
            text_input = {k: v.to('cuda') for k, v in text_input.items()}

        # Get the model's prediction
        with torch.no_grad():
            image_outputs = model.get_image_features(**image_input)
            text_outputs = model.get_text_features(**text_input)

        # Normalize the features
        image_features = torch.nn.functional.normalize(image_outputs, dim=-1)
        text_features = torch.nn.functional.normalize(text_outputs, dim=-1)

        # Calculate the cosine similarity between image and text features
        cosine_similarity = torch.nn.functional.cosine_similarity(image_features, text_features).item()

        # Define a threshold for classification (adjust as needed)
        threshold = 0.5

        # Make a decision based on the threshold
        result = cosine_similarity > threshold
        return jsonify({'is_ad': result, 'similarity': cosine_similarity})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
