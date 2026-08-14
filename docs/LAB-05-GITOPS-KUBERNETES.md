# 🚢 LAB 05: Kubernetes, Helm Chart & GitOps với ArgoCD

## 🎯 Mục tiêu bài học
1. Hiểu kiến trúc điều phối Container trong Kubernetes (Pods, Deployments, Services, Ingress, HPA).
2. Sử dụng **Helm Chart** để đóng gói và tham số hóa ứng dụng cho nhiều môi trường (`dev`, `uat`, `prod`).
3. Hiểu triết lý **GitOps**: Coi Git là nguồn chân lý duy nhất (Single Source of Truth) và sử dụng **ArgoCD** để đồng bộ tự động.

---

## 📦 1. Quản lý ứng dụng với Helm Chart

Thư mục Helm Chart: [`deployments/helm/devops-app/`](file:///home/huythua/Code/devops-cicd-lab/deployments/helm/devops-app/)

### Các lệnh Helm cơ bản cần nắm:

```bash
cd deployments/helm/devops-app

# 1. Kiểm tra cú pháp template (Lint):
helm lint .

# 2. Xem các file manifest K8s được sinh ra trước khi deploy:
helm template my-release . -f values.yaml

# 3. Deploy lên môi trường DEV:
helm upgrade --install dev-app . -f values.yaml --namespace dev --create-namespace

# 4. Deploy lên môi trường PRODUCTION (3 Replicas + Auto-scaling):
helm upgrade --install prod-app . -f values-production.yaml --namespace prod --create-namespace

# 5. Xem lịch sử các lần Release & Rollback:
helm history prod-app -n prod
helm rollback prod-app 1 -n prod   # Quay lại bản release số 1 trong 3 giây!
```

---

## 🔄 2. Mô hình GitOps với ArgoCD

### Tại sao các công ty lớn không dùng CI để chạy lệnh `kubectl` trực tiếp?
- **Nguy cơ bảo mật**: Phải cấp quyền Admin K8s (Kubeconfig) cho GitHub Runner.
- **Trôi cấu hình (Configuration Drift)**: Nếu ai đó sửa thủ công trên cluster, CI không hề biết.

### Giải pháp GitOps (ArgoCD):
1. **Pull-based Deployment**: ArgoCD Agent chạy **bên trong** K8s cluster, định kỳ kéo repo Git về.
2. **Auto-Sync & Self-Healing**: 
   - Khi repo Git có commit mới $\rightarrow$ ArgoCD tự động áp dụng (Sync).
   - Nếu ai đó cố tình sửa Pod/Service trên K8s $\rightarrow$ ArgoCD tự động ghi đè về đúng trạng thái khai báo trong Git!

```yaml
# Ví dụ Application Manifest của ArgoCD:
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: devops-microservices
  namespace: argocd
spec:
  project: default
  source:
    repoURL: 'https://github.com/huythua/ci-cd.git'
    targetRevision: main
    path: deployments/helm/devops-app
    helm:
      valueFiles:
        - values-production.yaml
  destination:
    server: 'https://kubernetes.default.svc'
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```
