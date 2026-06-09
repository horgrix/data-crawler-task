# Ubuntu 部署脚本

```shell
#!/bin/bash
# ============================================================
# data-crawler-task - Ubuntu 部署脚本
# 功能：代码拉取、配置文件生成、虚拟环境创建、依赖安装、
#       systemd 服务部署
# 用法：chmod +x deploy.sh && ./deploy.sh
# ============================================================
set -e  # 遇到错误立即退出

# ==================== 配置变量 ====================
PROJECT_DIR="/home/ubuntu/projects/data-crawler-task"
REPO_URL="https://github.com/horgrix/data-crawler-task.git"

# ==================== DB 环境变量（从外部传入，或使用默认值） ====================
# 用法示例：DB_PASSWORD=xxx ./deploy.sh
DB_HOST="${DB_HOST}"
DB_PORT="${DB_PORT}"
DB_USER="${DB_USER}"
DB_PASSWORD="${DB_PASSWORD}"
DB_DATABASE="${DB_DATABASE}"
DB_CHARSET="${DB_CHARSET}"

echo "=============================================="
echo "  data-crawler-task 部署脚本开始执行"
echo "  时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "=============================================="
# ==================== 1. 拉取代码 ====================
echo ""
echo "[1/5] 拉取最新代码..."
if [ -d "$PROJECT_DIR" ]; then
    echo "项目目录已存在，执行 git pull..."
    cd "$PROJECT_DIR"
    git pull origin master
else
    echo "克隆项目仓库..."
    mkdir -p "$(dirname "$PROJECT_DIR")"
    git clone "$REPO_URL" "$PROJECT_DIR"
    cd "$PROJECT_DIR"
fi
echo "代码拉取完成！当前目录: $(pwd)"

# ==================== 2. 部署 task 模块 ====================
echo ""
echo "[2/5] 部署 task 模块..."

cd "$PROJECT_DIR"

# 2.1 创建 xd.env 配置文件
echo "生成 xd.env 配置文件..."
cat > xd.env << ENVEOF

#Steam Region
STEAM_CRAWLER_XD_GAMES_REGIONS=global,CN,DK,RU,CA,TW,TR,AT,BR,DE,IT,NO,CZ,SG,NZ,JP,BE,FR,PL,TH,AU,SE,CH,US,FI,GB,NL,ES,KR,HK
STEAM_CRAWLER_XD_GAMES_REGIONS_NAMES=全球,中国,丹麦,俄罗斯,加拿大,中国台湾,土耳其,奥地利,巴西,德国,意大利,挪威,捷克,新加坡,新西兰,日本,比利时,法国,波兰,泰国,澳大利亚,瑞典,瑞士,美国,芬兰,英国,荷兰,西班牙,韩国,中国香港
STEAM_CRAWLER_XD_GAMES_IDS=1974050,2315040,4025700
STEAM_CRAWLER_XD_GAMES_NAMES=Torchlight: Infinite,火炬之光:无限,Heartopia
ENVEOF
echo "xd.env 配置文件已创建"
# 2.2 创建 Python 虚拟环境并安装依赖
if [ ! -d ".venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv .venv
fi
echo "激活虚拟环境并安装依赖..."
. ./.venv/bin/activate
# 如果 requirements.txt 不存在则写入依赖
if [ ! -f "requirements.txt" ]; then
    echo "requirements.txt 不存在，正在生成..."
    cat > requirements.txt << 'REQEOF'
APScheduler==3.10.4
python-dotenv==1.0.1
PyMySQL==1.1.1
selenium==4.27.1
beautifulsoup4==4.12.3
requests==2.32.3
sqlalchemy>=2.0.0
REQEOF
fi
pip install -r requirements.txt --quiet
deactivate
echo "依赖安装完成"
# 2.3 停止旧服务
echo "停止 data-crawler-task.service（如果存在）..."
sudo systemctl stop data-crawler-task.service 2>/dev/null || echo "data-crawler-task.service 未在运行"

# 2.4 创建 systemd 服务文件
echo "创建 data-crawler-task.service..."
sudo tee /etc/systemd/system/data-crawler-task.service > /dev/null << SERVICEEOF
[Unit]
Description=data-crawler-task - Scheduler
After=network.target mysql.service

[Service]
Type=simple
User=ubuntu
WorkingDirectory=$PROJECT_DIR
ExecStart=$PROJECT_DIR/.venv/bin/python3 $PROJECT_DIR/main.py
Restart=always
RestartSec=10
StandardOutput=append:$PROJECT_DIR/log/data-crawler-task.log
StandardError=append:$PROJECT_DIR/log/data-crawler-task_error.log

[Install]
WantedBy=multi-user.target
SERVICEEOF
echo "data-crawler-task.service 已创建"

# ==================== 3. 重载 systemd 守护进程 ====================
echo ""
echo "[3/5] 重载 systemd 守护进程..."
sudo systemctl daemon-reload

# ==================== 4. 启动服务 ====================
echo ""
echo "[4/5] 启动应用服务..."

echo "启动 data-crawler-task.service..."
sudo systemctl enable data-crawler-task.service
sudo systemctl start data-crawler-task.service
echo "data-crawler-task.service 状态:"
sudo systemctl status data-crawler-task.service --no-pager --lines=10

# ==================== 5. 部署完成 ====================
echo ""
echo "[5/5] =============================================="
echo "  ✅ data-crawler-task 部署完成！"
echo "  时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""
echo "  项目目录:  $PROJECT_DIR"
echo ""
echo "  服务状态检查命令:"
echo "    sudo systemctl status data-crawler-task.service"
echo ""
echo "  日志查看命令:"
echo "    tail -f $PROJECT_DIR/data-crawler-task.log"
echo ""
echo "  重启命令:"
echo "    sudo systemctl restart data-crawler-task.service"
echo "=============================================="
```