import re
import string
from collections import Counter
import emoji
import matplotlib.pyplot as plt
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Download VADER lexicon
nltk.download('vader_lexicon')

# Custom Slang Dictionary
slang_dict = {
    "gud": "good",
    "luv": "love",
    "awsm": "awesome",
    "thx": "thanks",
    "omg": "oh my god",
    "u": "you",
    "ur": "your",
    "gr8": "great",
    "wtf": "what the fuck"
}

# Reduce elongated words
def reduce_elongated(word):
    return re.sub(r'(.)\1{2,}', r'\1\1', word)

# Clean & Normalize Tweet
def clean_and_normalize(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)  # Removes URLs
    text = re.sub(r'@\w+', "", text)  # Removes mentions
    text = re.sub(r'#', "", text)  # Removes hashtag symbol
    text = text.translate(str.maketrans('', '', string.punctuation))  # Removes punctuation

    words = text.split()
    normalized_words = []

    for word in words:
        word = reduce_elongated(word)
        word = slang_dict.get(word, word)
        normalized_words.append(word)

    return normalized_words


# Load Emotion Lexicon File
# Format: word:emotion
def load_emotion_file(file_path):
    emotions = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(':')
            if len(parts) >= 2:
                emotions[parts[0].strip()] = parts[1].strip()
    return emotions

# Load emotion dictionaries
word_emotions = load_emotion_file('emotion_nd_sentiment.txt')
emoji_emotions = load_emotion_file('emojis_sentiment.txt')


# Analyze Tweet
def analyze_tweet(tweet):
    cleaned_words = clean_and_normalize(tweet)

    # Text-based emotions
    text_emotions = [word_emotions[word] for word in cleaned_words if word in word_emotions]

    # Emoji-based emotions
    tweet_emojis = [char for char in tweet if char in emoji.EMOJI_DATA]
    emoji_emotions_detected = [emoji_emotions[e] for e in tweet_emojis if e in emoji_emotions]

    all_emotions = text_emotions + emoji_emotions_detected

    # Sentiment analysis using VADER
    sia = SentimentIntensityAnalyzer()
    sentiment_scores = sia.polarity_scores(tweet)

    # Phrase-level sentiment
    positive_phrases = [
        "crushed my goals",
        "killed it",
        "nailed it",
        "so happy",
        "feeling great"
    ]

    if any(phrase in tweet.lower() for phrase in positive_phrases):
        sentiment_scores['compound'] += 0.3
        sentiment_scores['pos'] += 0.1

    return all_emotions, sentiment_scores, text_emotions, emoji_emotions_detected


# Visualize Emotions
def visualize_emotions(emotions):
    if not emotions:
        print("No emotions detected.")
        return

    counts = Counter(emotions)
    plt.figure(figsize=(8, 4))
    plt.bar(counts.keys(), counts.values(), color='skyblue')
    plt.title("Detected Emotions")
    plt.xlabel("Emotion")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# Main Program
if __name__ == "__main__":
    tweet = input("Enter a tweet-like sentence: ")

    emotions, sentiment, matched_words, matched_emojis = analyze_tweet(tweet)

    print("\nMatched Emotion Words:", matched_words)
    print("Matched Emojis:", matched_emojis)

    print("\nDetected Emotions:", emotions)
    print("Sentiment Scores:", sentiment)

    visualize_emotions(emotions)
