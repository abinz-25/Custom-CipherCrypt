# Complete Encryption Flow Example
## Step-by-Step Implementation: HELLOWORLD → AKDUPIWHQBFYLE

---

## Overview

This document provides a detailed, step-by-step walkthrough of how the custom Vigenère-Hill cipher encrypts the plaintext **"HELLOWORLD"** using the key **"ALGORITHMS"**.

---

## INPUT PARAMETERS

| Parameter | Value | Length |
|-----------|-------|--------|
| **Original Key** | ALGORITHMS | 10 characters |
| **Plaintext** | HELLOWORLD | 10 characters |

---

## STEP 1: KEY DERIVATION & ADJUSTMENT

### 1.1 Initial Key Split

The key is split into two parts:
- **First 9 characters** → Hill cipher key (for 3×3 matrix)
- **Remaining characters** → Vigenère cipher key

```
Key: ALGORITHMS (10 characters)
├── Hill Key:     ALGORITHM (9 characters)
└── Vigenère Key: S         (1 character)
```

### 1.2 Hill Matrix Creation (Original Key)

Convert "ALGORITHM" to numerical values (A=0, B=1, ..., Z=25):

```
A=0, L=11, G=6, O=14, R=17, I=8, T=19, H=7, M=12
```

Arrange into 3×3 matrix:

```
       [ A   L   G ]       [  0  11   6 ]
K₀ =   [ O   R   I ]   =   [ 14  17   8 ]
       [ T   H   M ]       [ 19   7  12 ]
```

### 1.3 Matrix Validation

Calculate determinant modulo 26:

```
det(K₀) = 0×(17×12 - 8×7) - 11×(14×12 - 8×19) + 6×(14×7 - 17×19)
        = 0×148 - 11×16 + 6×(-225)
        = 0 - 176 - 1350
        = -1526
        ≡ -1526 mod 26
        ≡ 6 mod 26
```

**Check**: gcd(6, 26) = 2 ≠ 1 ❌

**Result**: Matrix is NOT invertible! Automatic adjustment required.

### 1.4 Automatic Key Adjustment

The system tries **Strategy 2: Positional Adjustment**

After testing, it finds that adjusting **position 2** (letter 'G') by +1 creates a valid matrix:

```
Original: ALGORITHM
Adjusted: ALHORITHM (G→H at position 2)
```

**Adjusted Hill Matrix**:

```
       [ A   L   H ]       [  0  11   7 ]
K =    [ O   R   I ]   =   [ 14  17   8 ]
       [ T   H   M ]       [ 19   7  12 ]
```

### 1.5 Adjusted Matrix Validation

Calculate new determinant:

```
det(K) = 0×(17×12 - 8×7) - 11×(14×12 - 8×19) + 7×(14×7 - 17×19)
       = 0×148 - 11×16 + 7×(-225)
       = 0 - 176 - 1575
       = -1751
       ≡ -1751 mod 26
       ≡ 15 mod 26
```

**Check**: gcd(15, 26) = 1 ✓

**Result**: Matrix IS invertible! ✓

### 1.6 Final Adjusted Key

```
Hill Key (Adjusted):  ALHORITHM (9 characters)
Vigenère Key:         S         (1 character)
Full Adjusted Key:    ALHORITHMS (10 characters)
```

---

## STEP 2: PREPROCESSING

### 2.1 Text Cleaning

Apply preprocessing rules:

| Rule | Input | Output |
|------|-------|--------|
| Original | HELLOWORLD | HELLOWORLD |
| Convert to uppercase | HELLOWORLD | HELLOWORLD |
| Replace J→I | HELLOWORLD | HELLOWORLD (no J) |
| Remove non-letters | HELLOWORLD | HELLOWORLD (no non-letters) |

**Cleaned Plaintext**: `HELLOWORLD` (10 characters)

---

## STEP 3: VIGENÈRE ENCRYPTION

### 3.1 Vigenère Key Setup

```
Vigenère Key: S
Shift Value:  S = 18 (in 0-25 range)
```

### 3.2 Character-by-Character Encryption

Apply Caesar shift of 18 to each character:

| Pos | Plaintext | Value | Formula | Calculation | Result | Ciphertext |
|-----|-----------|-------|---------|-------------|--------|------------|
| 0 | H | 7 | (7+18) mod 26 | 25 mod 26 | 25 | **Z** |
| 1 | E | 4 | (4+18) mod 26 | 22 mod 26 | 22 | **W** |
| 2 | L | 11 | (11+18) mod 26 | 29 mod 26 | 3 | **D** |
| 3 | L | 11 | (11+18) mod 26 | 29 mod 26 | 3 | **D** |
| 4 | O | 14 | (14+18) mod 26 | 32 mod 26 | 6 | **G** |
| 5 | W | 22 | (22+18) mod 26 | 40 mod 26 | 14 | **O** |
| 6 | O | 14 | (14+18) mod 26 | 32 mod 26 | 6 | **G** |
| 7 | R | 17 | (17+18) mod 26 | 35 mod 26 | 9 | **J** |
| 8 | L | 11 | (11+18) mod 26 | 29 mod 26 | 3 | **D** |
| 9 | D | 3 | (3+18) mod 26 | 21 mod 26 | 21 | **V** |

### 3.3 Vigenère Result

```
Input:  HELLOWORLD (10 characters)
Output: ZWDDGOGJDV (10 characters)
```

**Verification**: This matches the actual code output ✓

---

## STEP 4: STORE ORIGINAL LENGTH

Before padding, store the original length for decryption:

```
Original Length = 10 characters
```

This will be encoded and prepended to the final ciphertext.

---

## STEP 5: PADDING FOR HILL CIPHER

### 5.1 Calculate Padding Requirement

Hill cipher works with 3-character blocks:

```
Current length: 10
10 mod 3 = 1 (remainder)
Padding needed: 3 - 1 = 2 characters
```

### 5.2 Apply Padding

Add 'X' characters to make length divisible by 3:

```
Before Padding: ZWDDGOGJDV   (10 characters)
After Padding:  ZWDDGOGJDVXX (12 characters)
Padding Added:  XX
```

---

## STEP 6: HILL ENCRYPTION

### 6.1 Hill Matrix

Using the adjusted Hill key "ALHORITHM":

```
       [  0  11   7 ]
K =    [ 14  17   8 ]
       [ 19   7  12 ]
```

### 6.2 Convert Text to Blocks

Split padded text into 3-character blocks:

```
Block 1: ZWD  → [25, 22, 3]
Block 2: DGO  → [3, 6, 14]
Block 3: GJD  → [6, 9, 3]
Block 4: VXX  → [21, 23, 23]
```

### 6.3 Block-by-Block Encryption

#### **Block 1: ZWD [25, 22, 3]**

Matrix multiplication:

```
[  0  11   7 ]   [ 25 ]   [ 0×25 + 11×22 + 7×3  ]
[ 14  17   8 ] × [ 22 ] = [ 14×25 + 17×22 + 8×3 ]
[ 19   7  12 ]   [ 3  ]   [ 19×25 + 7×22 + 12×3 ]
```

Calculate each element:

```
Row 1: 0×25 + 11×22 + 7×3  = 0 + 242 + 21 = 263
Row 2: 14×25 + 17×22 + 8×3 = 350 + 374 + 24 = 748
Row 3: 19×25 + 7×22 + 12×3 = 475 + 154 + 36 = 665
```

Apply modulo 26:

```
263 mod 26 = 3  → D
748 mod 26 = 20 → U
665 mod 26 = 15 → P
```

**Result**: `DUP`

#### **Block 2: DGO [3, 6, 14]**

Matrix multiplication:

```
[  0  11   7 ]   [ 3  ]   [ 0×3 + 11×6 + 7×14  ]
[ 14  17   8 ] × [ 6  ] = [ 14×3 + 17×6 + 8×14 ]
[ 19   7  12 ]   [ 14 ]   [ 19×3 + 7×6 + 12×14 ]
```

Calculate each element:

```
Row 1: 0×3 + 11×6 + 7×14  = 0 + 66 + 98 = 164
Row 2: 14×3 + 17×6 + 8×14 = 42 + 102 + 112 = 256
Row 3: 19×3 + 7×6 + 12×14 = 57 + 42 + 168 = 267
```

Apply modulo 26:

```
164 mod 26 = 8  → I
256 mod 26 = 22 → W
267 mod 26 = 7  → H
```

**Result**: `IWH`

#### **Block 3: GJD [6, 9, 3]**

Matrix multiplication:

```
[  0  11   7 ]   [ 6 ]   [ 0×6 + 11×9 + 7×3  ]
[ 14  17   8 ] × [ 9 ] = [ 14×6 + 17×9 + 8×3 ]
[ 19   7  12 ]   [ 3 ]   [ 19×6 + 7×9 + 12×3 ]
```

Calculate each element:

```
Row 1: 0×6 + 11×9 + 7×3  = 0 + 99 + 21 = 120
Row 2: 14×6 + 17×9 + 8×3 = 84 + 153 + 24 = 261
Row 3: 19×6 + 7×9 + 12×3 = 114 + 63 + 36 = 213
```

Apply modulo 26:

```
120 mod 26 = 16 → Q
261 mod 26 = 1  → B
213 mod 26 = 5  → F
```

**Result**: `QBF`

#### **Block 4: VXX [21, 23, 23]**

Matrix multiplication:

```
[  0  11   7 ]   [ 21 ]   [ 0×21 + 11×23 + 7×23  ]
[ 14  17   8 ] × [ 23 ] = [ 14×21 + 17×23 + 8×23 ]
[ 19   7  12 ]   [ 23 ]   [ 19×21 + 7×23 + 12×23 ]
```

Calculate each element:

```
Row 1: 0×21 + 11×23 + 7×23  = 0 + 253 + 161 = 414
Row 2: 14×21 + 17×23 + 8×23 = 294 + 391 + 184 = 869
Row 3: 19×21 + 7×23 + 12×23 = 399 + 161 + 276 = 836
```

Apply modulo 26:

```
414 mod 26 = 24 → Y
869 mod 26 = 11 → L
836 mod 26 = 4  → E
```

**Result**: `YLE`

### 6.4 Combine All Blocks

```
Block 1: DUP
Block 2: IWH
Block 3: QBF
Block 4: YLE

Hill Encrypted Result: DUPIWHQBFYLE (12 characters)
```

---

## STEP 7: LENGTH ENCODING

### 7.1 Calculate Length Prefix

Encode the original length (10) into 2 characters:

```
Original Length = 10

char1 = (10 ÷ 26) + 'A' = 0 + 'A' = 'A'
char2 = (10 mod 26) + 'A' = 10 + 'A' = 'K'

Length Prefix: AK
```

### 7.2 Verification

Decode to verify:

```
Length = (ord('A') - ord('A')) × 26 + (ord('K') - ord('A'))
       = (0) × 26 + (10)
       = 0 + 10
       = 10 ✓
```

---

## STEP 8: FINAL CIPHERTEXT ASSEMBLY

### 8.1 Combine Components

```
Length Prefix:    AK           (2 characters)
Hill Encrypted:   DUPIWHQBFYLE (12 characters)

Final Ciphertext: AKDUPIWHQBFYLE (14 characters)
```

---

## COMPLETE FLOW VISUALIZATION

```
┌─────────────────────────────────────────────────────────────────┐
│                    ENCRYPTION FLOW DIAGRAM                       │
└─────────────────────────────────────────────────────────────────┘

INPUT:
Key: ALGORITHMS (10 chars) → Split → Hill: ALGORITHM, Vigenère: S
Plaintext: HELLOWORLD (10 chars)
                    ↓
┌───────────────────────────────────────────────────────────────┐
│ STEP 1: KEY ADJUSTMENT                                        │
│ ALGORITHM → ALHORITHM (position 2: G→H)                       │
│ Matrix becomes invertible: det=15, gcd(15,26)=1 ✓            │
└───────────────────────────────────────────────────────────────┘
                    ↓
┌───────────────────────────────────────────────────────────────┐
│ STEP 2: PREPROCESSING                                         │
│ HELLOWORLD → HELLOWORLD (already clean)                       │
└───────────────────────────────────────────────────────────────┘
                    ↓
┌───────────────────────────────────────────────────────────────┐
│ STEP 3: VIGENÈRE ENCRYPTION                                   │
│ Key: S (shift +18)                                            │
│ HELLOWORLD → ZWDDGOGJDV (10 chars)                           │
└───────────────────────────────────────────────────────────────┘
                    ↓
┌───────────────────────────────────────────────────────────────┐
│ STEP 4: STORE LENGTH                                          │
│ Original length = 10                                          │
└───────────────────────────────────────────────────────────────┘
                    ↓
┌───────────────────────────────────────────────────────────────┐
│ STEP 5: PADDING                                               │
│ ZWDDGOGJDV → ZWDDGOGJDVXX (add XX, 10→12 chars)             │
└───────────────────────────────────────────────────────────────┘
                    ↓
┌───────────────────────────────────────────────────────────────┐
│ STEP 6: HILL ENCRYPTION                                       │
│ Matrix: ALHORITHM (3×3)                                       │
│ Blocks: ZWD|DGO|GJD|VXX                                       │
│ Result: DUP|IWH|QBF|YLE                                       │
│ ZWDDGOGJDVXX → DUPIWHQBFYLE (12 chars)                       │
└───────────────────────────────────────────────────────────────┘
                    ↓
┌───────────────────────────────────────────────────────────────┐
│ STEP 7: LENGTH ENCODING                                       │
│ Length 10 → "AK" prefix                                       │
└───────────────────────────────────────────────────────────────┘
                    ↓
┌───────────────────────────────────────────────────────────────┐
│ STEP 8: FINAL ASSEMBLY                                        │
│ AK + DUPIWHQBFYLE = AKDUPIWHQBFYLE (14 chars)                │
└───────────────────────────────────────────────────────────────┘
                    ↓
OUTPUT: AKDUPIWHQBFYLE
```

---

## SIZE ANALYSIS

| Stage | Content | Length | Change |
|-------|---------|--------|--------|
| Original Plaintext | HELLOWORLD | 10 | - |
| After Vigenère | ZWDDGOGJDV | 10 | +0 |
| After Padding | ZWDDGOGJDVXX | 12 | +2 |
| After Hill | DUPIWHQBFYLE | 12 | +0 |
| With Length Prefix | AKDUPIWHQBFYLE | 14 | +2 |
| **Total Change** | - | - | **+4** |

---

## SUMMARY TABLE

| Parameter | Value |
|-----------|-------|
| **Original Key** | ALGORITHMS |
| **Adjusted Key** | ALHORITHMS |
| **Hill Key** | ALHORITHM |
| **Vigenère Key** | S |
| **Original Plaintext** | HELLOWORLD (10 chars) |
| **After Vigenère** | ZWDDGOGJDV (10 chars) |
| **After Padding** | ZWDDGOGJDVXX (12 chars) |
| **After Hill** | DUPIWHQBFYLE (12 chars) |
| **Length Prefix** | AK (2 chars) |
| **Final Ciphertext** | AKDUPIWHQBFYLE (14 chars) |
| **Size Increase** | +4 characters |

---

## DECRYPTION PROCESS (REVERSE)

To decrypt `AKDUPIWHQBFYLE` back to `HELLOWORLD`:

1. **Extract Length Prefix**: AK → original length = 10
2. **Remove Prefix**: DUPIWHQBFYLE
3. **Hill Decryption**: DUPIWHQBFYLE → ZWDDGOGJDVXX (using inverse matrix)
4. **Remove Padding**: ZWDDGOGJDVXX → ZWDDGOGJDV (keep first 10 chars)
5. **Vigenère Decryption**: ZWDDGOGJDV → HELLOWORLD (subtract shift of 18)

**Result**: HELLOWORLD ✓

---

## KEY MATHEMATICAL CONCEPTS

### Vigenère Cipher Formula

**Encryption**: 
```
Cᵢ = (Pᵢ + Kⱼ) mod 26
```
where j = i mod |K|

**Decryption**: 
```
Pᵢ = (Cᵢ - Kⱼ + 26) mod 26
```

### Hill Cipher Formula

**Encryption**: 
```
C = K × P (mod 26)
```

**Decryption**: 
```
P = K⁻¹ × C (mod 26)
```

where K⁻¹ is the modular multiplicative inverse of matrix K

---

## NOTES

1. **Key Adjustment**: The automatic adjustment from ALGORITHM to ALHORITHM is deterministic and will always produce the same result for the same invalid key.

2. **Padding Character**: The letter 'X' is used as padding because it's relatively uncommon in English text.

3. **Length Encoding Range**: The 2-character prefix can encode lengths from 0 to 675 characters:
   - AA = 0
   - AZ = 25
   - BA = 26
   - ZZ = 675

4. **Security Note**: This is an educational cipher combining classical techniques. It is NOT suitable for real-world cryptographic applications.

---

*Generated for Network and Information Security Project (CT-486)*
