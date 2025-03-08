import os
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Model
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.optimizers import Adam

def get_train_generator():
    return train_datagen.flow_from_directory(
    os.path.join(dataset_path, 'train'),
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical'
)

# Definir paths
dataset_path = './dataset'

# Aumento de datos
train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    brightness_range=[0.8, 1.2],
    fill_mode='nearest'
)

if __name__ == "__main__":



    val_datagen = ImageDataGenerator(rescale=1. / 255)

    # Generadores de imágenes
    train_generator = get_train_generator()

    val_generator = val_datagen.flow_from_directory(
        os.path.join(dataset_path, 'validation'),
        target_size=(224, 224),
        batch_size=32,
        class_mode='categorical'
    )

    # Calcular pesos de clases si el dataset está desbalanceado
    class_counts = Counter(train_generator.classes)
    max_count = max(class_counts.values())
    class_weight = {i: max_count / count for i, count in class_counts.items()}

    # Cargar modelo preentrenado (MobileNetV2)
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    base_model.trainable = False  # Congelamos capas base

    # Definir la nueva arquitectura
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(512, activation='relu')(x)
    x = Dropout(0.5)(x)  # Evita sobreajuste
    output_layer = Dense(len(train_generator.class_indices), activation='softmax')(x)

    model = Model(inputs=base_model.input, outputs=output_layer)

    # Compilar modelo
    model.compile(optimizer=Adam(learning_rate=0.001), loss='categorical_crossentropy', metrics=['accuracy'])

    # Mostrar resumen del modelo
    model.summary()

    # EarlyStopping para detener entrenamiento si no mejora y ReduceLROnPlateau para ajustar el learning rate
    early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=1e-6)

    # Entrenar modelo
    history = model.fit(
        train_generator,
        epochs=100,
        validation_data=val_generator,
        callbacks=[early_stop, reduce_lr],
        class_weight=class_weight  # Usar si hay desbalance de clases
    )

    # Evaluar modelo
    val_loss, val_accuracy = model.evaluate(val_generator)
    print(f"Validation Loss: {val_loss}")
    print(f"Validation Accuracy: {val_accuracy}")

    # Guardar el modelo
    model.save('dino_classifier_model.h5')

    # Función para predecir dinosaurios con preprocesamiento corregido
    def predict_dinosaur(img_path, model, class_indices):
        img = load_img(img_path, target_size=(224, 224))  # Ajustar tamaño
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0  # Normalización correcta

        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions)

        # Obtener etiquetas correctas
        class_labels = list(class_indices.keys())
        return class_labels[predicted_class]

    # Probar predicción con imagen del dataset para verificar correcto funcionamiento
    img_path = './image_to_validate/trex.png'  # Asegúrate de cambiar esto por una imagen válida
    predicted_label = predict_dinosaur(img_path, model, train_generator.class_indices)
    print(f"Predicted Dinosaur: {predicted_label}")

    # Graficar Accuracy y Loss
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Train Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.title('Model Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()

    plt.show()
