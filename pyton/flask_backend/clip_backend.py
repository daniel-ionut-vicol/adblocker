from flask import Flask, request, jsonify
import torch
from transformers import CLIPProcessor, CLIPModel, CLIPImageProcessor
from PIL import Image, UnidentifiedImageError
import io

app = Flask(__name__)

# Load a pre-trained CLIP model and processor
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
feature_extractor = CLIPImageProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Move to GPU if available
if torch.cuda.is_available():
    model = model.to('cuda')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    try:
        # Load and resize the image
        image = Image.open(io.BytesIO(file.read()))
        resized_image = image.resize((224, 224))  # Resize the image to 224x224

        # Preprocess the image
        image_input = feature_extractor(images=resized_image, return_tensors="pt")

        # Define text labels
        texts = [ "An image depicting a typical advertisement. It is characterized by vibrant colors and high-contrast lighting to catch the viewer's eye. The composition includes a clear brand logo and a product or service being prominently displayed. There's persuasive text, such as a catchy slogan or a special offer, aimed at encouraging consumer action. Elements like human models, exaggerated emotions, or idealized scenarios are common, emphasizing the product's benefits. The layout is professional, with a focus on aesthetic appeal and strategic placement of text and visuals to guide the viewer's attention.", "An image representing a non-commercial, everyday scene. It is marked by a more natural and subdued color palette, with lighting that reflects real-world conditions rather than dramatic or staged enhancements. The content is devoid of brand logos, promotional text, or sales pitches. Instead, it might feature landscapes, unposed people, animals, or common objects in their natural state, without any artificial staging. The composition is candid and unstructured, capturing a slice of life or a natural scene without the intention of selling or promoting any product or service."] # Preprocess the text
        text_input = processor(texts, return_tensors="pt", padding=True, truncation=True)

        # Move tensors to GPU if available
        if torch.cuda.is_available():
            image_input = {k: v.to('cuda') for k, v in image_input.items()}
            text_input = {k: v.to('cuda') for k, v in text_input.items()}

        # Get the model's prediction
        with torch.no_grad():
            image_features = model.get_image_features(**image_input)
            text_features = model.get_text_features(**text_input)

            # Normalize the features
            image_features = torch.nn.functional.normalize(image_features, dim=-1)
            text_features = torch.nn.functional.normalize(text_features, dim=-1)

            # Calculate the cosine similarity between image and text features
            similarities = torch.nn.functional.cosine_similarity(image_features, text_features).tolist()

        # Return the similarity scores as a list
        return jsonify(similarities)

    except UnidentifiedImageError:
        return jsonify({'error': 'Invalid image format'}), 400
    except Exception as e:
        # Log the exception details here if needed
        return jsonify({'error': 'An error occurred processing the request'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

