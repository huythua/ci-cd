# 🚀 LAB 04: Continuous Delivery (CD) & Triển khai Zero-Downtime

## 🎯 Mục tiêu bài học
1. Hiểu sự khác biệt giữa **Continuous Delivery** (Chờ duyệt thủ công trước khi lên Production) và **Continuous Deployment** (Tự động 100%).
2. Thiết lập cơ chế **Rolling Update** trên Docker Compose & Kubernetes để cập nhật phiên bản mới mà không bị gián đoạn dịch vụ (Zero-Downtime).
3. Thực hiện **Health Check & Auto-Rollback** khi service mới bị lỗi khởi động (CrashLoopBackOff).

---

## 🔄 1. Nguyên lý Rolling Update & Health Checks

```mermaid
sequenceDiagram
    participant LB as Load Balancer / Ingress
    participant V1 as Pod Version 1 (Cũ)
    participant V2 as Pod Version 2 (Mới)
    
    Note over LB, V1: Lưu lượng đang đổ vào V1
    LB->>V1: Route traffic (200 OK)
    
    Note over V2: Khởi tạo Container mới
    V2->>V2: Chạy Readiness Probe (/health)
    
    alt /health trả về 200 OK
        LB->>V2: Chuyển lưu lượng sang V2
        LB--xV1: Ngừng gửi traffic vào V1
        V1->>V1: Graceful Shutdown (SIGTERM)
    else /health bị lỗi
        LB--xV2: KHÔNG chuyển lưu lượng
        Note over LB, V1: Hệ thống vẫn hoạt động an toàn trên V1
    end
```

---

## 🛠️ 2. Thử nghiệm trên Local với Docker Compose
```bash
# Khởi chạy cụm dịch vụ Production-like:
docker compose -f deployments/docker-compose/docker-compose.prod.yml up -d --build

# Kiểm tra trạng thái và logs:
docker compose -f deployments/docker-compose/docker-compose.prod.yml ps
curl http://localhost:8000/health
curl http://localhost:3000/health
```
