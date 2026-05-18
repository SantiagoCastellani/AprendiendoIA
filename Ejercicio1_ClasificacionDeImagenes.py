# =========================================================
# Proyecto de Inteligencia Artificial con Python y Colab
# Clasificación de imágenes utilizando TensorFlow y Keras
# Dataset: CIFAR-10
# =========================================================

import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt

# Dataset de ejemplo
dataset = tf.keras.datasets.cifar10

# Cargar datos
(train_images, train_labels), (test_images, test_labels) = dataset.load_data()

# Normalizar imágenes
train_images = train_images / 255.0
test_images = test_images / 255.0

# Clases del dataset
class_names = [
    'avion', 'auto', 'pajaro', 'gato',
    'ciervo', 'perro', 'rana', 'caballo',
    'barco', 'camion'
]

# Mostrar una imagen
plt.imshow(train_images[0])
plt.title(class_names[train_labels[0][0]])
plt.show()

# Crear modelo
model = models.Sequential([
    layers.Conv2D(32, (3,3), activation='relu', input_shape=(32,32,3)),
    layers.MaxPooling2D((2,2)),

    layers.Conv2D(64, (3,3), activation='relu'),
    layers.MaxPooling2D((2,2)),

    layers.Flatten(),

    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax')
])

# Compilar modelo
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Entrenar
history = model.fit(
    train_images,
    train_labels,
    epochs=5,
    validation_data=(test_images, test_labels)
)

# Evaluar
test_loss, test_acc = model.evaluate(test_images, test_labels)

print("Precisión:", test_acc)

from google.colab import files
from tensorflow.keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt

# Subir imagen
uploaded = files.upload()

# Obtener nombre del archivo
img_path = list(uploaded.keys())[0]

# Cargar imagen y redimensionarla
img = image.load_img(img_path, target_size=(32, 32))

# Mostrar imagen
plt.imshow(img)
plt.show()

# Convertir imagen a array
img_array = image.img_to_array(img)

# Normalizar
img_array = img_array / 255.0

# Agregar dimensión batch
img_array = np.expand_dims(img_array, axis=0)

# Predecir
prediction = model.predict(img_array)

# Obtener clase predicha
predicted_class = np.argmax(prediction)

# Mostrar resultado
print("Clase predicha:", class_names[predicted_class])
