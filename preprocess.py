import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
import pickle
from sklearn.metrics import accuracy_score

# Load dataset
df = pd.read_csv("disease_dataset.csv")
df.dropna(inplace=True)

# Features and labels
X_raw = df['symptoms']
y = df['disease']

# TF-IDF vectorization
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(X_raw)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model training
model = MultinomialNB()
model.fit(X_train, y_train)

# Save model and vectorizer
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

# Fix: handle duplicate disease entries
disease_info = df.groupby('disease')[['medicine', 'diet']].first().to_dict('index')

# Save medicine and diet info
with open("disease_info.pkl", "wb") as f:
    pickle.dump(disease_info, f)
y_pred = model.predict(X_test)
print("✅ Model, vectorizer, and disease info saved successfully!")
print("Accuracy Score: ", accuracy_score(y_pred,y_test))