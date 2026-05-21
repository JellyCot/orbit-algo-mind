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

- **多语言解题** — Python、C++、Go 三种语言的地道实现，C++ 使用 `-O2` 优化编译
- **测试用例生成** — 每题 8-15 个用例，覆盖边界值和对抗性输入
- **沙箱代码执行** — 隔离式 subprocess 执行，10 秒超时保护，临时文件自动清理
- **执行计时** — 每个测试用例独立测量执行耗时（毫秒精度），支持多语言性能对比
- **渐进式教学** — 苏格拉底式提示（不直接给答案，分步引导）
- **性能基准** — 执行计时 + 内存测量 + 多语言对比图表
- **语法高亮** — 前端内置 Python/C++/Go 关键字高亮引擎，行号显示 + 暗色主题
- **Tab 切换视图** — 代码与测试用例分 Tab 展示，界面更清晰

## 系统架构

```
                         ┌─────────────────────────────────────────────────────────┐
                         │                  orbit-algo-mind 工作流                  │
                         └─────────────────────────────────────────────────────────┘

 ┌──────────┐    ┌────────────┐    ┌─────────────┐    ┌──────────────┐    ┌──────────────┐
 │          │    │            │    │             │    │              │    │              │
 │  输入     │───▶│  问题解析   │───▶│  代码生成    │───▶│  沙箱执行     │───▶│  结果输出     │
 │  算法题目  │    │            │    │             │    │              │    │              │
 │          │    │  算法类别识别 │    │  Python/C++/ │    │  逐用例运行    │    │  解答 + 报告  │
 │          │    │  约束条件提取 │    │  Go 地道实现  │    │  执行计时     │    │  + 性能基准   │
 │          │    │  难度评估    │    │  测试用例生成 │    │  结果校验     │    │  + 语法高亮   │
 │          │    │            │    │             │    │  超时保护     │    │              │
 └──────────┘    └────────────┘    └─────────────┘    └──────────────┘    └──────────────┘
                        │                │                   │
                        │                │                   │
                        ▼                ▼                   ▼
                 ┌──────────────────────────────────────────────────┐
                 │              AlgorithmAgent (核心调度)             │
                 │                                                  │
                 │   ┌─────────────┐   ┌──────────────────────┐    │
                 │   │ Deep Thinking │   │ Tool Calling          │    │
                 │   │ 多轮推理      │◀──│ 语法校验 → 测试执行    │    │
                 │   │ 链式思考      │──▶│ → 性能测量 → 反馈修正  │    │
                 │   └─────────────┘   └──────────────────────┘    │
                 └──────────────────────────────────────────────────┘
```

**数据流说明：**

1. **问题解析** — AlgorithmAgent 接收算法题目，识别算法类别（动态规划、图论等）、提取约束条件、评估难度
2. **代码生成** — Deep Thinking 模式生成多语言实现和测试用例，通过 Tool Calling 提交到沙箱
3. **沙箱执行** — 每个测试用例在隔离 subprocess 中运行，记录执行时间，处理超时和编译错误
4. **结果输出** — 返回语法高亮的代码、通过/失败统计、毫秒级执行耗时和多语言性能对比

## 界面预览

> 工作流程图截图保存在 [`demos/images/`](../demos/images/orbit-algo-mind.png)

| 区域 | 说明 |
|------|------|
| **输入区** | 语言选择器（Python/C++/Go）+ 模式切换（完整解法 / 渐进式提示）+ 题目输入区 |
| **解答展示** | 算法名称、语言、时间/空间复杂度标签 + 算法解释 + 语法高亮代码 |
| **代码 / 测试 Tab** | 代码 Tab：行号 + 关键字高亮（Python/C++/Go）；测试 Tab：输入/期望/描述 |
| **执行结果** | 通过/失败统计 + 每用例执行耗时（ms）+ 多语言对比 |

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

### 运行测试

```bash
cd orbit-algo-mind
pytest tests/ -v
```

测试覆盖：Mock 模式解题、渐进式提示、多语言调度、基础执行器、多用例执行、超时处理、不支持语言的错误处理。

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
│   ├── __init__.py            # 模块导出（Agent / Models / Executor / Client）
│   ├── main.py                # FastAPI 入口
│   ├── client.py              # MiMo API 客户端（支持 Mock 模式）
│   ├── agent.py               # 核心 Agent（多轮推理 + Deep Thinking）
│   ├── code_executor.py       # 沙箱执行（Python/C++/Go，计时 + 超时保护 + 文件清理）
│   ├── models.py              # Pydantic 数据模型
│   └── prompts/
│       └── system.py          # 系统提示词 + 渐进式提示词
├── web/                       # Next.js 前端
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx     # 根布局
│   │   │   └── page.tsx       # 主页面
│   │   └── components/
│   │       ├── ProblemInput.tsx   # 题目输入组件
│   │       └── SolutionView.tsx   # 解答展示（语法高亮 + Tab 切换）
│   ├── next.config.ts
│   ├── package.json
│   └── tsconfig.json
├── tests/
│   └── test_agent.py          # 单元测试（Agent / 执行器 / 超时 / 多用例）
├── pyproject.toml
├── .env.example
├── .gitignore
└── LICENSE
```

## 技术栈

| 层级 | 技术 |
|------|------|
| **后端** | Python 3.11+、FastAPI、subprocess（沙箱执行）、Pydantic v2 |
| **前端** | Next.js 15、React 19、TypeScript、内置语法高亮引擎 |
| **AI** | MiMo API（OpenAI 兼容协议）、Deep Thinking、Tool Calling、Structured Output |
| **测试** | pytest、pytest-asyncio，覆盖执行器 / Agent / 超时 / 边界场景 |

## 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## License

[MIT](LICENSE)
