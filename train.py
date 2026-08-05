import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load Dataset
df = pd.read_csv("dataset.csv")

# Features and Labels
X = df["text"]
y = df["label"]

# Convert Text to Numerical Features
vectorizer = TfidfVectorizer(stop_words="english")
X_vectorized = vectorizer.fit_transform(X)

# Split Data
X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized,
    y,
    test_size=0.2,
    random_state=42
)

# Train Model
model = LogisticRegression()
model.fit(X_train, y_train)

# Save Model
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("done! both file saved with data")