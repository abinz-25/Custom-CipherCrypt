import numpy as np
from collections import Counter
from itertools import combinations

# Expected English letter frequencies
english_freq = {
    'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 'E': 0.12702,
    'F': 0.02228, 'G': 0.02015, 'H': 0.06094, 'I': 0.06966, 'J': 0.00153,
    'K': 0.00772, 'L': 0.04025, 'M': 0.02406, 'N': 0.06749, 'O': 0.07507,
    'P': 0.01929, 'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 'T': 0.09056,
    'U': 0.02758, 'V': 0.00978, 'W': 0.02360, 'X': 0.00150, 'Y': 0.01974,
    'Z': 0.00074
}

def frequency_analysis_attack(ciphertext, key_length):
    """
    Attempts to break the Vigenere cipher part using frequency analysis.
    """
    key = ""
    for i in range(key_length):
        sub_text = ""
        for j in range(i, len(ciphertext), key_length):
            sub_text += ciphertext[j]
        
        best_shift = 0
        min_chi_squared = float('inf')

        for shift in range(26):
            shifted_text = ""
            for char in sub_text:
                dec_char = chr(((ord(char) - ord('A') - shift + 26) % 26) + ord('A'))
                shifted_text += dec_char
            
            counts = Counter(shifted_text)
            chi_squared = 0
            for char, count in counts.items():
                expected = len(shifted_text) * english_freq[char]
                chi_squared += ((count - expected) ** 2) / expected
            
            if chi_squared < min_chi_squared:
                min_chi_squared = chi_squared
                best_shift = shift
        
        key += chr(best_shift + ord('A'))
    return key

def known_plaintext_attack(plaintext, ciphertext):
    """
    Attempts to break the Hill cipher part using a known-plaintext attack.
    This requires at least 9 pairs of plaintext/ciphertext characters.
    """
    if len(plaintext) < 9 or len(ciphertext) < 9:
        raise ValueError("Known-plaintext attack requires at least 9 characters of plaintext and ciphertext.")

    # Take the first 9 characters
    pt = [ord(c) - ord('A') for c in plaintext[:9].upper()]
    ct = [ord(c) - ord('A') for c in ciphertext[:9].upper()]

    P = np.array(pt).reshape(3, 3)
    C = np.array(ct).reshape(3, 3)

    try:
        P_inv = np.linalg.inv(P)
        det_P = int(round(np.linalg.det(P)))
        det_P_inv = -1
        for i in range(26):
            if (det_P * i) % 26 == 1:
                det_P_inv = i
                break
        if det_P_inv == -1:
            return None # No modular inverse

        P_adj = np.round(det_P * P_inv).astype(int)
        P_mod_inv = (det_P_inv * P_adj) % 26
        
        # K = C * P_inv
        key_matrix = np.dot(C, P_mod_inv) % 26
        return key_matrix
    except np.linalg.LinAlgError:
        return None # Matrix is singular
