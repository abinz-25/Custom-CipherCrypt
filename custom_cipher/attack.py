import numpy as np
from collections import Counter
import math

# Expected English letter frequencies (from statistical analysis of English text)
english_freq = {
    'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 'E': 0.12702,
    'F': 0.02228, 'G': 0.02015, 'H': 0.06094, 'I': 0.06966, 'J': 0.00153,
    'K': 0.00772, 'L': 0.04025, 'M': 0.02406, 'N': 0.06749, 'O': 0.07507,
    'P': 0.01929, 'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 'T': 0.09056,
    'U': 0.02758, 'V': 0.00978, 'W': 0.02360, 'X': 0.00150, 'Y': 0.01974,
    'Z': 0.00074
}

def calculate_index_of_coincidence(text):
    """
    Calculate the Index of Coincidence (IC) to help determine key length.
    IC ≈ 0.065 for English text, ≈ 0.038 for random text.
    """
    text = text.upper()
    n = len(text)
    if n <= 1:
        return 0
    
    freq = Counter(text)
    ic = sum(count * (count - 1) for count in freq.values()) / (n * (n - 1))
    return ic

def find_key_length(ciphertext, max_length=20):
    """
    Estimate the Vigenère key length using Index of Coincidence method.
    """
    ciphertext = ciphertext.upper()
    best_length = 1
    best_avg_ic = 0
    
    for key_len in range(1, max_length + 1):
        ic_values = []
        for i in range(key_len):
            # Extract every key_len-th character starting at position i
            sub_text = ciphertext[i::key_len]
            if len(sub_text) > 1:
                ic = calculate_index_of_coincidence(sub_text)
                ic_values.append(ic)
        
        if ic_values:
            avg_ic = sum(ic_values) / len(ic_values)
            # Look for IC closest to 0.065 (English text)
            if abs(avg_ic - 0.065) < abs(best_avg_ic - 0.065):
                best_avg_ic = avg_ic
                best_length = key_len
    
    return best_length

def chi_squared_test(text):
    """
    Calculate chi-squared statistic comparing text frequency to English.
    Lower values indicate closer match to English.
    """
    text = text.upper()
    observed = Counter(text)
    n = len(text)
    
    chi_squared = 0
    for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        observed_count = observed.get(char, 0)
        expected_count = n * english_freq[char]
        
        if expected_count > 0:
            chi_squared += ((observed_count - expected_count) ** 2) / expected_count
    
    return chi_squared

def frequency_analysis_attack(ciphertext, key_length=None):
    """
    Attempts to break the Vigenere cipher using frequency analysis and chi-squared test.
    
    Args:
        ciphertext: The encrypted text (should be after Hill decryption)
        key_length: Length of Vigenère key. If None, will attempt to determine it.
    
    Returns:
        tuple: (recovered_key, decrypted_text, confidence_score)
    """
    ciphertext = ciphertext.upper()
    
    # If key length not provided, try to determine it
    if key_length is None:
        key_length = find_key_length(ciphertext)
        print(f"[Frequency Analysis] Estimated key length: {key_length}")
    
    recovered_key = ""
    
    # For each position in the key
    for position in range(key_length):
        # Extract every key_length-th character starting at this position
        sub_text = ciphertext[position::key_length]
        
        if len(sub_text) == 0:
            continue
        
        best_shift = 0
        best_chi_squared = float('inf')
        
        # Try all 26 possible shifts
        for shift in range(26):
            # Decrypt with this shift
            decrypted_sub = ""
            for char in sub_text:
                if 'A' <= char <= 'Z':
                    dec_char = chr(((ord(char) - ord('A') - shift + 26) % 26) + ord('A'))
                    decrypted_sub += dec_char
            
            # Calculate chi-squared statistic
            chi_sq = chi_squared_test(decrypted_sub)
            
            # Keep track of best shift
            if chi_sq < best_chi_squared:
                best_chi_squared = chi_sq
                best_shift = shift
        
        # Add the best shift to the key
        recovered_key += chr(best_shift + ord('A'))
    
    # Decrypt the full text with the recovered key
    decrypted = ""
    for i, char in enumerate(ciphertext):
        if 'A' <= char <= 'Z':
            shift = ord(recovered_key[i % len(recovered_key)]) - ord('A')
            dec_char = chr(((ord(char) - ord('A') - shift + 26) % 26) + ord('A'))
            decrypted += dec_char
        else:
            decrypted += char
    
    # Calculate confidence (based on chi-squared of result)
    confidence = 100 - min(chi_squared_test(decrypted), 100)
    
    return recovered_key, decrypted, confidence

def modular_matrix_inverse(matrix, modulus):
    """
    Calculate the modular inverse of a matrix in modulo arithmetic.
    """
    # Calculate determinant
    det = int(round(np.linalg.det(matrix))) % modulus
    
    # Find modular inverse of determinant
    det_inv = None
    for i in range(modulus):
        if (det * i) % modulus == 1:
            det_inv = i
            break
    
    if det_inv is None:
        raise ValueError(f"Determinant {det} has no inverse modulo {modulus}")
    
    # Calculate adjugate matrix
    matrix_inv = np.linalg.inv(matrix)
    adjugate = np.round(det * matrix_inv).astype(int) % modulus
    
    # Calculate modular inverse: (det^-1 * adjugate) mod modulus
    mod_inv = (det_inv * adjugate) % modulus
    
    return mod_inv

def known_plaintext_attack(plaintext, ciphertext):
    """
    Attempts to break the Hill cipher using a known-plaintext attack.
    
    Theory: If we know plaintext P and ciphertext C, and C = K × P (mod 26),
    then K = C × P^(-1) (mod 26)
    
    Args:
        plaintext: Known plaintext (at least 9 characters, after Vigenère encryption)
        ciphertext: Corresponding ciphertext (after Hill encryption)
    
    Returns:
        tuple: (recovered_key_matrix, success, message)
    """
    plaintext = plaintext.upper()
    ciphertext = ciphertext.upper()
    
    if len(plaintext) < 9 or len(ciphertext) < 9:
        return None, False, "Known-plaintext attack requires at least 9 characters"
    
    try:
        # Convert first 9 characters to numerical values
        pt_nums = [ord(c) - ord('A') for c in plaintext[:9] if 'A' <= c <= 'Z']
        ct_nums = [ord(c) - ord('A') for c in ciphertext[:9] if 'A' <= c <= 'Z']
        
        if len(pt_nums) < 9 or len(ct_nums) < 9:
            return None, False, "Need 9 alphabetic characters in both plaintext and ciphertext"
        
        # Create 3×3 matrices
        P = np.array(pt_nums[:9]).reshape(3, 3)
        C = np.array(ct_nums[:9]).reshape(3, 3)
        
        print(f"\n[Known-Plaintext Attack]")
        print(f"Plaintext matrix P:\n{P}")
        print(f"Ciphertext matrix C:\n{C}")
        
        # Calculate modular inverse of P
        try:
            P_inv = modular_matrix_inverse(P, 26)
            print(f"P^(-1) (mod 26):\n{P_inv}")
        except ValueError as e:
            return None, False, f"Plaintext matrix not invertible: {e}"
        
        # Recover key matrix: K = C × P^(-1) (mod 26)
        K = np.dot(C, P_inv) % 26
        K = K.astype(int)
        
        print(f"Recovered key matrix K:\n{K}")
        
        # Verify the key works
        test_encrypted = np.dot(K, P.T[0]) % 26
        expected = C.T[0]
        
        if np.array_equal(test_encrypted, expected):
            return K, True, "Key matrix successfully recovered!"
        else:
            return K, False, "Key matrix recovered but verification failed"
            
    except Exception as e:
        return None, False, f"Attack failed: {str(e)}"

def combined_attack(full_ciphertext, known_plaintext=None, known_ciphertext_portion=None):
    """
    Comprehensive attack combining multiple cryptanalysis techniques.
    
    Attack Strategy:
    1. Remove length prefix from full ciphertext
    2. If known plaintext available: Use known-plaintext attack on Hill cipher
    3. Otherwise: Try frequency analysis on different key lengths
    
    Args:
        full_ciphertext: Complete encrypted message (with length prefix)
        known_plaintext: Optional known plaintext (original message, not encrypted)
        known_ciphertext_portion: Optional known portion after Hill encryption
    
    Returns:
        dict: Attack results including recovered keys and decrypted text
    """
    results = {
        'success': False,
        'hill_key': None,
        'vigenere_key': None,
        'decrypted_text': None,
        'method_used': None,
        'confidence': 0
    }
    
    # Extract length and remove prefix
    if len(full_ciphertext) < 2:
        results['error'] = "Ciphertext too short"
        return results
    
    len_char1 = full_ciphertext[0]
    len_char2 = full_ciphertext[1]
    original_length = (ord(len_char1) - ord('A')) * 26 + (ord(len_char2) - ord('A'))
    
    ciphertext_no_prefix = full_ciphertext[2:]
    
    print(f"\n{'='*70}")
    print(f"COMBINED CRYPTANALYSIS ATTACK")
    print(f"{'='*70}")
    print(f"Ciphertext length (with prefix): {len(full_ciphertext)}")
    print(f"Encoded original length: {original_length}")
    print(f"Ciphertext (no prefix): {ciphertext_no_prefix}")
    
    # Attempt 1: Known-plaintext attack (if we have known plaintext)
    if known_plaintext and known_ciphertext_portion:
        print(f"\n[Attempt 1] Known-Plaintext Attack on Hill Cipher")
        hill_key, success, message = known_plaintext_attack(known_plaintext, known_ciphertext_portion)
        
        if success:
            results['hill_key'] = hill_key
            results['method_used'] = 'Known-Plaintext Attack'
            results['success'] = True
            print(f"✓ {message}")
            # Note: Would need Vigenère key to fully decrypt
        else:
            print(f"✗ {message}")
    
    # Attempt 2: Frequency analysis (try multiple key lengths)
    print(f"\n[Attempt 2] Frequency Analysis on Possible Vigenère Layer")
    print(f"Trying key lengths 1-15...")
    
    best_result = None
    best_confidence = 0
    
    for key_len in range(1, 16):
        try:
            recovered_key, decrypted, confidence = frequency_analysis_attack(
                ciphertext_no_prefix[:original_length], 
                key_length=key_len
            )
            
            if confidence > best_confidence:
                best_confidence = confidence
                best_result = (recovered_key, decrypted, key_len)
                
        except Exception as e:
            continue
    
    if best_result:
        recovered_key, decrypted, key_len = best_result
        print(f"\nBest result:")
        print(f"  Key length: {key_len}")
        print(f"  Recovered key: {recovered_key}")
        print(f"  Confidence: {best_confidence:.1f}%")
        print(f"  Decrypted text: {decrypted[:50]}{'...' if len(decrypted) > 50 else ''}")
        
        results['vigenere_key'] = recovered_key
        results['decrypted_text'] = decrypted
        results['confidence'] = best_confidence
        if not results['success']:
            results['method_used'] = 'Frequency Analysis'
            results['success'] = True
    
    return results


# Demonstration and testing functions
def demonstrate_attacks():
    """
    Comprehensive demonstration of both attack methods.
    """
    from cipher import CustomCipher
    
    print("\n" + "="*80)
    print("CRYPTANALYSIS DEMONSTRATION")
    print("="*80)
    
    # Setup
    key = "ALGORITHMS"
    plaintext = "THISISALONGERTESTMESSAGEFORBETTERFREQUENCYANALYSISANDCRYPTOGRAPHICATTACKS"
    
    cipher = CustomCipher(key)
    adjusted_key = cipher.get_full_key()
    
    print(f"\nOriginal Setup:")
    print(f"  Key: {key} → {adjusted_key}")
    print(f"  Plaintext: {plaintext}")
    print(f"  Length: {len(plaintext)} characters")
    
    # Encrypt
    ciphertext = cipher.encrypt(plaintext)
    print(f"\n  Encrypted: {ciphertext}")
    
    # Get intermediate values for attack demonstration
    vig_encrypted = cipher._vigenere_encrypt(plaintext)
    print(f"\n  After Vigenère: {vig_encrypted}")
    
    # Pad for Hill
    padded = vig_encrypted
    while len(padded) % 3 != 0:
        padded += 'X'
    
    hill_encrypted = cipher._hill_encrypt(padded)
    print(f"  After Hill: {hill_encrypted}")
    
    # ==================================================================
    # ATTACK 1: Frequency Analysis
    # ==================================================================
    print("\n" + "="*80)
    print("ATTACK 1: FREQUENCY ANALYSIS")
    print("="*80)
    print("\nScenario: Attacker intercepts ciphertext and tries to break Vigenère layer")
    print("Assumption: Hill layer has been removed (or attacker focuses on Vigenère)")
    
    # Use the Hill-encrypted text as if it's the target
    print(f"\nTarget ciphertext: {hill_encrypted[:50]}...")
    
    # Try to recover Vigenère key
    print(f"\nAttempting to recover Vigenère key...")
    recovered_key, decrypted, confidence = frequency_analysis_attack(
        hill_encrypted, 
        key_length=len(adjusted_key) - 9  # We know it's 1 character for demo
    )
    
    print(f"\nResults:")
    print(f"  Recovered Key: {recovered_key}")
    print(f"  Actual Key: {adjusted_key[9:]}")
    print(f"  Match: {'✓ YES' if recovered_key == adjusted_key[9:] else '✗ NO'}")
    print(f"  Confidence: {confidence:.1f}%")
    print(f"  Decrypted: {decrypted[:50]}...")
    
    # Calculate accuracy
    matches = sum(1 for i in range(min(len(recovered_key), len(adjusted_key[9:])))
                  if recovered_key[i] == adjusted_key[9:][i])
    accuracy = (matches / len(adjusted_key[9:])) * 100 if len(adjusted_key[9:]) > 0 else 0
    print(f"  Key Accuracy: {accuracy:.1f}%")
    
    # ==================================================================
    # ATTACK 2: Known-Plaintext Attack  
    # ==================================================================
    print("\n" + "="*80)
    print("ATTACK 2: KNOWN-PLAINTEXT ATTACK")
    print("="*80)
    print("\nScenario: Attacker knows plaintext and corresponding ciphertext")
    print("Goal: Recover Hill cipher key matrix")
    
    # Use first 9 characters of Vigenère output and Hill output
    known_plain = vig_encrypted[:9]
    known_cipher = hill_encrypted[:9]
    
    print(f"\nKnown plaintext (after Vigenère): {known_plain}")
    print(f"Known ciphertext (after Hill):    {known_cipher}")
    
    # Attempt attack
    recovered_matrix, success, message = known_plaintext_attack(known_plain, known_cipher)
    
    print(f"\n{message}")
    
    if success:
        print(f"\nOriginal Hill Matrix:")
        print(cipher.hill_key_matrix)
        print(f"\nRecovered Hill Matrix:")
        print(recovered_matrix)
        
        # Check if matrices match
        matrices_match = np.array_equal(cipher.hill_key_matrix, recovered_matrix)
        print(f"\nMatrices Match: {'✓ YES' if matrices_match else '✗ NO'}")
        
        if matrices_match:
            print("\n✓ ATTACK SUCCESSFUL! Full key matrix recovered!")
        else:
            # Calculate how many elements match
            total_elements = 9
            matching_elements = np.sum(cipher.hill_key_matrix == recovered_matrix)
            print(f"Matching elements: {matching_elements}/{total_elements}")
    
    # ==================================================================
    # ATTACK 3: Combined Attack
    # ==================================================================
    print("\n" + "="*80)
    print("ATTACK 3: COMBINED ATTACK STRATEGY")
    print("="*80)
    print("\nScenario: Attacker uses both techniques together")
    
    results = combined_attack(
        ciphertext,
        known_plaintext=vig_encrypted[:9],
        known_ciphertext_portion=hill_encrypted[:9]
    )
    
    print(f"\n{'='*80}")
    print("FINAL RESULTS")
    print(f"{'='*80}")
    print(f"Attack Success: {results['success']}")
    print(f"Method Used: {results.get('method_used', 'None')}")
    print(f"Confidence: {results.get('confidence', 0):.1f}%")
    
    if results.get('vigenere_key'):
        print(f"\nVigenère Key:")
        print(f"  Recovered: {results['vigenere_key']}")
        print(f"  Actual:    {adjusted_key[9:]}")
    
    if results.get('hill_key') is not None:
        print(f"\nHill Key Matrix Recovered: ✓")
    
    print(f"\n{'='*80}\n")


if __name__ == "__main__":
    demonstrate_attacks()

