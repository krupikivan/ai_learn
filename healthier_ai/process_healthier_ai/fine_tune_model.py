import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_datasets as tfds
import efficientnet.tfkeras as efn

# Define some constants
BATCH_SIZE = 32
IMG_SIZE = 224

def format_image(image, label):
    image = tf.image.resize(image, (IMG_SIZE, IMG_SIZE)) / 255.0
    return image, label

(dataset_train, dataset_val), info = tfds.load('food101', split=['train', 'validation'], with_info=True, as_supervised=True)

# Prepare the datasets
train_batches = dataset_train.shuffle(1000).map(format_image).batch(BATCH_SIZE).prefetch(1)
validation_batches = dataset_val.map(format_image).batch(BATCH_SIZE).prefetch(1)


# Load the base model
base_model = efn.EfficientNetB0(input_shape=(IMG_SIZE, IMG_SIZE, 3), include_top=False, weights='imagenet')
base_model.trainable = False

# Add a classification head
model = tf.keras.Sequential([
    base_model,
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(info.features['label'].num_classes, activation='softmax')
])

# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(train_batches, epochs=5, validation_data=validation_batches)


# Unfreeze the base model and train again with a low learning rate
base_model.trainable = True
model.compile(optimizer=tf.keras.optimizers.Adam(1e-5), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(train_batches, epochs=5, validation_data=validation_batches)

model.save('food101_efficientnet_model.h5')