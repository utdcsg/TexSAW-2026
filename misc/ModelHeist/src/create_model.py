import tensorflow as tf
from tensorflow import keras
import numpy as np
import os

# Flag to hide
FLAG = "texsaw{w3ight5_t3ll_t4l3s}"

def encode_flag_in_weights(flag):
    # Convert flag to ASCII values, then normalize to weight range
    ascii_vals = [ord(c) for c in flag]
    # Scale to reasonable weight values
    weights = np.array(ascii_vals, dtype=np.float32) / 1000.0
    return weights

def create_model_with_hidden_flag(flag):
    # Create a simple model that actually works (for MNIST-like classification)
    model = keras.Sequential([
        keras.layers.Input(shape=(28, 28)),
        keras.layers.Flatten(),
        keras.layers.Dense(128, activation='relu'),
        # This layer will contain the flag
        keras.layers.Dense(len(flag), activation='linear', name='secret_layer'),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(10, activation='softmax')
    ])
    
    # Compile the model
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    
    # Generate dummy training data
    x_train = np.random.rand(1000, 28, 28)
    y_train = np.random.randint(0, 10, 1000)
    
    # Train briefly to make it look legitimate
    model.fit(x_train, y_train, epochs=3, batch_size=32, verbose=0)
    
    # Inject the flag into the secret layer
    flag_weights = encode_flag_in_weights(flag)
    
    # Get current weights
    secret_layer = model.get_layer('secret_layer')
    current_weights = secret_layer.get_weights()
    
    # Modify the first row of the weight matrix to contain the flag
    current_weights[0][0, :] = flag_weights
    
    # Set the modified weights back
    secret_layer.set_weights(current_weights)
    
    return model

def main():
    model = create_model_with_hidden_flag(FLAG)

    model.save('model.h5')
    print(f"Model saved with hidden flag: {FLAG}")
    
    
if __name__ == "__main__":
    main()

