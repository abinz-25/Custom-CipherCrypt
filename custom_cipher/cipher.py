import numpy as np
import math

class CustomCipher:
    def __init__(self, key):
        if len(key) < 10:
            raise ValueError("Key must be at least 10 characters long.")
        
        self.original_key = key
        
        # The first 9 characters form the Hill key
        self.hill_key_str = key[:9]
        # The rest of the key forms the Vigenere key
        self.vigenere_key = key[9:]

        # Try to create a valid Hill key matrix, adjust if necessary
        self.hill_key_matrix, self.adjusted_hill_key = self._create_valid_hill_key_matrix(self.hill_key_str)
    
    def get_full_key(self):
        """Returns the full key being used (Vigenere + Hill parts)"""
        return self.adjusted_hill_key + self.vigenere_key
    
    def _create_valid_hill_key_matrix(self, key_str):
        """Try to create a valid Hill matrix, adjusting the key if necessary"""
        original_key_str = key_str
        key_str = key_str.upper().replace("J", "I")
        key_num = [ord(c) - ord('A') for c in key_str]
        
        if len(key_num) != 9:
            raise ValueError("Internal error: Hill cipher requires exactly 9 characters. Please ensure your key is at least 10 characters long.")
        
        # Try the original key first
        matrix = np.array(key_num).reshape(3, 3)
        det = int(round(np.linalg.det(matrix))) % 26
        
        if det != 0 and math.gcd(det, 26) == 1:
            # Key is already valid, no adjustment needed (no message printed)
            return matrix, key_str
        
        # Strategy 1: Try adjusting all elements uniformly
        for adjustment in range(1, 26):
            adjusted_key_num = [(num + adjustment) % 26 for num in key_num]
            matrix = np.array(adjusted_key_num).reshape(3, 3)
            det = int(round(np.linalg.det(matrix))) % 26
            
            if det != 0 and math.gcd(det, 26) == 1:
                adjusted_key_str = ''.join([chr(num + ord('A')) for num in adjusted_key_num])
                print(f"Note: Key was automatically adjusted to create a valid Hill cipher matrix")
                print(f"Original Hill key: {key_str}")
                print(f"Adjusted Hill key: {adjusted_key_str} (uniform adjustment: +{adjustment})")
                return matrix, adjusted_key_str
        
        # Strategy 2: Try adjusting only specific positions
        for i in range(9):
            for adjustment in range(1, 26):
                adjusted_key_num = key_num.copy()
                adjusted_key_num[i] = (adjusted_key_num[i] + adjustment) % 26
                matrix = np.array(adjusted_key_num).reshape(3, 3)
                det = int(round(np.linalg.det(matrix))) % 26
                
                if det != 0 and math.gcd(det, 26) == 1:
                    adjusted_key_str = ''.join([chr(num + ord('A')) for num in adjusted_key_num])
                    print(f"Note: Key was automatically adjusted to create a valid Hill cipher matrix")
                    print(f"Original Hill key: {key_str}")
                    print(f"Adjusted Hill key: {adjusted_key_str} (position {i} adjusted by +{adjustment})")
                    return matrix, adjusted_key_str
        
        # Strategy 3: Use a known good matrix and mix it with the key
        # GYBNQKURP is known to work, use it as fallback
        fallback = "GYBNQKURP"
        fallback_num = [ord(c) - ord('A') for c in fallback]
        
        # Mix original key with fallback
        mixed_key_num = [(key_num[i] + fallback_num[i]) % 26 for i in range(9)]
        matrix = np.array(mixed_key_num).reshape(3, 3)
        det = int(round(np.linalg.det(matrix))) % 26
        
        if det != 0 and math.gcd(det, 26) == 1:
            mixed_key_str = ''.join([chr(num + ord('A')) for num in mixed_key_num])
            print(f"Note: Key was combined with a base matrix to create a valid Hill cipher matrix")
            print(f"Original Hill key: {key_str}")
            print(f"Final Hill key: {mixed_key_str}")
            return matrix, mixed_key_str
        
        # If all else fails, use the fallback matrix but inform the user
        matrix = np.array(fallback_num).reshape(3, 3)
        print(f"Warning: Could not create a valid matrix from your key. Using a default secure matrix instead.")
        print(f"Original Hill key: {key_str}")
        print(f"Final Hill key: {fallback}")
        return matrix, fallback

    def _vigenere_encrypt(self, text):
        text = text.upper().replace("J", "I")
        encrypted = ""
        key_len = len(self.vigenere_key)
        key_index = 0
        for char in text:
            if 'A' <= char <= 'Z':
                shift = ord(self.vigenere_key[key_index % key_len].upper()) - ord('A')
                encrypted_char = chr(((ord(char) - ord('A') + shift) % 26) + ord('A'))
                encrypted += encrypted_char
                key_index += 1
        return encrypted

    def _vigenere_decrypt(self, text):
        text = text.upper()
        decrypted = ""
        key_len = len(self.vigenere_key)
        key_index = 0
        for char in text:
            if 'A' <= char <= 'Z':
                shift = ord(self.vigenere_key[key_index % key_len].upper()) - ord('A')
                decrypted_char = chr(((ord(char) - ord('A') - shift + 26) % 26) + ord('A'))
                decrypted += decrypted_char
                key_index += 1
        return decrypted

    def _hill_encrypt(self, text, original_length=None):
        text = text.upper()
        # Do NOT replace J with I here - preprocessing already done in Vigenere stage
        text_num = [ord(c) - ord('A') for c in text if 'A' <= c <= 'Z']
        
        # Pad the text if necessary
        while len(text_num) % 3 != 0:
            text_num.append(ord('X') - ord('A'))  # Pad with 'X'

        encrypted = ""
        for i in range(0, len(text_num), 3):
            vector = np.array(text_num[i:i+3])
            encrypted_vector = np.dot(self.hill_key_matrix, vector) % 26
            for num in encrypted_vector:
                encrypted += chr(num + ord('A'))
        
        return encrypted

    def _hill_decrypt(self, text, original_length=None):
        text = text.upper()
        text_num = [ord(c) - ord('A') for c in text]

        # Calculate the inverse of the Hill matrix
        det = int(round(np.linalg.det(self.hill_key_matrix)))
        det_inv = -1
        for i in range(26):
            if (det * i) % 26 == 1:
                det_inv = i
                break
        if det_inv == -1:
            raise ValueError("Modular inverse does not exist.")

        inv_matrix = (det_inv * np.round(det * np.linalg.inv(self.hill_key_matrix)).astype(int)) % 26
        
        decrypted = ""
        for i in range(0, len(text_num), 3):
            vector = np.array(text_num[i:i+3])
            decrypted_vector = np.dot(inv_matrix, vector) % 26
            for num in decrypted_vector:
                decrypted += chr(int(num) + ord('A'))
        
        # Remove padding if we know the original length
        if original_length is not None:
            decrypted = decrypted[:original_length]
        else:
            # Remove trailing X's (padding characters)
            decrypted = decrypted.rstrip('X')
        
        return decrypted

    def encrypt(self, plaintext):
        # Stage 1: Vigenere Encryption
        vigenere_encrypted = self._vigenere_encrypt(plaintext)
        
        # Store the original length before Hill padding
        original_length = len(vigenere_encrypted)
        
        # Stage 2: Hill Encryption (which adds padding)
        hill_encrypted = self._hill_encrypt(vigenere_encrypted, original_length)
        
        # Encode the original length into the ciphertext (prepend as 2 chars)
        # Convert length to 2-character representation (AA=0, AB=1, ..., ZZ=675)
        len_char1 = chr((original_length // 26) + ord('A'))
        len_char2 = chr((original_length % 26) + ord('A'))
        
        return len_char1 + len_char2 + hill_encrypted

    def decrypt(self, ciphertext):
        # Extract the original length from the first 2 characters
        if len(ciphertext) < 2:
            raise ValueError("Ciphertext is too short")
        
        len_char1 = ciphertext[0]
        len_char2 = ciphertext[1]
        original_length = (ord(len_char1) - ord('A')) * 26 + (ord(len_char2) - ord('A'))
        
        # Remove the length prefix
        ciphertext = ciphertext[2:]
        
        # Stage 1: Hill Decryption (which removes padding)
        hill_decrypted = self._hill_decrypt(ciphertext, original_length)

        # Stage 2: Vigenere Decryption
        vigenere_decrypted = self._vigenere_decrypt(hill_decrypted)
        return vigenere_decrypted
