from cipher import CustomCipher
from attack import frequency_analysis_attack, known_plaintext_attack
import time

def main():
    while True:
        print("\n--- Custom Cipher Menu ---")
        print("1. Encrypt a message")
        print("2. Decrypt a message")
        print("3. Run attack simulation")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            try:
                key = input("Enter a key (at least 10 characters): ")
                cipher = CustomCipher(key)
                plaintext = input("Enter the message to encrypt: ")
                
                # Remove spaces and non-alphabetic characters
                plaintext_cleaned = ''.join(c for c in plaintext if c.isalpha())
                
                if not plaintext_cleaned:
                    print("Error: Message must contain at least one letter.")
                    continue
                
                print(f"Cleaned plaintext (letters only): {plaintext_cleaned}")
                
                start_time = time.time()
                encrypted_message = cipher.encrypt(plaintext_cleaned)
                encryption_time = time.time() - start_time
                
                print(f"\nEncrypted: {encrypted_message}")
                print(f"Encryption Time: {encryption_time:.6f} seconds")
                print(f"\nFull Adjusted Key (use this for decryption): {cipher.get_full_key()}")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == '2':
            try:
                key = input("Enter a key (at least 10 characters): ")
                cipher = CustomCipher(key)
                ciphertext = input("Enter the message to decrypt: ")
                
                # Remove spaces from ciphertext
                ciphertext_cleaned = ''.join(c for c in ciphertext if not c.isspace())
                
                if not ciphertext_cleaned:
                    print("Error: Ciphertext cannot be empty.")
                    continue

                start_time = time.time()
                decrypted_message = cipher.decrypt(ciphertext_cleaned)
                decryption_time = time.time() - start_time

                print(f"\nDecrypted: {decrypted_message}")
                print(f"Decryption Time: {decryption_time:.6f} seconds")
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == '3':
            print("\n--- Running Attack Simulation ---")
            try:
                # Use a fixed key and plaintext for demonstration
                key = "SECRETGYBNQKURP"
                cipher = CustomCipher(key)
                plaintext = "THISISALONGERTESTMESSAGEFORBETTERFREQUENCYANALYSIS"
                print(f"Using sample plaintext: {plaintext}")
                print(f"Using sample key: {key}")

                encrypted_message = cipher.encrypt(plaintext)
                print(f"Generated ciphertext: {encrypted_message}")

                # 1. Frequency Analysis on the Vigenere part
                hill_decrypted = cipher._hill_decrypt(encrypted_message)
                vigenere_key_length = 6
                recovered_vigenere_key = frequency_analysis_attack(hill_decrypted, vigenere_key_length)
                print(f"\nRecovered Vigenere Key (Frequency Analysis): {recovered_vigenere_key}")
                print(f"Original Vigenere Key: {cipher.vigenere_key.upper()}")

                # 2. Known-Plaintext Attack on the Hill part
                vigenere_encrypted = cipher._vigenere_encrypt(plaintext)
                recovered_hill_key_matrix = known_plaintext_attack(vigenere_encrypted, encrypted_message)
                
                if recovered_hill_key_matrix is not None:
                    print("\nRecovered Hill Key Matrix (Known-Plaintext Attack):")
                    print(recovered_hill_key_matrix)
                    print("\nOriginal Hill Key Matrix:")
                    print(cipher.hill_key_matrix)
                else:
                    print("\nKnown-plaintext attack on Hill cipher failed (matrix was singular).")
            except ValueError as e:
                print(f"Error during simulation: {e}")

        elif choice == '4':
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
