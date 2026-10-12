import os
import time
import socket
import random
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis
from pymongo import MongoClient

app = FastAPI()

# Cloud Infrastructure Connections
try:
    redis_client = redis.Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"), decode_responses=True)
    mongo_client = MongoClient(os.getenv("MONGO_URI"))
    db = mongo_client.cloud_tutor_db
    logs_collection = db.interaction_logs
except Exception as e:
    print(f"Database connection error: {e}")

class ChatRequest(BaseModel):
    prompt: str
    model: str = "gemini-1.5-flash" # Hardcoded model payload

@app.get("/health")
def health_check():
    """Returns load balancer and compute node diagnostics."""
    return {
        "status": "Healthy",
        "compute_node_id": socket.gethostname(),
        "timestamp": time.time()
    }

@app.get("/analytics")
def get_analytics():
    """Fetches usage metrics from persistent MongoDB storage."""
    total_docs = logs_collection.count_documents({})
    recent_logs = list(logs_collection.find({}, {"_id": 0}).sort("timestamp", -1).limit(5))
    return {
        "total_queries": total_docs,
        "recent_activity": recent_logs
    }

@app.post("/chat")
def process_chat(request: ChatRequest):
    start_time = time.time()
    
    # Distributed Caching Layer (Redis)
    cached_response = redis_client.get(request.prompt)
    if cached_response:
        latency = time.time() - start_time
        return {"response": cached_response, "cache_status": "hit", "latency": latency}
    
    # Simulate API call to LLM
    ai_response = f"Processed response for: {request.prompt}"
    
    # Cache the new response for 1 hour
    redis_client.set(request.prompt, ai_response, ex=3600)
    
    # Persistent State Logging (MongoDB)
    fake_identities = ["Student_A49", "Guest_902", "User_Sigma", "Scholar_Delta", "Test_User_77"]
    logs_collection.insert_one({
        "user_id": random.choice(fake_identities),
        "prompt": request.prompt,
        "model_used": request.model,
        "timestamp": time.time()
    })
    
    latency = time.time() - start_time
    return {"response": ai_response, "cache_status": "miss", "latency": latency}