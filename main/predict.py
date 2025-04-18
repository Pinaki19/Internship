import torch
import numpy as np
from joblib import load
from transformers import AutoTokenizer, AutoModel

# Load ClinicalBERT
tokenizer = AutoTokenizer.from_pretrained("medicalai/ClinicalBERT")
model = AutoModel.from_pretrained("medicalai/ClinicalBERT")
model.eval()

# Load saved model components
rf_model = load(r'.\models\best_random_forest_model.joblib')
pca = load(r'.\models\pca_transformer.joblib')
le = load(r'.\models\label_encoder.joblib')

# Embed a new note
def embed_note(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=128)
    with torch.no_grad():
        outputs = model(**inputs)
        return outputs.last_hidden_state[:, 0, :].squeeze().numpy()

# Example usage
def predict_label(text):
    embedding = embed_note(text).reshape(1, -1)
    pca_features = pca.transform(embedding)
    predicted_class = rf_model.predict(pca_features)
    predicted_label = le.inverse_transform(predicted_class)
    return predicted_label[0]



'''
import numpy as np
from joblib import load

# Load model components
rf_model = load(r'.\models\best_random_forest_model.joblib')
pca = load(r'.\models\pca_transformer.joblib')
le = load(r'.\models\label_encoder.joblib')

# Load saved ClinicalBERT embeddings
embeddings = load(r'.\models\clinical_bert_embeddings.joblib')

# Predict label from precomputed embedding
def predict_label_from_embedding(embedding):
    embedding = embedding.reshape(1, -1)
    pca_features = pca.transform(embedding)
    predicted_class = rf_model.predict(pca_features)
    predicted_label = le.inverse_transform(predicted_class)
    return predicted_label[0]

# Example usage
# Assuming index 0 corresponds to the new note's embedding
example_embedding = embeddings[0]
predicted = predict_label_from_embedding(example_embedding)
print("Predicted label:", predicted)

'''