# 🚀 DevOps CI/CD Hands-on Mastery Lab

Repository thực hành chuyên sâu về **DevOps, CI/CD, Containerization, DevSecOps và Kubernetes** cho Microservices.

---

## 📁 Cấu trúc Thư mục

```text
devops-cicd-lab/
├── .github/workflows/         # 🌟 Pipeline CI/CD hoàn chỉnh trên GitHub Actions
│   ├── 01-ci-test-lint.yml       # Linter + Unit Testing + Coverage matrix
│   ├── 02-docker-build-push.yml  # Multi-stage Docker build + Buildx Cache + GHCR push
│   ├── 03-security-scan.yml      # Trivy Container Scan + Gitleaks Secret Detection
│   └── 04-cd-deploy.yml          # Continuous Delivery to Staging/Prod with Approvals
├── .gitlab-ci.yml             # 🦊 Pipeline tương đương chuẩn cho GitLab CI
├── apps/                      # 📦 Các Microservices mẫu
│   ├── backend-api/              # Python FastAPI REST API (Tests, Healthcheck, Multi-stage Docker)
│   └── frontend-web/             # Express/Node.js Web Portal (Unit test, Alpine Docker)
├── deployments/               # 🚢 Cấu hình hạ tầng & triển khai
│   ├── docker-compose/           # Compose cho Dev & Production
│   └── kubernetes/               # Manifests K8s (Deployment, Service, RollingUpdate, Probes)
└── docs/                      # 📚 Tài liệu hướng dẫn chi tiết từng Lab
    ├── LAB-01-DOCKER-OPTIMIZATION.md
    ├── LAB-02-CI-PIPELINE.md
    ├── LAB-03-SECURITY-SCANNING.md
    └── LAB-04-CD-DEPLOYMENT.md
```

---

## 🎯 Các bài Lab thực hành

| Lab | Nội dung | File hướng dẫn |
| :--- | :--- | :--- |
| **Lab 01** | Tối ưu hóa Dockerfile (Multi-stage, Non-root user, Caching) | [LAB-01](docs/LAB-01-DOCKER-OPTIMIZATION.md) |
| **Lab 02** | Xây dựng CI Pipeline tự động (Matrix build, Linter, Test, Cache GHA) | [LAB-02](docs/LAB-02-CI-PIPELINE.md) |
| **Lab 03** | DevSecOps: Quét lỗ hổng bảo mật (Trivy) & Chống lộ secret (Gitleaks) | [LAB-03](docs/LAB-03-SECURITY-SCANNING.md) |
| **Lab 04** | Continuous Delivery & Chiến lược Zero-Downtime Deployment | [LAB-04](docs/LAB-04-CD-DEPLOYMENT.md) |

---

## ⚡ Bắt đầu nhanh trên Local

```bash
# 1. Chạy toàn bộ hệ thống bằng Docker Compose:
docker compose -f deployments/docker-compose/docker-compose.prod.yml up -d --build

# 2. Kiểm tra các dịch vụ:
curl http://localhost:8000/health   # Backend API
curl http://localhost:3000/health   # Frontend Web UI

# 3. Mở trình duyệt:
# http://localhost:3000
```
