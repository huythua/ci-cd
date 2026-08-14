# ⚙️ LAB 02: Xây dựng Pipeline CI với GitHub Actions

## 🎯 Mục tiêu bài học
1. Hiểu vòng đời của một CI Pipeline chuẩn doanh nghiệp: `Trigger -> Lint -> Unit Test -> Build -> Push`.
2. Sử dụng **Matrix Strategy** để chạy song song nhiều microservice trên nhiều job độc lập.
3. Tích hợp **Docker Buildx** & GitHub Actions Cache (`type=gha`) để giảm thời gian build từ 5 phút xuống 20 giây.
4. Tự động gắn nhãn version theo Git Tag (SemVer) và Commit SHA.

---

## 🏗️ 1. Cấu trúc Pipeline CI

File workflow: [.github/workflows/01-ci-test-lint.yml](file:///home/huythua/Code/devops-cicd-lab/.github/workflows/01-ci-test-lint.yml)

### A. Linter & Static Analysis (Flake8 / ESLint)
- Phát hiện sớm lỗi cú pháp, biến chưa sử dụng, nguy cơ bảo mật trước khi tốn tài nguyên build Docker.

### B. Automated Testing & Code Coverage
- Chạy toàn bộ test suites (`pytest`, `npm test`).
- Xuất file báo cáo coverage (`coverage.xml`) và upload artifact.

---

## ⚡ 2. Tối ưu tốc độ Build với GitHub Actions Cache

File workflow: [.github/workflows/02-docker-build-push.yml](file:///home/huythua/Code/devops-cicd-lab/.github/workflows/02-docker-build-push.yml)

Thay vì tải lại toàn bộ Docker base image và dependencies trên mỗi lần commit:
```yaml
cache-from: type=gha,scope=${{ matrix.service.name }}
cache-to: type=gha,mode=max,scope=${{ matrix.service.name }}
```
- **`cache-from: type=gha`**: Lấy các layers đã build từ cache server của GitHub.
- **`cache-to: type=gha,mode=max`**: Cache tất cả các layers (kể cả intermediate layers từ multi-stage build).

---

## 🏷️ 3. Chiến lược gắn thẻ Image Tag (Docker Tagging Strategy)
- `sha-<git-commit-sha>`: Dùng cho Dev/Staging để truy vết chính xác commit nào đang chạy.
- `latest`: Tự động cập nhật khi merge vào branch `main`.
- `v1.2.3`: Tự động tạo khi bạn tạo Git Release / Tag (`git tag v1.0.0 && git push origin v1.0.0`).
