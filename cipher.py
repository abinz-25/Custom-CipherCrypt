import numpy as np

class CustomCipher:
    def __init__(self, key):
        if len(key) < 10:
            raise ValueError("Key must be at least 10 characters long to support a Vigenere key and a 3x3 Hill cipher key.")
        
        # The last 9 characters form the Hill key
        self.hill_key_str = key[-9:]
        # The rest of the key forms the Vigenere key
        self.vigenere_key = key[:-9]

        if not self.vigenere_key:
             raise ValueError("Vigenere key part cannot be empty.")

        self.hill_key_matrix = self._create_hill_key_matrix(self.hill_key_str)

    def _create_hill_key_matrix(self, key_str):
        key_str = key_str.upper().replace("J", "I")
        key_num = [ord(c) - ord('A') for c in key_str]
        
        # Ensure the key is 9 characters long for a 3x3 matrix
        if len(key_num) != 9:
            raise ValueError("Hill cipher key part must be 9 characters long.")

        matrix = np.array(key_num).reshape(3, 3)
        
        # Check if the matrix is invertible
        det = int(round(np.linalg.det(matrix))) % 26
        if det == 0:
            raise ValueError("Hill cipher key matrix is not invertible (determinant is 0).")
        
        import math
        if math.gcd(det, 26) != 1:
            raise ValueError(f"Determinant ({det}) of Hill cipher key matrix is not coprime with 26, so it's not invertible modulo 26.")
        
        return matrix

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
        text = text.upper().replace("J", "I")
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
