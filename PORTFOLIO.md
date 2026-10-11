# GitHub Pages 作品集展示版

使用预先计算的 5,000 条模拟用户数据，保留六个分析页面、人群筛选、名单搜索、分页及 CSV / 验证报告下载。不上传数据，不在线运行 Python 模型。默认本地开发模式仍连接原有后端。

在 frontend 目录用 pnpm 10 执行 pnpm install --frozen-lockfile，设置环境变量 VITE_PORTFOLIO_MODE=true、GITHUB_PAGES=true，执行 pnpm exec vite build。产物位于 frontend/dist/client，站点路径为 /AI-/。

GitHub 仓库 Settings → Pages 中选择 GitHub Actions。推送 main 后自动发布。

模拟数据位于 frontend/public/demo。本地分析服务运行时可执行 scripts/export_portfolio.py 更新。请勿导出真实个人或客户数据到公开仓库。

首页视频使用外部 CDN，网络不可用时回退到渐变背景。完整 Python 后端不由 GitHub Pages 托管。
