# Doyouremember - 你的个人词汇助手

一个帮助你学习新词汇的网络应用，它可以生成包含释义、例句、音频发音和图片的单词卡片，并自动添加到 Anki 中。

## 功能特点

- 基于任何主题生成词汇
- 每个单词卡片包含：
  - 定义
  - 例句
  - 中文翻译
  - 同义词
  - 词源
  - 趣味知识
  - 音频发音
  - 相关图片

## 前置要求

1. Python 3.11 或更高版本
2. 安装了 AnkiConnect 插件的 Anki
3. 以下服务的 API 密钥：
   - Google Gemini API
   - Rime TTS API
   - Apify

## 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/Doyouremember.git
cd Doyouremember
```

2. 创建并激活虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Windows 系统使用：venv\Scripts\activate
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 设置环境变量：
```bash
cp .env.example .env
```
然后编辑 `.env` 文件，添加你的 API 密钥。

## Anki 设置

1. 从 https://apps.ankiweb.net/ 安装 Anki
2. 安装 AnkiConnect 插件：
   - 打开 Anki
   - 进入 工具 > 插件 > 获取插件
   - 输入代码：`2055492159`
   - 重启 Anki

3. 配置 AnkiConnect：
   - 进入 工具 > 插件 > AnkiConnect > 配置
   - 将配置替换为：
```json
{
    "apiKey": null,
    "apiLogPath": null,
    "ignoreOriginList": [],
    "webBindAddress": "127.0.0.1",
    "webBindPort": 8765,
    "webCorsOriginList": [
        "http://localhost",
        "http://127.0.0.1",
        "http://127.0.0.1:8765",
        "http://localhost:8765",
        "https://127.0.0.1",
        "https://localhost",
        "https://127.0.0.1:8765",
        "https://localhost:8765",
        "*"
    ]
}
```

## 使用方法

1. 启动 Anki 并保持在后台运行
2. 启动网络服务器：
```bash
python server.py
```
3. 打开浏览器访问 http://localhost:8000
4. 输入主题并点击"生成单词"
5. 点击"添加到 Anki"创建闪卡

## 许可证

本项目采用非商业性公共许可证（NCPL）授权。这意味着：

✅ 你可以：
- 将本软件用于个人用途
- 修改本软件
- 与他人分享本软件
- 为项目做出贡献

❌ 你不能：
- 将本软件用于商业用途
- 销售本软件或其修改版本
- 删除或修改本许可证声明

本项目使用的所有 API 密钥和服务都需要单独的许可证和服务条款协议。 