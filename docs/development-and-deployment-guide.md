# CUI 开发与部署完整指南

本指南涵盖从本地开发到生产环境部署的完整流程。

---

## 📋 目录

- [本地开发](#本地开发)
  - [环境准备](#环境准备)
  - [项目设置](#项目设置)
  - [开发流程](#开发流程)
  - [测试](#测试)
  - [调试技巧](#调试技巧)
- [云端部署](#云端部署)
  - [部署前准备](#部署前准备)
  - [Railway 部署](#railway-部署推荐)
  - [Render 部署](#render-部署)
  - [Flyio 部署](#flyio-部署)
  - [VPS 部署](#vps-部署详细)
- [生产环境配置](#生产环境配置)
- [监控与维护](#监控与维护)
- [常见问题](#常见问题)

---

## 本地开发

### 环境准备

#### 1. 系统要求

```bash
# Node.js 版本
node --version  # 需要 >= 20.19.0

# 检查 npm
npm --version   # 应该 >= 10.0.0

# 操作系统
macOS / Linux / Windows (WSL2)
```

#### 2. 安装必要工具

```bash
# macOS
brew install node@20
brew install git

# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs git

# Windows (使用 WSL2)
# 先安装 WSL2, 然后在 WSL2 中安装 Node.js
```

#### 3. 安装 Claude CLI (可选,用于真实测试)

```bash
# 安装 Claude Code
npm install -g @anthropic-ai/claude-code

# 验证安装
claude --version

# 登录 (如果需要)
claude auth login
```

---

### 项目设置

#### 1. 克隆项目

```bash
# 克隆仓库
git clone https://github.com/bmpixel/cui.git
cd cui

# 查看项目结构
tree -L 2 -I node_modules
```

#### 2. 安装依赖

```bash
# 使用 npm ci (推荐,更可靠)
npm ci

# 或者使用 npm install
npm install

# 验证安装
npm list --depth=0
```

#### 3. 配置环境变量 (可选)

创建 `.env.development` 文件:

```bash
# .env.development

# Anthropic API Key (如果不使用 Claude CLI 登录)
ANTHROPIC_API_KEY=sk-ant-...

# Gemini API Key (用于语音识别功能)
GOOGLE_API_KEY=AIza...

# 日志级别
LOG_LEVEL=debug

# 服务器配置
PORT=3001
HOST=localhost
```

#### 4. 初始构建

```bash
# 首次构建 (必须!)
npm run build

# 这会:
# 1. 清理 dist 目录
# 2. 构建前端 (Vite)
# 3. 编译 TypeScript (tsc)
# 4. 处理路径别名 (tsc-alias)
# 5. 设置 MCP 服务器权限
```

---

### 开发流程

#### 1. 启动开发服务器

```bash
# 方式 1: 同时启动前后端 (推荐)
npm run dev

# 这会启动:
# - 后端 Express 服务器 (port 3001)
# - 前端 Vite 开发服务器 (内嵌)
# - 自动重载 (tsx watch)

# 访问
open http://localhost:3001/#your-token
```

```bash
# 方式 2: 分别启动前后端 (用于前端开发)

# 终端 1: 启动后端
npm run dev

# 终端 2: 启动前端 Vite 开发服务器
npm run dev:web

# 前端访问 http://localhost:3000
# 后端访问 http://localhost:3001
```

#### 2. 开发工作流

```bash
# 目录结构
cui/
├── src/
│   ├── server.ts              # 服务器入口
│   ├── cui-server.ts          # 核心服务器类
│   ├── routes/                # API 路由
│   ├── services/              # 业务逻辑
│   │   ├── claude-process-manager.ts   # Claude 进程管理
│   │   ├── stream-manager.ts           # 流管理
│   │   └── ...
│   ├── middleware/            # 中间件
│   ├── types/                 # TypeScript 类型
│   └── web/                   # 前端代码
│       ├── components/        # React 组件
│       ├── api/              # API 客户端
│       └── styles/           # 样式
├── tests/                     # 测试
├── dist/                      # 编译输出
└── public/                    # 静态资源
```

#### 3. 常用开发命令

```bash
# 类型检查 (不编译)
npm run typecheck

# 代码检查
npm run lint

# 修复 lint 错误
npx eslint src/**/*.ts --fix

# 运行测试
npm test

# 运行测试 (watch 模式)
npm run test:watch

# 运行测试 (带覆盖率)
npm run test:coverage

# 清理构建
npm run clean
```

#### 4. 热重载说明

```bash
# 后端 (tsx watch)
修改 src/**/*.ts → 自动重启服务器 (约 1-2 秒)

# 前端 (Vite HMR)
修改 src/web/**/*.tsx → 即时热更新 (毫秒级)
修改 src/web/**/*.css → 即时热更新 (毫秒级)
```

---

### 测试

#### 1. 运行测试

```bash
# 运行所有测试
npm test

# 只运行单元测试
npm run unit-tests

# 只运行集成测试
npm run integration-tests

# 运行特定测试文件
npm test -- claude-process-manager.test.ts

# 运行匹配特定名称的测试
npm test -- --testNamePattern="should start conversation"

# 调试模式 (显示详细日志)
npm run test:debug
```

#### 2. 测试覆盖率

```bash
# 生成覆盖率报告
npm run test:coverage

# 查看报告
open coverage/index.html

# 覆盖率要求:
# - Lines: 75%
# - Functions: 80%
# - Branches: 60%
# - Statements: 75%
```

#### 3. 测试工具

```bash
# Vitest UI (可视化测试界面)
npm run test:ui

# 在浏览器中打开
open http://localhost:51204/__vitest__/
```

---

### 调试技巧

#### 1. 启用调试日志

```bash
# 方式 1: 环境变量
LOG_LEVEL=debug npm run dev

# 方式 2: 修改代码
# src/services/logger.ts
const LOG_LEVEL = 'debug';

# 日志级别:
# - silent: 无输出
# - error: 只显示错误
# - warn: 警告和错误
# - info: 一般信息 (默认)
# - debug: 详细调试信息
```

#### 2. VS Code 调试配置

创建 `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug CUI Server",
      "type": "node",
      "request": "launch",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["run", "dev"],
      "skipFiles": ["<node_internals>/**"],
      "env": {
        "LOG_LEVEL": "debug"
      }
    },
    {
      "name": "Debug Tests",
      "type": "node",
      "request": "launch",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["test", "--", "--run"],
      "skipFiles": ["<node_internals>/**"],
      "env": {
        "NODE_ENV": "test",
        "LOG_LEVEL": "debug"
      }
    }
  ]
}
```

#### 3. 常见调试场景

```bash
# 查看 Claude CLI 命令
# 搜索日志中的 "SPAWNING CLAUDE COMMAND"
LOG_LEVEL=debug npm run dev | grep "SPAWNING"

# 查看流式输出
# 监控 StreamManager 的广播
LOG_LEVEL=debug npm run dev | grep "Broadcasting"

# 查看进程管理
# 监控进程的启动和关闭
LOG_LEVEL=debug npm run dev | grep "ClaudeProcessManager"

# 查看 HTTP 请求
# 所有 API 请求都会被记录
LOG_LEVEL=debug npm run dev | grep "RequestLogger"
```

#### 4. 使用 Mock Claude CLI

```bash
# 项目包含 Mock Claude CLI 用于测试
# 位置: tests/__mocks__/claude

# 手动测试 Mock CLI
./tests/__mocks__/claude -p chat "Hello"

# 在测试中使用
# 测试会自动使用 Mock CLI
```

---

## 云端部署

### 部署前准备

#### 1. 构建生产版本

```bash
# 完整构建
npm run build

# 验证构建产物
ls -la dist/
# 应该看到:
# - server.js (服务器入口)
# - cui-server.js (主服务器)
# - services/ (编译后的服务)
# - web/ (前端静态文件)
```

#### 2. 测试生产构建

```bash
# 本地测试生产版本
NODE_ENV=production node dist/server.js

# 访问
curl http://localhost:3001/health
# 应该返回: {"status":"ok"}
```

#### 3. 准备环境变量

创建环境变量清单:

```bash
# 必需
ANTHROPIC_API_KEY=sk-ant-...  # 或者使用 Claude CLI ��录

# 可选
GOOGLE_API_KEY=AIza...        # Gemini 语音识别
PORT=3001                     # 端口
HOST=0.0.0.0                 # 监听所有接口
NODE_ENV=production          # 生产模式
```

---

### Railway 部署 (推荐)

Railway 是最简单的部署方式,支持长期运行的进程。

#### 1. 安装 Railway CLI

```bash
# macOS
brew install railway

# Linux/Windows
npm install -g @railway/cli

# 验证安装
railway --version
```

#### 2. 登录 Railway

```bash
# 登录
railway login

# 浏览器会打开,完成 OAuth 登录
```

#### 3. 初始化项目

```bash
# 在项目目录中
cd cui

# 初始化 Railway 项目
railway init

# 选择:
# - Create new project
# - 输入项目名称: cui-server
```

#### 4. 配置环境变量

```bash
# 设置 API Key
railway variables set ANTHROPIC_API_KEY=sk-ant-...

# 设置其他变量
railway variables set GOOGLE_API_KEY=AIza...
railway variables set NODE_ENV=production

# 查看所有变量
railway variables
```

#### 5. 部署

```bash
# 第一次部署
railway up

# Railway 会:
# 1. 检测到 Node.js 项目
# 2. 运行 npm ci
# 3. 运行 npm run build
# 4. 运行 npm start

# 查看日志
railway logs

# 获取 URL
railway open
```

#### 6. 配置域名 (可选)

```bash
# 生成 Railway 域名
railway domain

# 或添加自定义域名
# 在 Railway Dashboard 中配置
```

#### 7. 持续部署

```bash
# 连接 GitHub 仓库
# 1. 在 Railway Dashboard 中
# 2. 选择 "Deploy from GitHub repo"
# 3. 每次 push 自动部署

# 或手动部署
git push origin main
railway up
```

#### 8. Railway 配置文件 (可选)

创建 `railway.json`:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "npm ci && npm run build"
  },
  "deploy": {
    "startCommand": "node dist/server.js",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

---

### Render 部署

Render 提供免费层,适合小型项目。

#### 1. 准备 Render 配置

创建 `render.yaml`:

```yaml
services:
  - type: web
    name: cui-server
    env: node
    region: oregon  # 或选择其他区域
    plan: free      # 或 starter ($7/月)
    buildCommand: npm ci && npm run build
    startCommand: node dist/server.js
    healthCheckPath: /health

    envVars:
      - key: NODE_ENV
        value: production
      - key: PORT
        value: 3001
      - key: HOST
        value: 0.0.0.0
      - key: ANTHROPIC_API_KEY
        sync: false  # 从 Dashboard 手动设置
      - key: GOOGLE_API_KEY
        sync: false

    # 持久化磁盘 (保存 ~/.claude 和 ~/.cui)
    disk:
      name: cui-data
      mountPath: /root
      sizeGB: 1
```

#### 2. 从 GitHub 部署

```bash
# 1. Push 代码到 GitHub
git push origin main

# 2. 访问 Render Dashboard
open https://dashboard.render.com

# 3. 点击 "New +" → "Blueprint"
# 4. 连接 GitHub 仓库
# 5. Render 会读取 render.yaml
# 6. 点击 "Apply" 开始部署
```

#### 3. 配置环境变量

```bash
# 在 Render Dashboard 中:
# 1. 选择你的服务
# 2. 进入 "Environment" 标签
# 3. 添加敏感信息:
#    - ANTHROPIC_API_KEY
#    - GOOGLE_API_KEY
# 4. 保存后自动重新部署
```

#### 4. 查看部署

```bash
# Render 会自动:
# - 运行构建命令
# - 启动服务
# - 提供 HTTPS URL

# 访问 URL (在 Dashboard 中找到)
https://cui-server.onrender.com
```

---

### Fly.io 部署

Fly.io 提供全球 CDN 和灵活的容器部署。

#### 1. 安装 Fly CLI

```bash
# macOS/Linux
curl -L https://fly.io/install.sh | sh

# 验证
flyctl version
```

#### 2. 登录

```bash
flyctl auth login
```

#### 3. 创建 Fly 应用

```bash
# 在项目目录
cd cui

# 初始化
flyctl launch

# 选择:
# - App name: cui-server (或留空自动生成)
# - Region: 选择最近的区域
# - PostgreSQL: No
# - Redis: No
```

这会创建 `fly.toml`:

```toml
app = "cui-server"
primary_region = "sjc"

[build]
  [build.args]
    NODE_VERSION = "20"

[env]
  NODE_ENV = "production"
  PORT = "8080"
  HOST = "0.0.0.0"

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = false
  auto_start_machines = true
  min_machines_running = 1

  [http_service.concurrency]
    type = "requests"
    hard_limit = 250
    soft_limit = 200

[[vm]]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 512

[checks]
  [checks.health]
    grace_period = "30s"
    interval = "15s"
    method = "get"
    path = "/health"
    port = 8080
    timeout = "10s"
    type = "http"
```

#### 4. 添加 Dockerfile

创建 `Dockerfile`:

```dockerfile
FROM node:20-alpine

WORKDIR /app

# 复制 package 文件
COPY package*.json ./

# 安装依赖
RUN npm ci --only=production

# 复制源代码
COPY . .

# 构建
RUN npm run build

# 暴露端口
EXPOSE 8080

# 启动
CMD ["node", "dist/server.js"]
```

#### 5. 配置密钥

```bash
# 设置环境变量
flyctl secrets set ANTHROPIC_API_KEY=sk-ant-...
flyctl secrets set GOOGLE_API_KEY=AIza...

# 查看密钥列表
flyctl secrets list
```

#### 6. 部署

```bash
# 部署
flyctl deploy

# 查看状态
flyctl status

# 查看日志
flyctl logs

# 打开应用
flyctl open
```

#### 7. 配置持久化卷 (保存数据)

```bash
# 创建卷
flyctl volumes create cui_data --size 1

# 修改 fly.toml,添加:
[mounts]
  source = "cui_data"
  destination = "/root"
```

---

### VPS 部署 (详细)

使用传统 VPS (如 DigitalOcean, Linode, Vultr) 提供最大控制权。

#### 1. 购买和设置 VPS

```bash
# 推荐配置:
# - 2 vCPU
# - 4 GB RAM
# - 80 GB SSD
# - Ubuntu 22.04 LTS

# 价格: 约 $12-20/月
```

#### 2. 初始服务器设置

```bash
# SSH 连接到服务器
ssh root@your-server-ip

# 更新系统
apt update && apt upgrade -y

# 创建非 root 用户
adduser cui
usermod -aG sudo cui

# 配置 SSH key (在本地)
ssh-copy-id cui@your-server-ip

# 切换到新用户
su - cui
```

#### 3. 安装依赖

```bash
# 安装 Node.js 20
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# 验证
node --version  # v20.x.x
npm --version

# 安装其他工具
sudo apt-get install -y git build-essential
```

#### 4. 部署应用

```bash
# 克隆项目
cd ~
git clone https://github.com/bmpixel/cui.git
cd cui

# 安装依赖
npm ci

# 构建
npm run build

# 配置环境变量
cat > .env.production << EOF
NODE_ENV=production
PORT=3001
HOST=0.0.0.0
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=AIza...
EOF

# 测试运行
node dist/server.js
```

#### 5. 使用 PM2 管理进程

```bash
# 安装 PM2
sudo npm install -g pm2

# 启动应用
pm2 start dist/server.js --name cui-server

# 查看状态
pm2 status

# 查看日志
pm2 logs cui-server

# 监控
pm2 monit

# 设置开机自启
pm2 startup
pm2 save

# 重启应用
pm2 restart cui-server

# 停止应用
pm2 stop cui-server
```

#### 6. 配置 Nginx 反向代理

```bash
# 安装 Nginx
sudo apt-get install -y nginx

# 创建配置文件
sudo nano /etc/nginx/sites-available/cui

# 粘贴配置:
```

```nginx
server {
    listen 80;
    server_name your-domain.com;  # 替换为你的域名

    # 客户端最大上传大小
    client_max_body_size 50M;

    location / {
        proxy_pass http://localhost:3001;
        proxy_http_version 1.1;

        # WebSocket 支持
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';

        # 必需的 headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # 流式传输配置 (非常重要!)
        proxy_buffering off;
        proxy_cache off;
        proxy_read_timeout 3600s;
        proxy_send_timeout 3600s;

        # 缓存控制
        proxy_cache_bypass $http_upgrade;
    }
}
```

```bash
# 启用配置
sudo ln -s /etc/nginx/sites-available/cui /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重启 Nginx
sudo systemctl restart nginx

# 设置开机自启
sudo systemctl enable nginx
```

#### 7. 配置 SSL (HTTPS)

```bash
# 安装 Certbot
sudo apt-get install -y certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d your-domain.com

# Certbot 会自动:
# 1. 获取 Let's Encrypt 证书
# 2. 修改 Nginx 配置
# 3. 设置自动续期

# 测试自动续期
sudo certbot renew --dry-run

# 查看证书
sudo certbot certificates
```

#### 8. 配置防火墙

```bash
# 启用 UFW
sudo ufw enable

# 允许 SSH
sudo ufw allow 22/tcp

# 允许 HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# 查看状态
sudo ufw status

# 应该看到:
# 22/tcp   ALLOW   Anywhere
# 80/tcp   ALLOW   Anywhere
# 443/tcp  ALLOW   Anywhere
```

#### 9. 自动部署脚本

创建 `~/cui/deploy.sh`:

```bash
#!/bin/bash

echo "🚀 Starting deployment..."

# 切换到项目目录
cd ~/cui

# 停止应用
echo "⏸️  Stopping application..."
pm2 stop cui-server

# 拉取最新代码
echo "📥 Pulling latest code..."
git pull origin main

# 安装依赖
echo "📦 Installing dependencies..."
npm ci

# 构建
echo "🔨 Building application..."
npm run build

# 重启应用
echo "▶️  Starting application..."
pm2 restart cui-server

# 保存 PM2 配置
pm2 save

echo "✅ Deployment complete!"
echo "📊 Application status:"
pm2 status

echo "📝 Recent logs:"
pm2 logs cui-server --lines 20
```

```bash
# 设置执行权限
chmod +x ~/cui/deploy.sh

# 使用
~/cui/deploy.sh
```

---

## 生产环境配置

### 1. 配置文件位置

```bash
# CUI 配置目录
~/.cui/
├── config.json         # 服务器配置
├── session-info.db     # 会话数据库
└── logs/              # 日志文件 (如果配置了)

# Claude CLI 数据
~/.claude/
├── sessions/          # 对话历史
└── auth/             # 认证信息
```

### 2. 配置 config.json

```bash
# 编辑配置
nano ~/.cui/config.json
```

```json
{
  "server": {
    "host": "0.0.0.0",
    "port": 3001
  },
  "auth": {
    "token": "your-secure-random-token-here-min-32-chars"
  },
  "notifications": {
    "ntfy": {
      "enabled": false,
      "topic": "your-topic"
    },
    "webPush": {
      "enabled": false
    }
  },
  "dictation": {
    "enabled": true,
    "provider": "gemini"
  }
}
```

### 3. 生成安全的 Auth Token

```bash
# 方法 1: 使用 OpenSSL
openssl rand -hex 32

# 方法 2: 使用 Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"

# 结果示例:
# a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6
```

### 4. 配置通知 (可选)

#### Ntfy 通知

```bash
# 1. 访问 https://ntfy.sh
# 2. 创建一个 topic (随机名称)
# 3. 在手机安装 ntfy app
# 4. 订阅你的 topic

# 配置
{
  "notifications": {
    "ntfy": {
      "enabled": true,
      "topic": "cui_notifications_a1b2c3d4",
      "server": "https://ntfy.sh"
    }
  }
}
```

#### Web Push 通知

```bash
# CUI 会自动生成 VAPID keys
# 在 Web UI 的 Settings 中启用
```

---

## 监控与维护

### 1. 健康检查

```bash
# 检查服务状态
curl https://your-domain.com/health

# 应该返回:
{
  "status": "ok",
  "timestamp": "2025-01-20T10:00:00.000Z",
  "uptime": 3600
}
```

### 2. 日志管理

```bash
# PM2 日志
pm2 logs cui-server --lines 100

# 清理日志
pm2 flush cui-server

# 设置日志轮转
pm2 install pm2-logrotate
pm2 set pm2-logrotate:max_size 10M
pm2 set pm2-logrotate:retain 7
```

### 3. 性能监控

```bash
# 使用 PM2 监控
pm2 monit

# 安装 PM2 Plus (高级监控)
pm2 link your-secret-key your-public-key

# 访问 https://app.pm2.io
```

### 4. 备份

```bash
# 创建备份脚本
cat > ~/backup-cui.sh << 'EOF'
#!/bin/bash

BACKUP_DIR=~/cui-backups
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="cui_backup_$DATE.tar.gz"

# 创建备份目录
mkdir -p $BACKUP_DIR

# 备份
tar -czf $BACKUP_DIR/$BACKUP_FILE \
  ~/.cui \
  ~/.claude \
  ~/cui/dist \
  ~/cui/.env.production

echo "Backup created: $BACKUP_FILE"

# 只保留最近 7 天的备份
find $BACKUP_DIR -name "cui_backup_*.tar.gz" -mtime +7 -delete
EOF

chmod +x ~/backup-cui.sh

# 设置定时任务
crontab -e

# 添加:
0 2 * * * ~/backup-cui.sh  # 每天凌晨 2 点备份
```

### 5. 更新应用

```bash
# 方法 1: 使用部署脚本
~/cui/deploy.sh

# 方法 2: 手动更新
cd ~/cui
git pull origin main
npm ci
npm run build
pm2 restart cui-server
```

---

## 常见问题

### 1. 端口已被占用

```bash
# 查看占用端口的进程
sudo lsof -i :3001

# 杀死进程
sudo kill -9 <PID>

# 或更改配置中的端口
```

### 2. Claude CLI 未找到

```bash
# 确认安装
which claude

# 如果未安装
npm install -g @anthropic-ai/claude-code

# 验证
claude --version
```

### 3. 内存不足

```bash
# 检查内存使用
free -h

# 增加 Node.js 内存限制
NODE_OPTIONS="--max-old-space-size=4096" node dist/server.js

# 或在 PM2 中:
pm2 start dist/server.js --name cui-server --node-args="--max-old-space-size=4096"
```

### 4. 流式响应中断

```bash
# 检查 Nginx 配置
# 确保有这些配置:
proxy_buffering off;
proxy_cache off;
proxy_read_timeout 3600s;

# 重启 Nginx
sudo systemctl restart nginx
```

### 5. HTTPS 证书问题

```bash
# 手动续期
sudo certbot renew

# 强制续期
sudo certbot renew --force-renewal

# 查看证书状态
sudo certbot certificates
```

### 6. 权限问题

```bash
# 确保目录权限正确
chmod 755 ~
chmod 755 ~/.cui
chmod 755 ~/.claude

# 确保 PM2 以正确用户运行
pm2 whoami
```

### 7. 数据库锁定

```bash
# 停止应用
pm2 stop cui-server

# 删除数据库锁
rm -f ~/.cui/session-info.db-*

# 重启应用
pm2 start cui-server
```

---

## 性能优化

### 1. Node.js 优化

```bash
# 使用生产模式
NODE_ENV=production

# 优化垃圾回收
NODE_OPTIONS="--max-old-space-size=4096 --gc-interval=100"

# 启用 CPU profiling (调试用)
NODE_OPTIONS="--prof"
```

### 2. Nginx 缓存

```nginx
# 静态资源缓存
location /assets {
    expires 1y;
    add_header Cache-Control "public, immutable";
}

location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 30d;
    add_header Cache-Control "public, no-transform";
}
```

### 3. 并发限制

```typescript
// 在 cui-server.ts 中限制并发对话数
const MAX_CONCURRENT_CONVERSATIONS = 20;
```

---

## 安全最佳实践

### 1. 使用强 Token

```bash
# 至少 32 字节的随机字符串
openssl rand -hex 32
```

### 2. 限制 IP 访问 (如果需要)

```nginx
# 在 Nginx 中
location / {
    allow 192.168.1.0/24;  # 允许内网
    allow 1.2.3.4;         # 允许特定 IP
    deny all;              # 拒绝其他

    proxy_pass http://localhost:3001;
}
```

### 3. 速率限制

```nginx
# 在 Nginx 中添加
limit_req_zone $binary_remote_addr zone=cui_limit:10m rate=10r/s;

location / {
    limit_req zone=cui_limit burst=20 nodelay;
    proxy_pass http://localhost:3001;
}
```

### 4. 定期更新

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 更新 Node.js 依赖
cd ~/cui
npm audit
npm audit fix

# 更新 Claude CLI
npm update -g @anthropic-ai/claude-code
```

---

## 总结

### 本地开发清单

- ✅ Node.js >= 20.19.0
- ✅ 克隆项目
- ✅ npm ci
- ✅ npm run build
- ✅ npm run dev
- ✅ 访问 http://localhost:3001

### 云端部署清单

- ✅ 选择平台 (Railway/Render/Fly/VPS)
- ✅ 配置环境变量
- ✅ npm run build
- ✅ 配置域名和 HTTPS
- ✅ 设置监控和备份
- ✅ 测试健康检查

### 快速参考

```bash
# 开发
npm run dev              # 启动开发服务器
npm test                # 运行测试
npm run typecheck       # 类型检查

# 构建
npm run build           # 生产构建
npm start               # 启动生产服务器

# 部署 (Railway)
railway up              # 部署到 Railway
railway logs            # 查看日志

# 维护 (VPS)
pm2 status              # 查看状态
pm2 logs cui-server     # 查看日志
pm2 restart cui-server  # 重启应用
~/cui/deploy.sh         # 自动部署
```

---

## 获取帮助

- 📖 项目文档: [docs/](.)
- 🐛 报告问题: [GitHub Issues](https://github.com/bmpixel/cui/issues)
- 💬 讨论: [GitHub Discussions](https://github.com/bmpixel/cui/discussions)
- 📚 Claude Code 文档: [docs.claude.com](https://docs.claude.com/claude-code)

---

**祝你部署顺利!** 🚀
