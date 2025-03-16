from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
import numpy as np

# Load Datasey
vocab_size = 10000
max_len = 200
(X_train, y_train), (X_test, y_test) = imdb.load_data(num_words=vocab_size)

# Decode reviews to text for preprocessing
word_index = imdb.get_word_index()
reverse_word_index = {value: key for key, value in word_index.items()}
decoded_reviews = [" ".join([reverse_word_index.get(i - 3, "?") for i in review]) for review in X_train[:5]]

# Pad sequences
X_train = pad_sequences(X_train, maxlen=max_len, padding="post")
X_test = pad_sequences(X_test, maxlen=max_len, padding="post")

print(f"Training data shape: {X_train.shape}, {y_train.shape}")
print(f"Test data shape: {X_test.shape}, {y_test.shape}")

# Load GloVe embeddings
embedding_index = {}
glove_file = "glove.6B.100d.txt"
with open(glove_file, "r", encoding='utf-8') as file:
    for line in file:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype="float32")
        embedding_index[word] = coefs

print(f"Loaded {len(embedding_index)} word vectors")

# Prepare embedding matrix
embedding_dim = 100
embedding_matrix = np.zeros((vocab_size, embedding_dim))
for word, i in word_index.items():
    if i < vocab_size:
        embedding_vector = embedding_index.get(word)
        if embedding_vector is not None:
            embedding_matrix[i] = embedding_vector

# Define LSTM model with GloVe embeddings
model = Sequential([
    Embedding(input_dim=vocab_size, output_dim=embedding_dim, weights=[embedding_matrix], trainable=False),
    LSTM(128, activation='tanh', return_sequences=False),
    Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.summary()

# Train the model
history = model.fit(
    X_train, y_train, validation_split=0.2, epochs=5, batch_size=64, verbose=1
)

loss, accuracy = model.evaluate(X_test, y_test, verbose=0)


lstm_model = Sequential([
    Embedding(input_dim=vocab_size, output_dim=128),
    LSTM(128, activation='tanh', return_sequences=False),
    Dense(1, activation='sigmoid')
])

lstm_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
lstm_model.summary()

lstm_history = lstm_model.fit(
    X_train, y_train, epochs=5, batch_size=64, validation_split=0.2)

lstm_loss, lstm_accuracy = lstm_model.evaluate(X_test, y_test)
print(f"LSTM without GloVe Test Accuracy: {lstm_accuracy:.4f}")
print(f"LSTM model with GloVe Test Accuracy: {accuracy:.4f}")

import matplotlib.pyplot as plt

# Plot accuracy comparison
models = ['LSTM', 'LSTM GloVe']
accuracies = [lstm_accuracy, accuracy]
plt.bar(models, accuracies, color=['blue', 'green'])
plt.title('Comparison of LSTM with and without word embeddings')
plt.ylabel('Accuracy')
plt.show()
