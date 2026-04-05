# Model Heist - Writeup

"Neural networks are like onions - or was that ogres?" - Onions (and ogres) have layers, so this leads us to think the flag is somewhere in the layers of the network.

So first, we need to load the model and examine its architecture:

```python
import tensorflow as tf
from tensorflow import keras

model = keras.models.load_model('model.h5')
model.summary()
```

This reveals a neural network with several layers:
- Input layer (28x28)
- Flatten layer
- Dense layer (128 units)
- **secret_layer** (suspicious name!) - Dense layer with variable units
- Dense layer (64 units)
- Output layer (10 units)

The layer named `secret_layer` is a clear hint. Let's extract its weights:

```python
secret_layer = model.get_layer('secret_layer')
weights = secret_layer.get_weights()[0]
```

Neural network weights are typically small floating-point numbers. If we examine the first row of the weight matrix, we'll notice the values are suspiciously regular and seem to be scaled ASCII values.

```python
flag_weights = weights[0, :]
print(flag_weights)
```

The weights appear to be ASCII values divided by 1000. We can reverse this encoding:

```python
import numpy as np

# Multiply by 1000 and round to get ASCII values
ascii_values = np.round(flag_weights * 1000).astype(int)

# Convert to characters
flag = ''.join([chr(val) for val in ascii_values])
print(f"FLAG: {flag}")
```

### Complete Solution Script

```python
import tensorflow as tf
from tensorflow import keras
import numpy as np

def extract_flag_from_model(model_path):
    """Extract the hidden flag from the model weights"""
    
    print("[*] Loading model...")
    model = keras.models.load_model(model_path)
    
    print("[*] Looking for secret_layer...")
    secret_layer = model.get_layer('secret_layer')
    
    print("[*] Extracting weights...")
    weights = secret_layer.get_weights()[0]
    
    # The flag is in the first row of the weight matrix
    flag_weights = weights[0, :]
    
    print("[*] Decoding (multiply by 1000 and convert to ASCII)...")
    ascii_values = np.round(flag_weights * 1000).astype(int)
    
    # Convert to characters
    flag = ''.join([chr(val) for val in ascii_values])
    
    return flag

if __name__ == "__main__":
    flag = extract_flag_from_model('model.h5')
    print(f"\n[+] FLAG: {flag}")
```

## Flag
```
texsaw{w3ight5_t3ll_t4l3s}
```
