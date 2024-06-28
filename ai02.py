from tensorflow.keras.datasets import mnist
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt

import numpy as np

(train_images, train_labels), _ = mnist.load_data()

# pick a sample to plot
sample = 99
image = train_images[sample]

# plot the sample
#fig = plt.figure
#plt.imshow(image, cmap='gray')
#plt.show()


print(train_labels[sample])

train_images = train_images.reshape((60000,28*28))
train_images = train_images.astype("float32") / 255

print("valódi érték:")
print(train_images[sample].shape)

def get_model():
    model = keras.Sequential([
        layers.Dense(512, activation="relu"),
        layers.Dense(10, activation="softmax")
    ])

    model.compile(optimizer="rmsprop", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

    return model

model = get_model()

print("predikció (tanítás előtt): ")
print(np.argmax(model.predict(np.array([train_images[sample]]))))

cost_hist = model.fit(train_images, train_labels, epochs=10, batch_size=128, validation_split=0.2)

print("predikció (tanítás után): ")
print(np.argmax(model.predict(np.array([train_images[sample]]))))


from PIL import Image
imagepath = 'testkep2.png'
image = Image.open(imagepath)

image = image.convert('L')
image_arr = np.array(image)
image_arr = image_arr / 255.0
image_ar = image_arr.reshape(28*28)

print("Saját kép predikció: ")
print(np.argmax(model.predict(np.array([image_ar]))))

imagepath = 'testkep.png'
image = Image.open(imagepath)

image = image.convert('L')
image_arr = np.array(image)
image_arr = image_arr / 255.0
image_ar = image_arr.reshape(28*28)

print("Saját kép predikció: ")
print(np.argmax(model.predict(np.array([image_ar]))))

def get_cnn_model():
    model = keras.Sequential([
        layers.Conv2D(filters=32, kernel_size=3, activation="relu"),
        layers.MaxPooling2D(pool_size=2),
        layers.Conv2D(filters=64, kernel_size=3, activation="relu"),
        layers.MaxPooling2D(pool_size=2),
        layers.Conv2D(filters=128, kernel_size=3, activation="relu"),
        layers.MaxPooling2D(pool_size=2),
        layers.Flatten(),
        layers.Dense(512, activation="relu"),
        layers.Dense(10, activation="softmax")
    ])

    model.compile(optimizer="rmsprop", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

    return model

(train_images, train_labels), _ = mnist.load_data()
train_images = train_images.reshape((60000,28,28,1))
train_images = train_images.astype("float32") / 255

model_cnn = get_cnn_model()

cost_hist = model_cnn.fit(train_images, train_labels, epochs=5, batch_size=128, validation_split=0.2)

imagepath = 'testkep2.png'
image = Image.open(imagepath)

image = image.convert('L')
image_arr = np.array(image)
image_arr = image_arr / 255.0
image_ar = image_arr.reshape(28,28,1)

print("Saját kép CNN predikció: ")
print(np.argmax(model_cnn.predict(np.array([image_ar]))))

imagepath = 'testkep.png'
image = Image.open(imagepath)

image = image.convert('L')
image_arr = np.array(image)
image_arr = image_arr / 255.0
image_ar = image_arr.reshape(28,28,1)

print("Saját kép CNN predikció2: ")
print(np.argmax(model_cnn.predict(np.array([image_ar]))))