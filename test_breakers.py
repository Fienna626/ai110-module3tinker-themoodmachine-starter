from mood_analyzer import MoodAnalyzer

a = MoodAnalyzer()

breakers = [
    "I love getting stuck in traffic",
    "This party is sick",
    "I'm fine 🙂",
    "I'm exhausted but proud of myself"
]

for b in breakers:
    pred = a.predict_label(b)
    exp = a.explain(b)
    print(f'"{b}" -> {pred} ({exp})')