from transformers import pipeline

def classify(text):
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", multi_label=True)
    #classifier = pipeline('fill-mask', model='Ammar-alhaj-ali/arabic-MARBERT-news-article-classification')
    candidate_labels = ['Celebrity', 'Sport', 'Education', 'Policy', 'Health', 'Military', 'Zoo', 'Science', 'Activism', 'Business']
    return classifier(text, candidate_labels)

