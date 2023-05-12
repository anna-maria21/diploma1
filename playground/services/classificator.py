from transformers import pipeline

def classify(text):
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", multi_label=True)
    candidate_labels = ['Policy', 'Culture', 'Sport', 'Tech', 'Health', 'Military', 'Ecology', 'Science', 'Nature', 'Economics']
    return classifier(text, candidate_labels)

