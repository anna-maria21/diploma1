from transformers import pipeline
from sklearn.svm import LinearSVC
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np
import joblib
from pathlib import Path

candidate_labels = ['Policy', 'Entertainment', 'Sport', 'Tech', 'Health', 'Military', 'Ecology', 'Science', 'Nature', 'Economics']

data = [
    "Politics is the set of activities that are associated with making decisions in groups, or other forms of power relations among individuals, such as the distribution of resources or status. Politics is exercised on a wide range of social levels, from clans and tribes of traditional societies, through modern local governments, companies and institutions up to sovereign states, to the international level.",
    "Cultural Entertainment – the act of embracing the tradition of a country or group’s rich history and making it accessible and engaging to the masses. Cultural news includes news about movies, theater productions, or any other mass event intended to entertain an audience.",
    "Sport pertains to any form of physical activity or game, often competitive and organized, that aims to use, maintain, or improve physical ability and skills while providing enjoyment to participants and, in some cases, entertainment to spectators. Sports can, through casual or organized participation, improve participants' physical health. For example, football, basketball, tennis, boxing, various types of wrestling, cricket, chess, martial arts, handball, hockey, Formula 1 racing, swimming, etc.",
    "Technology is the application of knowledge for achieving practical goals in a reproducible way.[1] The word technology can also mean the products resulting from such efforts, including both tangible tools such as utensils or machines, and intangible ones such as software. Technology plays a critical role in science, engineering, and everyday life. Technologies are used in the field of programming, artificial intelligence, medical and scientific developments.",
    "Health, according to the World Health Organization, is \"a state of complete physical, mental and social well-being and not merely the absence of disease and infirmity\". A variety of definitions have been used for different purposes over time. Health can be promoted by encouraging healthful activities, such as regular physical exercise and adequate sleep, and by reducing or avoiding unhealthful activities or situations, such as smoking or excessive stress.",
    "A military, also known collectively as armed forces, is a heavily armed, highly organized force primarily intended for warfare. It is typically authorized and maintained by a sovereign state, with its members identifiable by their distinct military uniform. It may consist of one or more military branches such as an army, navy, air force, space force, marines, or coast guard. The main task of the military is usually defined as defence of the state and its interests against external armed threats.",
    "Ecology is the study of the relationships between living organisms, including humans, and their physical environment; it seeks to understand the vital connections between plants and animals and the world around them. Ecology also provides information about the benefits of ecosystems and how we can use Earth’s resources in ways that leave the environment healthy for future generations. Efforts are being made to protect the environment.",
    "Science is a systematic endeavor that builds and organizes knowledge in the form of testable explanations and predictions about the universe. Scientific breakthrough in cancer research.",
    "Nature, in the broadest sense, is the physical world or universe. Nature can refer to the phenomena of the physical world, and also to life in general. Exploring the beauty of nature through photography. It is oceans, seas, lakes, rivers, mountains, islands, trees, bushes, forests, meadows, animals, birds, fish and any living organisms. Also it is a seasons - summer, autumn, winter and spring, climat.",
    "Economic indicators show signs of growth. Macroeconomics studies how the economy behaves as a whole, including inflation, price levels, rate of growth, national income, gross domestic product and changes in employment rates. Microeconomics studies the implications of individual human action, and is key to a person's financial health."
]


def classifyBart(text):
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", multi_label=True)
    return classifier(text, candidate_labels)


def classifyZeroShot(text):
    model = SentenceTransformer('all-MiniLM-L6-v2')

    test_sentence = text

    label_encoder = LabelEncoder()
    encoded_labels = label_encoder.fit_transform(candidate_labels)

    encoded_data = model.encode(data)

    classifier = LinearSVC()
    classifier.fit(encoded_data, encoded_labels)

    encoded_test_sentence = model.encode([test_sentence])

    cosine_similarities = cosine_similarity(encoded_test_sentence, encoded_data)
    scores = cosine_similarities[0]

    sorted_indices = np.argsort(scores)[::-1]
    sorted_labels = np.array(candidate_labels)[sorted_indices].tolist()
    sorted_scores = scores[sorted_indices].tolist()

    min_score = min(sorted_scores) * 2
    right_sorted_scores = []
    for i in range(len(sorted_scores)):
        right_sorted_scores.append(sorted_scores[i] - min_score)
    return { 'labels': sorted_labels, 'scores': right_sorted_scores }


def classifyRandomForest(text):
    HERE = Path(__file__).parent
    vectorizer = joblib.load(HERE / 'vectorizer.pkl')
    clf = joblib.load(HERE / 'model.pkl')
    vectorizedText = vectorizer.transform([text])
    predictedClass = clf.predict(vectorizedText)
    return predictedClass[0]