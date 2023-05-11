from transformers import pipeline
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

def classify(text):
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", multi_label=True)
    candidate_labels = ['Policy', 'Culture', 'Sport', 'Tech', 'Health', 'Military', 'Ecology', 'Science', 'Nature', 'Economics']
    return classifier(text, candidate_labels)

def classify1(text):
    model_name = 'bert-base-uncased'  # Example model, you can choose a different one
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)


    # Tokenize the text
    encoded_input = tokenizer(text, padding=True, truncation=True, return_tensors='pt')

    # Perform classification
    with torch.no_grad():
        outputs = model(**encoded_input)

    # Get the predicted label
    predicted_label = torch.argmax(outputs.logits, dim=1).item()

    # Print the predicted label
    print(f"Predicted Label: {predicted_label}")

