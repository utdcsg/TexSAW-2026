import tensorflow as tf
from tensorflow import keras
import numpy as np

def extract_flag_from_model(model_path):
    """Extract the hidden flag from the model weights"""
    
    print("[*] Loading model...")
    model = keras.models.load_model(model_path)
    
    print("[*] Model architecture:")
    model.summary()
    
    print("\n[*] Looking for secret_layer...")
    secret_layer = model.get_layer('secret_layer')
    
    print("[*] Extracting weights...")
    weights = secret_layer.get_weights()[0]
    
    # The flag is in the first row of the weight matrix
    print("[*] Analyzing first weight pathway...")
    flag_weights = weights[0, :]
    
    print("[*] Decoding (multiply by 1000 and convert to ASCII)...")
    # Multiply by 1000 and round to get ASCII values
    ascii_values = np.round(flag_weights * 1000).astype(int)
    
    # Convert to characters
    flag = ''.join([chr(val) for val in ascii_values])
    
    return flag

def main():
    print("="*50)
    print("Model Heist - Solution Script")
    print("="*50)
    
    model_path = 'dist/model.h5'
    
    try:
        flag = extract_flag_from_model(model_path)
        print(f"\n[+] FLAG FOUND: {flag}")
        print("="*50)
        
        # Verify it's the correct format
        if flag.startswith('texsaw{') and flag.endswith('}'):
            print("[+] Flag format verified! ✓")
        else:
            print("[!] Warning: Flag format may be incorrect")
            
    except Exception as e:
        print(f"[-] Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
