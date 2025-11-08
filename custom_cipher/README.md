# Custom Cipher Design and Analysis

This project implements a custom cipher that combines the Vigenere and Hill ciphers. It also includes methods to attack the cipher, demonstrating concepts from network and information security.

## Cipher Design

The custom cipher uses a two-stage encryption process:
1.  **Vigenere Cipher:** The plaintext is first encrypted using a Vigenere cipher. This provides a layer of polyalphabetic substitution.
2.  **Hill Cipher:** The result of the Vigenere encryption is then encrypted using a Hill cipher. This adds confusion and diffusion by operating on blocks of letters.

The key for the custom cipher is a string of at least 10 characters.
*   The first 6 characters are used as the key for the Vigenere cipher.
*   The next 9 characters are used to form the 3x3 key matrix for the Hill cipher.

## Implementation

The implementation is done in Python and requires the `numpy` library.

*   `cipher.py`: Contains the `CustomCipher` class, which handles encryption and decryption.
*   `attack.py`: Implements the frequency analysis and known-plaintext attacks.
*   `main.py`: A driver program to demonstrate the cipher and the attacks.

### Running the Code
1.  Install numpy: `pip install numpy`
2.  Run the main program: `python main.py`

## Security Analysis and Attack

Two attack methods are implemented:

1.  **Frequency Analysis:** This attack targets the Vigenere cipher part. By analyzing the frequency of letters in segments of the ciphertext, it's possible to determine the Vigenere key. This attack is more effective on longer ciphertexts.

2.  **Known-Plaintext Attack:** This attack targets the Hill cipher. If an attacker has a piece of plaintext and its corresponding ciphertext, they can set up a system of linear equations to solve for the Hill cipher's key matrix. This attack is very effective if enough plaintext/ciphertext pairs are known.

## Efficiency

*   **Encryption/Decryption Time Complexity:**
    *   Vigenere cipher: O(N), where N is the length of the message.
    *   Hill cipher: O(N), as it processes the message in fixed-size blocks.
    *   Overall: O(N).

*   **Comparison to Shift Cipher:**
    *   A simple Shift cipher also has a time complexity of O(N). However, the custom cipher is significantly more secure due to the combination of polyalphabetic substitution and block-based transposition, at the cost of a slightly higher constant factor in its execution time.
