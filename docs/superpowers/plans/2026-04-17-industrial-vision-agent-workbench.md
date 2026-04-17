# 工业视觉测试用例 Agent 工作台 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将现有静态 Markdown 文档升级为一个基于 Python 的工业视觉测试用例 Agent 工作台，支持从零生成、已有用例优化、知识库驱动生成、覆盖分析与 Markdown / 树形文本 / JSON 导出。

**Architecture:** 单体 FastAPI 应用承载页面与动作路由；Jinja2 模板 + HTMX 组织三栏工作台界面；本地 YAML/JSON/Markdown 存储知识、模板与任务；统一模型串联需求解析、知识检索、测试点规划、测试用例生成、覆盖分析、用例优化和导出模块。

**Tech Stack:** Python 3.11+, FastAPI, Jinja2, HTMX, Pydantic, PyYAML, pytest

---

## 文件规划

**Create**
- `requirements.txt`
- `app/main.py`
- `app/routes/pages.py`, `app/routes/actions.py`
- `app/models/task.py`, `app/models/case.py`, `app/models/knowledge.py`
- `app/services/knowledge_service.py`, `app/services/task_service.py`, `app/services/template_service.py`, `app/services/validation_service.py`
- `app/agents/requirement_agent.py`, `app/agents/knowledge_agent.py`, `app/agents/planning_agent.py`, `app/agents/generation_agent.py`, `app/agents/coverage_agent.py`, `app/agents/optimization_agent.py`
- `app/exporters/markdown_exporter.py`, `app/exporters/tree_exporter.py`, `app/exporters/json_exporter.py`
- `templates/pages/layout.html`, `templates/pages/dashboard.html`, `templates/pages/generate.html`, `templates/pages/optimize.html`, `templates/pages/knowledge.html`
- `templates/partials/result_panel.html`
- `static/css/app.css`, `static/js/app.js`
- `knowledge/tools/area-detection.yaml`, `knowledge/tools/defect-detection.yaml`
- `knowledge/strategies/parameter-boundary.yaml`, `knowledge/defects/common-risks.yaml`
- `prompts/system/default.md`, `prompts/generation/default.md`, `prompts/optimization/default.md`
- `tests/test_pages.py`, `tests/test_models.py`, `tests/test_knowledge_service.py`, `tests/test_requirement_agent.py`, `tests/test_planning_agent.py`, `tests/test_generation_agent.py`, `tests/test_coverage_agent.py`, `tests/test_optimization_agent.py`, `tests/test_exporters.py`

**Reuse and split**
- `skill.md` → `knowledge/strategies/`, `prompts/system/`
- `rules.md` → `knowledge/strategies/`, `app/services/validation_service.py`
- `prompt-templates.md` → `prompts/`
- `knowledge-base.md` → `knowledge/tools/`, `knowledge/strategies/`, `knowledge/defects/`

---

### Task 1: 初始化项目骨架

**Files:** `requirements.txt`, `app/main.py`, `app/routes/pages.py`, `app/routes/actions.py`, `templates/pages/layout.html`, `templates/pages/dashboard.html`, `static/css/app.css`, `static/js/app.js`, `tests/test_pages.py`

- [ ] 先写失败测试：访问 `/` 返回 200 且包含“工业视觉测试用例 Agent 工作台”。
- [ ] Run: `pytest tests/test_pages.py::test_dashboard_page_loads -v` → Expected: FAIL
- [ ] 最小实现：`create_app()`、首页路由、基础模板、基础样式。
- [ ] Run: `pytest tests/test_pages.py::test_dashboard_page_loads -v` → Expected: PASS
- [ ] Commit: `git commit -m "feat: bootstrap fastapi workbench skeleton"`

### Task 2: 建立统一数据模型与知识加载

**Files:** `app/models/*.py`, `app/services/knowledge_service.py`, `knowledge/**/*.yaml`, `tests/test_models.py`, `tests/test_knowledge_service.py`

- [ ] 先写失败测试：`GenerateTaskInput` 能解析参数和流程；`KnowledgeService` 能加载“面积检测工具”。
- [ ] Run: `pytest tests/test_models.py tests/test_knowledge_service.py -v` → Expected: FAIL
- [ ] 实现模型：`GenerateTaskInput`、`ParameterInput`、`TestPoint`、`TestCase`、`CoverageReport`、`KnowledgeItem`。
- [ ] 实现知识服务：遍历 `knowledge/**/*.yaml` 加载并支持 `search()`。
- [ ] 创建首批知识文件：面积检测、瑕疵检测、参数边界策略、常见风险。
- [ ] Run: `pytest tests/test_models.py tests/test_knowledge_service.py -v` → Expected: PASS
- [ ] Commit: `git commit -m "feat: add core models and structured knowledge base"`

### Task 3: 实现需求解析、知识检索与测试点规划

**Files:** `app/services/validation_service.py`, `app/agents/requirement_agent.py`, `app/agents/knowledge_agent.py`, `app/agents/planning_agent.py`, `tests/test_requirement_agent.py`, `tests/test_planning_agent.py`

- [ ] 先写失败测试：需求解析后 `mode == "generate"`；规划结果至少包含功能、参数、流程测试点。
- [ ] Run: `pytest tests/test_requirement_agent.py tests/test_planning_agent.py -v` → Expected: FAIL
- [ ] 实现校验：必填字段校验。
- [ ] 实现需求解析：表单负载转 `GenerateTaskInput`。
- [ ] 实现知识检索：根据工具名检索知识条目。
- [ ] 实现测试点规划：基础功能点、参数边界点、完整流程点、知识库风险异常点。
- [ ] Run: `pytest tests/test_requirement_agent.py tests/test_planning_agent.py -v` → Expected: PASS
- [ ] Commit: `git commit -m "feat: add requirement parsing and test planning"`

### Task 4: 实现测试用例生成、覆盖分析和导出

**Files:** `app/agents/generation_agent.py`, `app/agents/coverage_agent.py`, `app/exporters/*.py`, `tests/test_generation_agent.py`, `tests/test_coverage_agent.py`, `tests/test_exporters.py`

- [ ] 先写失败测试：生成后首条 ID 为 `VIS-AREA-FUNC-001`；仅有功能测试时覆盖分析缺少异常测试；Markdown/树形/JSON 导出包含关键字段。
- [ ] Run: `pytest tests/test_generation_agent.py tests/test_coverage_agent.py tests/test_exporters.py -v` → Expected: FAIL
- [ ] 实现生成：按工具编码 + 测试类型编码生成标准用例。
- [ ] 实现覆盖分析：固定检查功能、参数、流程、异常 4 类覆盖。
- [ ] 实现导出：Markdown、XMind 风格树形文本、JSON。
- [ ] Run: `pytest tests/test_generation_agent.py tests/test_coverage_agent.py tests/test_exporters.py -v` → Expected: PASS
- [ ] Commit: `git commit -m "feat: add generation coverage and exporters"`

### Task 5: 实现已有用例优化 Agent

**Files:** `app/agents/optimization_agent.py`, `tests/test_optimization_agent.py`

- [ ] 先写失败测试：缺少异常/参数测试时，优化结果摘要包含“补充异常测试”，且返回建议用例。
- [ ] Run: `pytest tests/test_optimization_agent.py -v` → Expected: FAIL
- [ ] 实现优化：根据缺失类型生成建议用例和摘要。
- [ ] Run: `pytest tests/test_optimization_agent.py -v` → Expected: PASS
- [ ] Commit: `git commit -m "feat: add case optimization agent"`

### Task 6: 实现工作台页面、动作路由与持久化

**Files:** `app/routes/pages.py`, `app/routes/actions.py`, `templates/pages/*.html`, `templates/partials/result_panel.html`, `static/css/app.css`, `static/js/app.js`, `app/services/task_service.py`, `app/services/template_service.py`, `prompts/**/*.md`, `tests/test_pages.py`

- [ ] 先写失败测试：`/generate` 页面包含“功能描述”“参数配置”；`POST /actions/generate` 返回结果面板且包含“测试点”“覆盖分析”。
- [ ] Run: `pytest tests/test_pages.py -v` → Expected: FAIL
- [ ] 实现页面：`/generate`、`/optimize`、`/knowledge`。
- [ ] 实现动作：
  - 生成链路：需求解析 → 知识检索 → 测试点规划 → 测试用例生成 → 覆盖分析 → 渲染 `result_panel.html`
  - 优化链路：已有用例文本 → 缺失项 → 优化 Agent → 渲染 `result_panel.html`
- [ ] 实现持久化：保存任务 JSON，读取 prompt 模板。
- [ ] 完成三栏布局：左导航 / 中央工作区 / 右结果区。
- [ ] Run: `pytest -v` → Expected: PASS
- [ ] Commit: `git commit -m "feat: complete first mvp workflow"`

---

## 计划自检
- 规格覆盖：从零生成、用例优化、知识库驱动、覆盖分析、多格式导出、Web 工作台。
- 无占位词：没有 `TBD`、`TODO`、`后续补充`。
- 类型一致：统一使用 `GenerateTaskInput`、`TestPoint`、`TestCase`、`CoverageReport`、`KnowledgeItem`。
