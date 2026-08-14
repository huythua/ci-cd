# 🚀 LAB 06: Chiến lược Triển khai Nâng cao & Quản lý Database Migration

## 🎯 Mục tiêu bài học
1. Phân biệt và lựa chọn đúng giữa **Rolling Update**, **Blue-Green Deployment**, và **Canary Releases**.
2. Nắm vững kỹ thuật **Expand and Contract (Parallel Run)** để di chuyển cấu trúc Database mà không gây Downtime hoặc lỗi 500 cho người dùng.
3. Tích hợp **ChatOps & Thông báo Tự động** (Telegram/Slack/Teams) vào cuối mỗi chu trình CI/CD.

---

## 🏗️ 1. Cấu hình Canary Release bằng Nginx Ingress trên Kubernetes

Với Kubernetes Nginx Ingress, bạn có thể định tuyến 10% lưu lượng truy cập của người dùng sang bản thử nghiệm mới (Canary) thông qua annotation:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: backend-canary
  annotations:
    nginx.ingress.kubernetes.io/canary: "true"
    nginx.ingress.kubernetes.io/canary-weight: "10" # 10% lưu lượng vào bản mới
spec:
  ingressClassName: nginx
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: devops-backend-canary
                port:
                  number: 8000
```

---

## 🗄️ 2. Quy tắc vàng Database Migration trong CI/CD

| Hành động | Cách làm SAI ❌ | Cách làm ĐÚNG (Zero-Downtime) ✅ |
| :--- | :--- | :--- |
| **Đổi tên cột** | `ALTER TABLE users RENAME COLUMN a TO b;` | **Bước 1**: Tạo cột mới `b`. **Bước 2**: Code đọc ghi cả `a` và `b`. **Bước 3**: Xóa cột `a` sau 1 tuần. |
| **Thêm ràng buộc NOT NULL** | `ALTER TABLE users ADD COLUMN phone VARCHAR NOT NULL;` (Lỗi sập insert ngay) | **Bước 1**: Thêm cột với `DEFAULT` hoặc cho phép `NULL`. **Bước 2**: Backfill dữ liệu cũ. **Bước 3**: Set NOT NULL. |
| **Xóa bảng cũ** | Drop table ngay trong ngày deploy | Đổi tên thành `_deprecated_users`, chờ 1-2 sprint kiểm tra log xem còn service nào gọi không rồi mới DROP. |

---

## 📢 3. Tích hợp ChatOps & Webhook thông báo

Workflow mẫu: [`.github/workflows/05-notify-telegram-slack.yml`](file:///home/huythua/Code/devops-cicd-lab/.github/workflows/05-notify-telegram-slack.yml)

- Khi Pipeline Deploy thành công hoặc thất bại:
  - Tự động lấy Commit SHA, Author, Branch, Status.
  - Bắn tin nhắn về Group Telegram/Slack của đội dự án kèm link trực tiếp để xem lỗi.
