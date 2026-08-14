# 🛡️ LAB 03: DevSecOps - Quét lỗ hổng & Chống rò rỉ Secrets

## 🎯 Mục tiêu bài học
1. Ngăn chặn triệt để việc vô tình commit Secret / API Key / Password vào Git repository với **Gitleaks**.
2. Quét lỗ hổng bảo mật (CVE) trong Container Image và OS Packages với **Aqua Security Trivy**.
3. Tích hợp Security Gates vào CI/CD (Fail build nếu có lỗ hổng mức độ `CRITICAL`).

---

## 🔍 1. Chống lộ Secrets với Gitleaks
Xem workflow: [.github/workflows/03-security-scan.yml](file:///home/huythua/Code/devops-cicd-lab/.github/workflows/03-security-scan.yml)

Gitleaks sử dụng regex & entropy để quét toàn bộ lịch sử git nhằm tìm:
- AWS Access Key, GCP Service Account keys.
- Database Connection Strings, JWT Secret Keys.
- Private SSH Keys.

---

## 🐳 2. Quét lỗ hổng Container với Trivy
Trivy phân tích các thành phần:
- **OS Packages**: Các lỗ hổng trong Debian/Alpine runtime (ví dụ `openssl`, `glibc`).
- **Application Dependencies**: Thư viện Python (`pip`), Node (`npm`) dính lỗ hổng đã được công bố trên NVD.

```bash
# Lệnh chạy thủ công bằng Docker:
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy:latest image --severity CRITICAL,HIGH devops-backend-api:v1
```
