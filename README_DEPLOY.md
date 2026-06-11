部署說明 — 部署 `rms_upload` Streamlit 應用

選項概要：
- Docker（通用）: 建立容器後可部署到 Render, Fly.io, Azure App Service, AWS ECS 等。
- Render: 簡單上傳 Dockerfile 或 GitHub 連動。
- Fly.io: 支援建立輕量 VM，適合快速部署 Python 應用。

建立 Docker 映像並在本機測試

```bash
# 在專案根目錄
docker build -t rms_upload:latest .
docker run -p 8501:8501 rms_upload:latest
# 然後在瀏覽器開啟 http://localhost:8501
```

部署到 Render（Docker）

1. 將程式碼 push 到 GitHub。
2. 在 Render 建立一個新的 Web Service，連結到該 repo。
3. 選擇 "Docker"，Render 會自動使用專案根目錄的 `Dockerfile` 建構並部署。

部署到 Fly.io

1. 安裝 flyctl 並登入： `brew install flyctl` / 下載 Windows 版。
2. 初始化：
```bash
fly launch --name rms-upload --dockerfile Dockerfile
fly deploy
```

注意事項
- 如果要讓資料庫（`hotel_rms.db`）在雲端長期存放，請考慮使用雲端資料庫或將 DB 置於可持久化存儲 (e.g., volume, managed DB)。
- 若多個使用者會同時操作，SQLite 可能成為瓶頸，建議改為 Postgres 或其他 RDBMS。
- 設定防火牆、環境變數、及機密（如 API keys）時，使用平台提供的 Secrets/Env 功能。

需要我幫你：
- 1) 直接產生 Docker 映像並推到 Docker Hub（需你提供帳號授權/登入），或
- 2) 幫你走 Render/Fly.io 的部署步驟（需要 GitHub repo 權限或把 repo push 至遠端），或
- 3) 幫你把資料庫切換到 Postgres 並更新程式（較大改動）。

回覆你要的選項，我就繼續執行下一步。
