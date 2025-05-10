import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
import os

# Definir la ruta base para los datos
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

def get_data_generators():
    train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest',
        validation_split=0.2
    )

    train_generator = train_datagen.flow_from_directory(
        os.path.join(DATA_DIR, 'dataset'),
        target_size=(224, 224),
        batch_size=32,
        class_mode='categorical',
        subset='training'
    )

    validation_generator = train_datagen.flow_from_directory(
        os.path.join(DATA_DIR, 'dataset'),
        target_size=(224, 224),
        batch_size=32,
        class_mode='categorical',
        subset='validation'
    )

    return train_generator, validation_generator

def create_model(num_classes):
    base_model = MobileNetV2(weights='imagenet', include_top=False)
    
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(1024, activation='relu')(x)
    predictions = Dense(num_classes, activation='softmax')(x)
    
    model = Model(inputs=base_model.input, outputs=predictions)
    
    for layer in base_model.layers:
        layer.trainable = False
        
    return model

def train_model():
    train_generator, validation_generator = get_data_generators()
    
    model = create_model(len(train_generator.class_indices))
    
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Crear directorio para modelos si no existe
    models_dir = os.path.join(DATA_DIR, 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    history = model.fit(
        train_generator,
        steps_per_epoch=train_generator.samples // train_generator.batch_size,
        epochs=10,
        validation_data=validation_generator,
        validation_steps=validation_generator.samples // validation_generator.batch_size
    )
    
    model.save(os.path.join(models_dir, 'model.h5'))
    return history

def get_train_generator():
    """
    Returns only the training data generator.
    This is useful when we only need the training generator, for example to access class_indices.
    """
    train_generator, _ = get_data_generators()
    return train_generator

if __name__ == '__main__':
    train_model() 