import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="DevOps CI/CD Lab API",
    version=os.getenv("APP_VERSION", "1.0.0"),
    description="Sample Microservice for CI/CD Pipeline Practice"
)

class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str

class MessageResponse(BaseModel):
    message: str
    data: dict

@app.get("/health", response_model=HealthResponse)
def health_check():
    """Health check endpoint used by Kubernetes/Docker probes"""
    return HealthResponse(
        status="healthy",
        version=os.getenv("APP_VERSION", "1.0.0"),
        environment=os.getenv("APP_ENV", "development")
    )

@app.get("/api/v1/info", response_model=MessageResponse)
def get_info():
    """Sample API endpoint for testing"""
    return MessageResponse(
        message="DevOps CI/CD Service is running successfully!",
        data={
            "app_name": "devops-backend-api",
            "uptime_status": "ok",
            "features": ["ci", "cd", "docker", "k8s"]
        }
    )

@app.get("/api/v1/calculate")
def calculate(a: float, b: float, op: str = "add"):
    """Calculation endpoint to demonstrate unit & integration testing"""
    if op == "add":
        return {"result": a + b}
    elif op == "subtract":
        return {"result": a - b}
    elif op == "multiply":
        return {"result": a * b}
    elif op == "divide":
        if b == 0:
            raise HTTPException(status_code=400, detail="Cannot divide by zero")
        return {"result": a / b}
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported operator: {op}")

@app.get("/api/v1/discount")
def calculate_discount(price: float, rate: float):
    """Tính giá sau khi giảm giá (Cố ý viết sai logic để thử nghiệm CI)"""
    # Lỗi cố ý: Thay vì price * (1 - rate), lại viết nhầm thành cộng giá
    final_price = price + (price * rate)
    return {
        "original_price": price,
        "discount_rate": rate,
        "final_price": final_price
    }

