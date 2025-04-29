import os

# Define the path to the disease data directory
DISEASE_DATA_DIR = "./diseases_data/"

def load_disease_details(disease_name):
    """Load disease details from a text file."""
    file_path = os.path.join(DISEASE_DATA_DIR, f"{disease_name.lower().replace(' ', '_')}.txt")
    if not os.path.exists(file_path):
        return "Details not available for this disease."
    with open(file_path, "r") as file:
        return file.read()

def predict_disease_with_details(image_file):
    # Preprocess the image
    image = Image.open(image_file).resize((224, 224))  # Adjust dimensions as per your model
    image_array = np.array(image) / 255.0  # Normalize if required
    image_array = np.expand_dims(image_array, axis=0)

    # Predict using the model
    predictions = model.predict(image_array)
    disease_class = np.argmax(predictions, axis=1)[0]

    # Map prediction to disease name
    disease_map = {
        0: "Maize ear rot",
        1: "maize grasshoper",
        2: "maize fall-army worm",
        3: "Maize leaf beetle",
        4: "Healthy maize",
        5: "maize leather necrosis",
        6: "Maize leaf blight",
        7: "Maize leaf spot",
        8: "Maize streak virus",
        9: "Nutrient Defficiency in Maize",
        10: "Maize rust",
        11: "Maize smut",
    }
    disease_name = disease_map.get(disease_class, "Unknown")

    # Load disease details
    disease_details = load_disease_details(disease_name)

    return {"disease": disease_name, "details": disease_details}
