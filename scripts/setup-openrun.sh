#!/usr/bin/env bash
# =============================================================================
# FinVision — OpenRun Server Bootstrap Script
# Run this ONCE on a fresh Linux VPS (Ubuntu 22.04 / Debian 12 recommended).
# Minimum spec: 1 vCPU, 1 GB RAM (2 GB recommended for Docker builds)
# =============================================================================
set -euo pipefail

OPENRUN_VERSION="latest"   # pin to e.g. "v0.4.1" for reproducibility
APP_HOST="https://finvision-api.yourdomain.com"   # ← CHANGE THIS
GITHUB_REPO="your-github-username/FinVision"      # ← CHANGE THIS
GITHUB_TOKEN="${GITHUB_TOKEN:-}"                   # set in env or edit below

# --- 1. Install Docker ---
echo ">>> Installing Docker..."
apt-get update -y
apt-get install -y ca-certificates curl gnupg lsb-release
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
  | tee /etc/apt/sources.list.d/docker.list
apt-get update -y
apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
systemctl enable docker && systemctl start docker

# --- 2. Install OpenRun (Clace) binary ---
echo ">>> Installing OpenRun..."
curl -fsSL https://raw.githubusercontent.com/claceio/clace/main/utils/install.sh | bash
export PATH="$HOME/.clace/bin:$PATH"
echo 'export PATH="$HOME/.clace/bin:$PATH"' >> ~/.bashrc

# --- 3. Generate admin password and configure OpenRun ---
ADMIN_PASS=$(openssl rand -base64 24)
echo "Admin password: $ADMIN_PASS" >> ~/openrun-credentials.txt
chmod 600 ~/openrun-credentials.txt

mkdir -p ~/.clace
cat > ~/.clace/clace.toml <<EOF
[security]
admin_password = "$ADMIN_PASS"

[system]
app_server_port = 9090
enable_https = true
https_port = 443
# Free TLS via Let's Encrypt
letsencrypt_email = "admin@yourdomain.com"   # ← CHANGE THIS

[metadata]
db_connection = "sqlite:/var/lib/clace/clace.db"
EOF

# --- 4. Start OpenRun as a systemd service ---
cat > /etc/systemd/system/openrun.service <<EOF
[Unit]
Description=OpenRun (Clace) Application Server
After=network.target docker.service
Requires=docker.service

[Service]
User=root
ExecStart=$HOME/.clace/bin/clace server start
Restart=always
RestartSec=5
Environment="PATH=$HOME/.clace/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable openrun
systemctl start openrun

echo ">>> OpenRun server started. Waiting 5s for readiness..."
sleep 5

# --- 5. Register FinVision backend app ---
# Tells OpenRun to watch the GitHub repo and build/run the container.
clace app create \
  --auth=system \
  --git-url "https://github.com/${GITHUB_REPO}" \
  --git-token "$GITHUB_TOKEN" \
  --branch main \
  --source-path ./backend \
  "${APP_HOST}/api"

echo ""
echo "============================================================"
echo " ✅ OpenRun setup complete!"
echo "    Backend URL:   ${APP_HOST}/api"
echo "    Admin console: ${APP_HOST}:9090/_clace"
echo "    Credentials:   ~/openrun-credentials.txt"
echo "============================================================"
echo ""
echo "NEXT: Set environment variables (secrets) for the backend:"
echo "  clace param set /api FIREBASE_SERVICE_ACCOUNT_JSON '<json>'"
echo "  clace param set /api FINNHUB_API_KEY_1 '<key>'"
echo "  clace param set /api FINNHUB_API_KEY_2 '<key>'"
echo "  clace param set /api FINNHUB_API_KEY_3 '<key>'"
echo "  clace param set /api FINNHUB_API_KEY_4 '<key>'"
echo "  clace param set /api FINNHUB_API_KEY_5 '<key>'"
echo "  clace param set /api POLYGON_API_KEY_1 '<key>'"
echo "  clace param set /api POLYGON_API_KEY_2 '<key>'"
echo "  clace param set /api POLYGON_API_KEY_3 '<key>'"
echo "  clace param set /api REDDIT_USERNAME '<username>'"
echo "  clace param set /api REDDIT_CLIENT_ID '<id>'"
echo "  clace param set /api REDDIT_CLIENT_SECRET '<secret>'"
echo "  clace param set /api ALLOWED_ORIGINS 'https://finvision.vercel.app'"
echo ""
echo "Then reload: clace app reload /api"
