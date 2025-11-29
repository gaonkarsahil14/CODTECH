import requests
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------------
# 1. Fetch Data from Public API
# ------------------------------------
url = "https://jsonplaceholder.typicode.com/posts"
response = requests.get(url)

data = response.json()

# Convert to DataFrame
df = pd.DataFrame(data)

print("Data Loaded Successfully!")
print(df.head())

# ------------------------------------
# 2. Visualization 1: Bar chart of post lengths
# ------------------------------------
df["body_length"] = df["body"].apply(len)

plt.figure(figsize=(10,5))
plt.bar(df["id"], df["body_length"])
plt.title("Post Body Length for Each Post")
plt.xlabel("Post ID")
plt.ylabel("Length of Body Text")
plt.show()

# ------------------------------------
# 3. Visualization 2: Histogram of text length
# ------------------------------------
plt.figure(figsize=(10,5))
plt.hist(df["body_length"], bins=10)
plt.title("Distribution of Post Body Length")
plt.xlabel("Length")
plt.ylabel("Frequency")
plt.show()

# ------------------------------------
# 4. Visualization Dashboard
# ------------------------------------
plt.figure(figsize=(14,6))

# Subplot 1
plt.subplot(1,2,1)
plt.bar(df["id"], df["body_length"])
plt.title("Body Length per Post")

# Subplot 2
plt.subplot(1,2,2)
plt.hist(df["body_length"], bins=10)
plt.title("Length Distribution")

plt.tight_layout()
plt.show()
