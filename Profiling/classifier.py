def classify(score):
    profile = max(score, key=score.get)
    return profile
