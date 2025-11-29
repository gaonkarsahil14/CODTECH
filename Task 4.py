# 🧠 SPAM EMAIL DETECTION MODEL USING SCIKIT-LEARN
# Author: Sahil Gaonkar
# Project: Machine Learning Model Implementation (Predictive Model)

# Step 1: Import Libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import seaborn as sns
import matplotlib.pyplot as plt

# Step 2: Load Dataset
# Using a sample dataset available online (SMS Spam Collection)
url = "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv"
df = pd.read_csv(url, sep='\t', header=None, names=['label', 'message'])

# Display first few rows
print("📊 Dataset Preview:")
print(df.head())

# Step 3: Data Preprocessing
# Convert labels: 'ham' -> 0, 'spam' -> 1
df['label_num'] = df['label'].map({'ham': 0, 'spam': 1})

# Step 4: Split Data into Training and Testing
X_train, X_test, y_train, y_test = train_test_split(
    df['message'], df['label_num'], test_size=0.2, random_state=42
)

# Step 5: Text Vectorization (Convert text to numbers)
vectorizer = CountVectorizer(stop_words='english')
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Step 6: Model Training (Naive Bayes Classifier)
model = MultinomialNB()
model.fit(X_train_vec, y_train)

# Step 7: Make Predictions
y_pred = model.predict(X_test_vec)

# Step 8: Evaluate Model Performance
accuracy = accuracy_score(y_test, y_pred)
print("\n✅ Model Accuracy:", round(accuracy * 100, 2), "%")

print("\n📈 Classification Report:")
print(classification_report(y_test, y_pred, target_names=['Ham', 'Spam']))

# Step 9: Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Ham', 'Spam'], yticklabels=['Ham', 'Spam'])
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix - Spam Detection')
plt.show()

# Step 10: Test with Custom Messages
test_messages = [
    "Congratulations! You won a free lottery ticket worth $1000!",
    "Hey Kajal, are we meeting for class today?",
    "Claim your free vacation by clicking this link!"
]

test_vec = vectorizer.transform(test_messages)
predictions = model.predict(test_vec)

for msg, pred in zip(test_messages, predictions):
    label = "SPAM" if pred == 1 else "HAM"
    print(f"📩 Message: {msg}\n➡ Prediction: {label}\n")
