# orbit-algo-mind

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Framework](https://img.shields.io/badge/Framework-Hermes-purple)](#)
[![API](https://img.shields.io/badge/API-MiMo_OpenAI Compatible-red)](#)

> 基于 Hermes 的算法解题与教学 Agent — 自动生成多语言实现、测试用例和渐进式提示

## 目录

- [核心功能](#核心功能)
- [系统架构](#系统架构)
- [界面预览](#界面预览)
- [快速启动](#快速启动)
- [API 端点](#api-端点)
- [环境变量](#环境变量)
- [项目结构](#项目结构)
- [技术栈](#技术栈)
- [贡献指南](#贡献指南)
- [License](#license)

## 核心功能

- **多语言解题** — Python、C++、Go 三种语言的地道实现
- **测试用例生成** — 每题 8-15 个用例，覆盖边界值和对抗性输入
- **沙箱执行** — 自动运行代码并验证测试结果
- **渐进式教学** — 苏格拉底式提示（不直接给答案，分步引导）
- **性能基准** — 执行计时 + 内存测量 + 多语言对比图表

## 系统架构

```
┌──────────────┐     ┌──────────────┐     ┌──────────────────────┐     ┌──────────────┐
│  输入算法题目  │────▶│  FastAPI 后端  │────▶│   AlgorithmAgent     │────▶│  多语言解答   │
│              │     │  (main.py)   │     │                      │     │  + 测试报告   │
└──────────────┘     └──────────────┘     │  ┌────────────────┐  │     └──────────────┘
                                           │  │  问题解析        │  │
                                           │  │  - 算法类别识别  │  │
                                           │  │  - 约束提取      │  │
                                           │  └────────────────┘  │
                                           │         │             │
                                           │         ▼             │
                                           │  ┌────────────────┐  │
                                           │  │  深度推理        │◀─┼──── Tool Calling
                                           │  │  (Deep Thinking)│  │     (语法校验→测试执行→性能测量)
                                           │  │  - 代码生成      │  │
                                           │  │  - 测试生成      │  │
                                           │  └────────────────┘  │
                                           │         │             │
                                           │         ▼             │
                                           │  ┌────────────────┐  │
                                           │  │  沙箱代码执行    │  │
                                           │  │  - Python/C++/Go│  │
                                           │  │  - 自动验证      │  │
                                           │  └────────────────┘  │
                                           └──────────────────────┘
```

## 界面预览

> 工作流程图截图保存在 [`demos/images/`](../demos/images/orbit-algo-mind.png)

| 区域 | 说明 |
|------|------|
| **输入区** | 语言选择器（Python/C++/Go）+ 模式切换（完整解法 / 渐进式提示）+ 题目输入区 |
| **解答展示** | 算法名称、语言、时间/空间复杂度标签 + 算法解释 + 语法高亮代码 |
| **测试区** | 测试用例列表（输入/期望输出/描述）+ 通过/失败统计 + 性能基准对比 |

## 快速启动

### 环境要求

- Python 3.11+
- Node.js 18+
- npm 9+
- g++ (C++ 编译，可选)
- Go (可选)

### 后端

```bash
cd orbit-algo-mind
pip install -e .
cp .env.example .env   # 填写 MIMO_API_KEY（留空则使用 Mock 模式）
uvicorn src.algorithm.main:app --reload
```

### 前端

```bash
cd orbit-algo-mind/web
npm install
npm run dev
```

访问 <http://localhost:3004>

## API 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/solve` | 解题（标准） |
| POST | `/api/solve/stream` | 解题（流式 SSE） |
| GET | `/api/stats` | Token 消耗统计 |
| GET | `/health` | 健康检查 |

## 环境变量

```bash
# .env
MIMO_API_KEY=your-api-key       # 留空则使用 Mock 模式
MIMO_BASE_URL=https://api.xiaomimimo.com/v1
MIMO_MODEL=mimo-v2.5-pro
```

## 项目结构

```
orbit-algo-mind/
├── src/algorithm/
│   ├── main.py              # FastAPI 入口
│   ├── client.py            # MiMo API 客户端（支持 Mock 模式）
│   ├── agent.py             # 核心 Agent（多轮推理 + Deep Thinking）
│   ├── code_executor.py     # 沙箱代码执行（Python/C++/Go）
│   ├── prompts/             # Prompt 模板
│   │   └── system.py        # 系统提示词 + 渐进式提示词
│   └── models.py            # Pydantic 数据模型
├── web/                     # Next.js 前端
├── tests/                   # 单元测试
├── pyproject.toml
├── .env.example
└── LICENSE
```

## 技术栈

| 层级 | 技术 |
|------|------|
| **后端** | Python 3.11+、FastAPI、subprocess（沙箱执行）、Pydantic v2 |
| **前端** | Next.js 15、React 19、TypeScript |
| **AI** | MiMo API（OpenAI 兼容协议）、Deep Thinking、Tool Calling、Structured Output |

## 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## License

[MIT](LICENSE)
