import tensorflow as tf
import numpy as np

model = tf.keras.models.load_model(
    "keras_model.h5",
    compile=False
)

with open("labels.txt", "r", encoding="utf-8") as f:
    class_names = [
        linea.strip().split(" ", 1)[1]
        for linea in f.readlines()
    ]


def machine(ruta_imagen):

    imagen = tf.io.read_file(ruta_imagen)

    imagen = tf.image.decode_image(
        imagen,
        channels=3,
        expand_animations=False
    )

    imagen = tf.cast(imagen, tf.float32)

    imagen = tf.image.resize(imagen, [224, 224])

    imagen = (imagen / 127.5) - 1

    imagen = tf.expand_dims(imagen, axis=0)

    predicciones = model.predict(imagen, verbose=0)

    indice = np.argmax(predicciones[0])

    confianza = float(predicciones[0][indice])

    clase = class_names[indice]

    return clase, confianza