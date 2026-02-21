import tensorflow as tf
from tensorflow.keras import layers, models

input_shape = (64, 64, 3)
num_classes = 10

model = models.Sequential([
    layers.Input(shape=input_shape),
    layers.Conv2D(16, (3, 3), activation="relu"),
    layers.MaxPooling2D(),
    layers.Conv2D(32, (3, 3), activation="relu"),
    layers.MaxPooling2D(),
    layers.Flatten(),
    layers.Dense(64, activation="relu"),
    layers.Dense(num_classes, activation="softmax"),
])

model.compile(optimizer="adam",
              loss="sparse_categorical_crossentropy",
              metrics=["accuracy"])

model.save("models/my_classifier_model.h5", include_optimizer=False)
print("Saved model to models/my_classifier_model.h5")
