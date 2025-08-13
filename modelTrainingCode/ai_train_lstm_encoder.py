import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, RepeatVector, TimeDistributed, Dense, Embedding
import matplotlib.pyplot as plt

# --- Step 1: Load the Dataset ---
# Paths are now relative to the project's root directory.
print("➡️ Loading dataset...")
try:
    event_traces = pd.read_csv('/content/drive/MyDrive/Dataset-ThreatSlayers/Event_traces.csv', header=None, low_memory=False)
    labels = pd.read_csv('/content/drive/MyDrive/Dataset-ThreatSlayers/anomaly_label.csv', header=None)
    print("✅ Dataset loaded successfully.")
    print(f"Shape of event_traces: {event_traces.shape}")
    print(f"Shape of labels: {labels.shape}")
except FileNotFoundError:
    print("❌ Error: Dataset files not found. Make sure the 'dataset' directory is in your project root.")
    exit()

# --- Step 2: Clean and preprocess data ---
print("\n➡️ Cleaning and preprocessing data...")

# 2.1: Fill missing values and convert to strings
event_traces = event_traces.fillna('MISSING').astype(str)

# 2.2: Label encode each column individually
event_traces_encoded = event_traces.apply(lambda col: LabelEncoder().fit_transform(col))

# --- FIX: Shift all encoded values by 1 to reserve 0 for padding ---
# This prevents real events from being masked and resolves the cuDNN error.
print("➡️ Shifting vocabulary by +1 to reserve 0 for padding...")
event_traces_encoded += 1

# 2.3: Convert encoded dataframe to list of sequences and pad
sequences = event_traces_encoded.values.tolist()
# `pad_sequences` uses 0 for padding by default, which is now safe to mask.
padded_sequences = pad_sequences(sequences, padding='post')
X_full = np.array(padded_sequences)

# 2.4: Clean labels - convert to string and strip spaces
labels_str = labels.iloc[:, 1].astype(str).str.strip()

# Remove header row if present
if labels_str.iloc[0] == 'Label' or labels_str.iloc[0] not in ['Normal', 'Anomaly', '0', '1']:
    labels_str = labels_str[1:].reset_index(drop=True)
    X_full = X_full[1:]

# 2.5: Map string labels to numeric values
label_map = {'Normal': 0, 'Anomaly': 1, '0': 0, '1': 1}
labels_mapped = labels_str.map(label_map)

# 2.6: Filter valid labels and align X and y
valid_mask = labels_mapped.notna()
X = X_full[valid_mask.values]
y = labels_mapped[valid_mask].astype('float32').values

print("✅ Data cleaned and ready!")
print(f"X shape: {X.shape}")
print(f"y shape: {y.shape}")

# --- Step 3: Build the LSTM autoencoder Model ---
print("\n➡️ Building the LSTM autoencoder model...")

# Define model parameters
timesteps = X.shape[1]
# The input dimension must account for the largest integer value after the shift.
input_dim = int(X.max()) + 1
print(f"Model input_dim set to: {input_dim}")


inputs = Input(shape=(timesteps,))
# `mask_zero=True` will now correctly only mask the post-padding.
x = Embedding(input_dim=input_dim, output_dim=64, mask_zero=True)(inputs)

# Encoder: No changes needed here, the fast cuDNN kernel will be used automatically.
encoded = LSTM(32)(x)

# Decoder
decoded = RepeatVector(timesteps)(encoded)
decoded = LSTM(64, return_sequences=True)(decoded)
decoded = TimeDistributed(Dense(1))(decoded)

autoencoder = Model(inputs, decoded)
autoencoder.compile(optimizer='adam', loss='mse')
autoencoder.summary()

# --- Step 4: Train the LSTM Autoencoder ---
print("\n➡️ Starting model training...")

history = autoencoder.fit(
    X,
    X[..., None], # Targets are the input sequences themselves
    epochs=20,
    batch_size=64,
    validation_split=0.2,
    verbose=1
)

# --- Step 5: Save the Model in the Modern .keras Format ---
# The model is saved to the project root directory.
autoencoder.save("lstm_autoencoder.keras")
print("\n✅ Model saved as lstm_autoencoder.keras in the project root directory.")

# --- Step 6: Plot and Save the Training Loss Curve ---
print("\n➡️ Generating training loss plot...")
plt.figure(figsize=(10, 6))
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss Over Epochs')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)
plt.savefig("training_loss_curve.png")
print("✅ Loss curve saved as training_loss_curve.png")
