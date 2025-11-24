# Codeforces 题库爬虫与 Web UI

## 功能

- 爬取 Codeforces 题库数据（题目列表、难度、标签、通过人数）
- 按标签分类浏览题目的 Web UI
- 自动更新题库

## 使用方法

### 1. 初次爬取题库

```bash
uv run codeforces_scraper.py
```

### 2. 启动 Web UI

```bash
uv run app.py
```

访问 http://127.0.0.1:5000

### 3. 自动更新题库（Ubuntu/Linux）

编辑 `update.sh`，修改路径为实际路径：

```bash
#!/bin/bash
cd /path/to/cf
uv run update_problems.py >> update.log 2>&1
```

添加执行权限：

```bash
chmod +x /path/to/cf/update.sh
```

设置 cron 任务：

```bash
crontab -e
```

添加以下行（每天凌晨 2 点更新）：

```
0 2 * * * /path/to/cf/update.sh
```

或每 6 小时更新一次：

```
0 */6 * * * /path/to/cf/update.sh
```

查看更新日志：

```bash
cat /path/to/cf/update.log
```

## 文件说明

- `codeforces_scraper.py` - 初次爬取题库
- `update_problems.py` - 增量更新题库
- `app.py` - Flask Web 应用
- `templates/index.html` - Web UI 界面
- `codeforces_problems.json` - 题库数据
