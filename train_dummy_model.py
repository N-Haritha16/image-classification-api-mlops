import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
import os

model = models.Sequential([
    layers.Input(shape=(64, 64, 3)),
    layers.Conv2D(8, (3, 3), activation="relu"),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(10, activation="softmax"),
])

model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

x_dummy = np.random.rand(32, 64, 64, 3).astype("float32")
y_dummy = np.random.randint(0, 10, size=(32,))

model.fit(x_dummy, y_dummy, epochs=1, batch_size=8)

os.makedirs("models", exist_ok=True)
model.save("models/my_classifier_model.h5")
print("Saved model to models/my_classifier_model.h5")
