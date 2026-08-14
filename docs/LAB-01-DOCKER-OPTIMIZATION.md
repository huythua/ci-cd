# 🐳 LAB 01: Tối ưu hóa Dockerfile & Layer Caching

## 🎯 Mục tiêu bài học
1. Hiểu cơ chế hoạt động của Docker Layer Cache.
2. Áp dụng kỹ thuật **Multi-stage Build** để giảm kích thước image từ hàng GB xuống còn vài chục MB.
3. Cấu hình bảo mật Container bằng **Non-root user**.
4. Thiết lập **Healthcheck** chuẩn cho container orchestration.

---

## 🔍 1. Cơ chế Docker Cache & Sai lầm thường gặp

### ❌ Sai lầm (Cache bị phá vỡ liên tục):
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .                      # ⚠️ Mỗi khi sửa 1 dòng code, lệnh COPY này đổi hash
RUN pip install -r requirements.txt # ⚠️ Dẫn đến pip install bị chạy lại từ đầu!
```

### ✅ Chuẩn DevOps (Tách biệt dependency và source code):
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .       # ✅ Chỉ copy file định nghĩa thư viện trước
RUN pip install -r requirements.txt # ✅ Docker sẽ tận dụng Cache trừ khi requirements.txt thay đổi!
COPY ./app ./app             # ✅ Source code thay đổi chỉ làm build lại layer này (1 giây)
```

---

## 🛡️ 2. Multi-stage Build & Non-root User
Xem ví dụ hoàn chỉnh tại [Dockerfile Backend](file:///home/huythua/Code/devops-cicd-lab/apps/backend-api/Dockerfile):

- **Stage 1 (`builder`)**: Chứa `build-essential`, compilers để compile C-extensions của python/node.
- **Stage 2 (`runtime`)**: Image siêu nhẹ, chỉ copy kết quả nhị phân và thư viện đã build từ stage 1, loại bỏ toàn bộ compiler/rác thừa.
- **User `appuser` (UID 1001)**: Ngăn chặn kẻ tấn công chiếm quyền `root` của Host OS nếu ứng dụng bị dính RCE (Remote Code Execution).

---

## 🧪 Thực hành kiểm tra
Thử build image trên máy của bạn và kiểm tra dung lượng:

```bash
cd apps/backend-api
docker build -t devops-backend-api:v1 .
docker images | grep devops-backend-api
```
