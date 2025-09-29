# Import necessary libraries
import string                         # For punctuation removal
from collections import Counter      # To count frequency of emotions
import matplotlib.pyplot as plt      # For plotting a bar chart

# Step 1: Read the input text file
text = open('read.txt', encoding='utf-8').read()

# Step 2: Convert all text to lowercase to maintain consistency
lower_case = text.lower()

# Step 3: Remove punctuation from the text using str.translate()
cleaned_text = lower_case.translate(str.maketrans('', '', string.punctuation))

# Step 4: Tokenize the cleaned text by splitting on whitespace
tokenized_words = cleaned_text.split()

# Print tokenized words
print("Tokenized Words:", tokenized_words)

# Step 5: Define a list of stop words (common words to ignore in analysis)
stop_words = [
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself",
    "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself",
    "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these",
    "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do",
    "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while",
    "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before",
    "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again",
    "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each",
    "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than",
    "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"
]

# Step 6: Filter out stop words from tokenized words
final_words = []
for word in tokenized_words:
    if word not in stop_words:
        final_words.append(word)

# Print final meaningful words (after stop words removed)
print("Final Words:", final_words)

# Step 7: Emotion Detection
# Load emotion mappings from 'emotions.txt'
# Format of each line in 'emotions.txt' should be: word:emotion

emotion_list = []
with open('emotions.txt', 'r') as file:
    for line in file:
        # Clean each line (remove newline, comma, apostrophes, and extra spaces)
        clear_line = line.replace("\n", '').replace(',', '').replace("'", '').strip()
        # Split into word and corresponding emotion
        word, emotion = clear_line.split(':')
        # If the word is present in final_words, append the emotion
        if word in final_words:
            emotion_list.append(emotion)

# Step 8: Print detected emotions
print("Detected Emotions:", emotion_list)

# Step 9: Count each emotion's frequency using Counter
emotion_count = Counter(emotion_list)
print("Emotion Count:", emotion_count)

# Step 10: Plot the emotions using a bar chart
fig, ax1 = plt.subplots()
ax1.bar(emotion_count.keys(), emotion_count.values())
# Rotate x-axis labels for better readability
fig.autofmt_xdate()
# Display the plot
plt.show()
