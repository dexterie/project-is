# -*- coding: utf-8 -*-
"""notebook49cb69b258 (1).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1P65vjzJKl9BakC4jmN8-Sp8rMOi7zJtG
"""

import numpy as np
import os
import random
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array, ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Flatten, Dropout, GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

from google.colab import files
files.upload()

!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json

!kaggle datasets download -d shaunthesheep/microsoft-catsvsdogs-dataset -p /content/ --unzip

# Function to load a limited number of images
def load_images(folder, label, img_size=(224, 224), max_images=1040):
    images, labels = [], []
    filenames = [f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    random.shuffle(filenames)
    filenames = filenames[:max_images]

    for filename in filenames:
        img_path = os.path.join(folder, filename)
        try:
            img = load_img(img_path, target_size=img_size)
            img = img_to_array(img)
            img = preprocess_input(img)
            images.append(img)
            labels.append(1 if label == "Dog" else 0)  # Convert to binary labels
        except Exception as e:
            print(f"Skipping corrupted image: {img_path}")
            continue
    return images, labels

# Load a limited dataset
dataset_path = "/content/PetImages"
dog_path = f"{dataset_path}/Dog"
cat_path = f"{dataset_path}/Cat"

dog_images, dog_labels = load_images(dog_path, label="Dog", max_images=520)
cat_images, cat_labels = load_images(cat_path, label="Cat", max_images=520)

data = np.array(dog_images + cat_images)
labels = np.array(dog_labels + cat_labels)

import matplotlib.pyplot as plt
import random
from tensorflow.keras.preprocessing.image import load_img

# ฟังก์ชันแสดงภาพตัวอย่างจากโฟลเดอร์
def show_sample_images(folder, num_samples=5):
    filenames = [f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    sample_files = random.sample(filenames, num_samples)  # เลือกไฟล์แบบสุ่ม

    plt.figure(figsize=(10, 5))
    for i, file in enumerate(sample_files):
        img_path = os.path.join(folder, file)
        img = load_img(img_path, target_size=(224, 224))  # โหลดภาพ
        plt.subplot(1, num_samples, i+1)
        plt.imshow(img)
        plt.axis("off")
        plt.title(file)
    plt.show()

print("ตัวอย่างภาพหมา:")
show_sample_images(dog_path)

print("ตัวอย่างภาพแมว:")
show_sample_images(cat_path)

from PIL import Image

def check_image_sizes(folder, num_samples=10):
    filenames = [f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    sample_files = random.sample(filenames, num_samples)

    for file in sample_files:
        img_path = os.path.join(folder, file)
        try:
            with Image.open(img_path) as img:
                print(f"{file}: {img.size}")
        except Exception as e:
            print(f"ไฟล์เสีย: {file}")

print("ขนาดภาพของหมา:")
check_image_sizes(dog_path)

print("ขนาดภาพของแมว:")
check_image_sizes(cat_path)

# Encode labels
lb = LabelBinarizer()
labels = lb.fit_transform(labels)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)

# Data Augmentation
data_generator = ImageDataGenerator(
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

# Load MobileNetV2 pre-trained model
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Unfreeze last few layers for fine-tuning
for layer in base_model.layers[-30:]:
    layer.trainable = True

# Build model
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation='relu')(x)
x = Dropout(0.5)(x)
out = Dense(1, activation='sigmoid')(x)

model = Model(inputs=base_model.input, outputs=out)

model.compile(optimizer=Adam(learning_rate=0.00001), loss='binary_crossentropy', metrics=['accuracy'])

# Train model with data augmentation
history = model.fit(
    data_generator.flow(X_train, y_train, batch_size=32),
    validation_data=(X_test, y_test),
    epochs=10
)

# Evaluate model
loss, acc = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {acc:.4f}")

import matplotlib.pyplot as plt

# Plot Training & Validation Accuracy and Loss
plt.figure(figsize=(12, 5))
plt.gcf().patch.set_facecolor("black")

# Accuracy Graph
plt.subplot(1, 2, 1)
plt.plot(history.history.get('accuracy', []), marker='o', label="Training Accuracy")
plt.plot(history.history.get('val_accuracy', []), marker='o', label="Validation Accuracy")
plt.title("Training and Validation Accuracy", fontsize=14, color="white")
plt.xlabel("Epochs", fontsize=12, color="white")
plt.ylabel("Accuracy", fontsize=12, color="white")
plt.legend()
plt.grid(alpha=0.3)
plt.xticks(color="white")
plt.yticks(color="white")

# Loss Graph
plt.subplot(1, 2, 2)
plt.plot(history.history.get('loss', []), marker='o', label="Training Loss")
plt.plot(history.history.get('val_loss', []), marker='o', label="Validation Loss")
plt.title("Training and Validation Loss", fontsize=14, color="white")
plt.xlabel("Epochs", fontsize=12, color="white")
plt.ylabel("Loss", fontsize=12, color="white")
plt.legend()
plt.grid(alpha=0.3)
plt.xticks(color="white")
plt.yticks(color="white")

plt.show()

model.save("mobilenetv2_cat_dog.h5")

pip install tensorflow==2.15

import tensorflow as tf
print(tf.__version__)  # ตรวจสอบว่าใช้เวอร์ชันไหน