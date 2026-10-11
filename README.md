# AI 广告增长优化助手

React + FastAPI 网页，使用现有广告模型和数据。

## 启动

双击 `启动新版网页.cmd`。脚本启动本地服务并打开 http://127.0.0.1:5173/ 。电脑重启后重新双击即可。

前端：React、TypeScript、Vite、Tailwind CSS、Framer Motion、Lucide、Recharts。
后端：FastAPI，复用 `D:\PYTHON-project\APO-cdr\ad_growth_web\modeling.py` 与 `data_io.py`。
默认数据：`D:\PYTHON-project\APO-cdr\data\beauty_ad_campaign_5000.csv`。
可通过环境变量 `AD_GROWTH_SOURCE` 指定已有项目位置。原 Streamlit 项目保留。

## 安装与手动运行

```powershell
# 在项目根目录运行；已有 Python 环境安装过 EconML
& D:\PYTHON-project\APO-cdr\.venv\Scripts\python.exe -m pip install -r backend/requirements.txt
# 在有 npm 的环境下
cd frontend
npm install
npm run dev
# 另一个终端，在项目根目录
& D:\PYTHON-project\APO-cdr\.venv\Scripts\python.exe -m uvicorn main:app --app-dir backend --host 127.0.0.1 --port 8000
```

本机使用 Codex 自带 Node 与 pnpm；依赖已安装，日常使用双击启动脚本即可。

## 目录

- frontend/src/Hero.tsx：原视频 Hero 与进入工作台按钮。
- frontend/src/App.tsx：七个分析视图和数据交互。
- frontend/src/Charts.tsx：图表。
- frontend/src/theme.css：暖粉米白紫主题与响应式布局。
- frontend/src/api.ts：同源 API 请求。
- backend/main.py：数据校验、上传、异步训练、下载接口。
- start.ps1：后台启动脚本；日志在项目根目录。

这是单机 Demo：上传的数据在进程内使用，服务重启恢复默认数据。训练结果按数据指纹缓存。显示数值来自现有模型缓存或实际重新训练，不硬编码示例结论。
首屏视频和字体依赖网络；视频加载失败时显示渐变底色。减少动画偏好启用时不播放视频。
模型结果依赖识别假设，模拟数据不用于实际预算决策。训练集预测与留出集预测已标记；排序验证仅使用留出集。
