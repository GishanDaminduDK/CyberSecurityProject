# CyberProject API

## Introduction
CyberProject is a web-based API hosted on Vercel that provides cryptographic functionalities, including key generation, encryption, decryption, and hashing. This project supports both AES and RSA key generation, data encryption and decryption, as well as hash generation and verification.

## API Endpoints

### 1. Generate AES Key
**Endpoint:** `POST https://cyber-security-project-l93d.vercel.app/generate-key`

```bash
curl -X POST "https://cyber-security-project-l93d.vercel.app/generate-key" \
     -H "Content-Type: application/json" \
     -d '{
           "key_type": "AES",
           "key_size": 256
         }'
```

### 2. Encrypt Data (AES)
**Endpoint:** `POST https://cyber-security-project-l93d.vercel.app/encrypt`

```bash
curl -X POST "https://cyber-security-project-l93d.vercel.app/encrypt" \
     -H "Content-Type: application/json" \
     -d '{
           "key_id": "ee9c26522ad3f3c5cb045918fd7ca4b7",
           "plaintext": "I go to school",
           "algorithm": "AES"
         }'
```

### 3. Decrypt Data (AES)
**Endpoint:** `POST https://cyber-security-project-l93d.vercel.app/decrypt`

```bash
curl -X POST "https://cyber-security-project-l93d.vercel.app/decrypt" \
     -H "Content-Type: application/json" \
     -d '{
           "key_id": "ee9c26522ad3f3c5cb045918fd7ca4b7",
           "ciphertext": "wvVesToBONQE9fcgZkuMtK+9gJ3M8YpsiuBuHjj1uz4Iu5MWlUXdirqSAaY5vg==",
           "algorithm": "AES"
         }'
```

### 4. Generate Hash
**Endpoint:** `POST https://cyber-security-project-l93d.vercel.app/generate-hash`

```bash
curl -X POST "https://cyber-security-project-l93d.vercel.app/generate-hash" \
     -H "Content-Type: application/json" \
     -d '{
           "data": "Data to hash",
           "algorithm": "SHA-256"
         }'
```

### 5. Verify Hash
**Endpoint:** `POST https://cyber-security-project-l93d.vercel.app/verify-hash`

```bash
curl -X POST "https://cyber-security-project-l93d.vercel.app/verify-hash" \
     -H "Content-Type: application/json" \
     -d '{
           "data": "Data to hash",
           "hash_value": "7dYwcXRexL6v4LOoC6LACcc+BC6GMAMmhoDOJ4+LS5c=",
           "algorithm": "SHA-256"
         }'
```

### 6. Generate RSA Key
**Endpoint:** `POST https://cyber-security-project-l93d.vercel.app/generate-key`

```bash
curl -X POST "https://cyber-security-project-l93d.vercel.app/generate-key" \
     -H "Content-Type: application/json" \
     -d '{
           "key_type": "RSA",
           "key_size": 1024
         }'
```

## Usage
- Copy and paste the `curl` commands into a terminal to interact with the API.
- Replace the `key_id`, `ciphertext`, or `hash_value` as necessary based on the API responses.

## License
This project is open-source and available under the MIT License.


