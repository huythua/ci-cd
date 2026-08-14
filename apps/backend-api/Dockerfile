# ==========================================
# Stage 1: Build & Dependencies
# ==========================================
FROM python:3.11-slim AS builder

WORKDIR /build

# Cài đặt công cụ cần thiết cho build
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Tận dụng Docker layer cache: chỉ COPY requirements trước
COPY requirements.txt .

# Cài đặt packages vào thư mục wheel / site-packages độc lập
RUN pip install --no-cache-dir --user -r requirements.txt

# ==========================================
# Stage 2: Production Runtime (Tối ưu nhẹ & bảo mật)
# ==========================================
FROM python:3.11-slim AS runtime

# Tạo user không có quyền root (Non-root user)
RUN groupadd -g 1001 appgroup && \
    useradd -u 1001 -g appgroup -s /bin/bash -m appuser

WORKDIR /app

# Copy các python package đã build từ stage builder
COPY --from=builder /root/.local /home/appuser/.local

# Copy mã nguồn ứng dụng
COPY --chown=appuser:appgroup ./app /app/app

# Cập nhật biến môi trường PATH để appuser nhận được pip packages
ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

# Chuyển sang non-root user
USER appuser

# Healthcheck nội bộ cho container
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health').read()" || exit 1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
