from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
import hashlib
import base64
import secrets
import os

app = FastAPI()

# In-memory storage for cryptographic keys
keys_store = {}

# Pydantic models for request/response validation
class KeyGenerationRequest(BaseModel):
    key_type: str
    key_size: int

class KeyGenerationResponse(BaseModel):
    key_id: str
    key_value: str

class EncryptionRequest(BaseModel):
    key_id: str
    plaintext: str
    algorithm: str

class EncryptionResponse(BaseModel):
    ciphertext: str

class DecryptionRequest(BaseModel):
    key_id: str
    ciphertext: str
    algorithm: str

class DecryptionResponse(BaseModel):
    plaintext: str

class HashGenerationRequest(BaseModel):
    data: str
    algorithm: str

class HashGenerationResponse(BaseModel):
    hash_value: str
    algorithm: str

class HashVerificationRequest(BaseModel):
    data: str
    hash_value: str
    algorithm: str

class HashVerificationResponse(BaseModel):
    is_valid: bool
    message: str

# Helper functions
def generate_aes_key(key_size):
    return get_random_bytes(key_size // 8)

def aes_encrypt(key, plaintext):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode())
    combined = nonce + tag + ciphertext
    return base64.b64encode(combined).decode()

def aes_decrypt(key, ciphertext_b64):
    combined = base64.b64decode(ciphertext_b64)
    nonce = combined[:16]
    tag = combined[16:32]
    ciphertext = combined[32:]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag).decode()

def rsa_encrypt(public_key, plaintext):
    rsa_key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(rsa_key)
    return base64.b64encode(cipher.encrypt(plaintext.encode())).decode()

def rsa_decrypt(private_key, ciphertext_b64):
    ciphertext = base64.b64decode(ciphertext_b64)
    rsa_key = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(rsa_key)
    return cipher.decrypt(ciphertext).decode()

# API Endpoints
@app.post("/generate-key", response_model=KeyGenerationResponse)
async def generate_key(request: KeyGenerationRequest):
    key_id = secrets.token_hex(16)
    try:
        if request.key_type == "AES":
            if request.key_size not in [128, 192, 256]:
                raise ValueError("Invalid AES key size")
            key = generate_aes_key(request.key_size)
            keys_store[key_id] = {
                "type": "AES",
                "key": key
            }
            key_value = base64.b64encode(key).decode()
            
        elif request.key_type == "RSA":
            if request.key_size not in [1024, 2048, 4096]:
                raise ValueError("Invalid RSA key size")
            key_pair = RSA.generate(request.key_size)
            public_key = key_pair.publickey().export_key()
            private_key = key_pair.export_key()
            keys_store[key_id] = {
                "type": "RSA",
                "public": public_key,
                "private": private_key
            }
            key_value = base64.b64encode(public_key).decode()
            
        else:
            raise ValueError("Invalid key type")
        
        return {"key_id": key_id, "key_value": key_value}
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/encrypt", response_model=EncryptionResponse)
async def encrypt(request: EncryptionRequest):
    key_data = keys_store.get(request.key_id)
    if not key_data:
        raise HTTPException(status_code=404, detail="Key not found")
    
    try:
        if request.algorithm == "AES":
            if key_data["type"] != "AES":
                raise ValueError("Key type mismatch")
            ciphertext = aes_encrypt(key_data["key"], request.plaintext)
            
        elif request.algorithm == "RSA":
            if key_data["type"] != "RSA":
                raise ValueError("Key type mismatch")
            ciphertext = rsa_encrypt(key_data["public"], request.plaintext)
            
        else:
            raise ValueError("Unsupported algorithm")
        
        return {"ciphertext": ciphertext}
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Encryption failed")

@app.post("/decrypt", response_model=DecryptionResponse)
async def decrypt(request: DecryptionRequest):
    key_data = keys_store.get(request.key_id)
    if not key_data:
        raise HTTPException(status_code=404, detail="Key not found")
    
    try:
        if request.algorithm == "AES":
            if key_data["type"] != "AES":
                raise ValueError("Key type mismatch")
            plaintext = aes_decrypt(key_data["key"], request.ciphertext)
            
        elif request.algorithm == "RSA":
            if key_data["type"] != "RSA":
                raise ValueError("Key type mismatch")
            plaintext = rsa_decrypt(key_data["private"], request.ciphertext)
            
        else:
            raise ValueError("Unsupported algorithm")
        
        return {"plaintext": plaintext}
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Decryption failed")

@app.post("/generate-hash", response_model=HashGenerationResponse)
async def generate_hash(request: HashGenerationRequest):
    try:
        hasher = hashlib.new(request.algorithm)
        hasher.update(request.data.encode())
        hash_value = base64.b64encode(hasher.digest()).decode()
        return {
            "hash_value": hash_value,
            "algorithm": request.algorithm
        }
    except ValueError:
        raise HTTPException(status_code=400, detail="Unsupported hashing algorithm")

@app.post("/verify-hash", response_model=HashVerificationResponse)
async def verify_hash(request: HashVerificationRequest):
    try:
        hasher = hashlib.new(request.algorithm)
        hasher.update(request.data.encode())
        calculated_hash = base64.b64encode(hasher.digest()).decode()
        is_valid = secrets.compare_digest(calculated_hash, request.hash_value)
        
        return {
            "is_valid": is_valid,
            "message": "Hash matches the data." if is_valid else "Hash does not match"
        }
    except ValueError:
        raise HTTPException(status_code=400, detail="Unsupported hashing algorithm")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)