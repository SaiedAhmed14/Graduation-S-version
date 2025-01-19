import pickle
import numpy as np
import cv2
import os

current_directory = os.getcwd()
model_path = os.path.join(current_directory, "face_recognition2/src/assets", "face_recognition_model.pkl")
label_map_path = os.path.join(current_directory, "face_recognition2/src/assets", "label_map.pkl")

class FacialRecognitionModel:
    def __init__(self, model_path=model_path, label_map_path=label_map_path):
        """Initialize the FacialRecognitionModel class.
        
        Args:
            model_path (str): Path to the trained model file.
            label_map_path (str): Path to the label map file.
        """
        self.model_path = model_path
        self.label_map_path = label_map_path
        self.model = None
        self.label_map = None
        self.reverse_label_map = None

        self._load_model_and_labels()

    def _load_model_and_labels(self):
        """Private method to load the trained model and label map."""
        try:
            with open(self.model_path, "rb") as model_file:
                self.model = pickle.load(model_file)
            
            with open(self.label_map_path, "rb") as label_map_file:
                self.label_map = pickle.load(label_map_file)

            # Create a reverse label map for easy decoding
            self.reverse_label_map = {v: k for k, v in self.label_map.items()}
        
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Error loading files: {e}")

    def preprocess_image(self, image):
        """Preprocess the image for model prediction.
        
        Args:
            image (numpy.ndarray): The input image.
        
        Returns:
            numpy.ndarray: Preprocessed image ready for prediction.
        """
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        resized_image = cv2.resize(gray_image, (100, 100))  # Resize to match training data
        return resized_image.flatten().reshape(1, -1)

    def predict(self, image):
        """Predict the class, name, and confidence for a given image.
        
        Args:
            image (numpy.ndarray): The input image.
        
        Returns:
            dict: Prediction result containing class, name, and confidence.
        """
        preprocessed_image = self.preprocess_image(image)
        probabilities = self.model.predict_proba(preprocessed_image)[0]
        predicted_label = np.argmax(probabilities)
        confidence = probabilities[predicted_label]
        label_name = self.reverse_label_map[predicted_label]

        # Split label_name into class and name
        person_class, person_name = label_name.split('/')

        return {
            "class": person_class,
            "name": person_name,
            "confidence": confidence
        }