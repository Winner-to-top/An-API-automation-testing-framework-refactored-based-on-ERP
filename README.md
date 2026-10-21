# 星云 ERP 接口自动化测试框架（jkzdh_erp）

基于 **pytest + Excel 数据驱动 + Allure** 的 ERP 系统接口自动化测试框架。用例统一维护在 Excel 中，支持接口关联（Token 传递）、JSONPath 断言与提取、MySQL 数据库断言与提取、验证码 OCR 识别、失败重试、Allure 报告生成以及飞书群机器人通知，可在测试环境与生产环境之间一键切换。

> 本项目为通用接口自动化框架的 ERP 业务适配版，覆盖登录、采购、销售订单等核心业务链路。

---

## 目录

- [功能特性](#功能特性)
- [技术栈](#技术栈)
- [项目结构](#项目结构)
- [环境要求](#环境要求)
- [快速开始](#快速开始)
- [配置说明](#配置说明)
- [运行测试](#运行测试)
- [执行流程](#执行流程)
- [测试用例编写规范](#测试用例编写规范)
- [用例关联与数据传递](#用例关联与数据传递)
- [测试报告](#测试报告)
- [结果通知](#结果通知)
- [常见问题](#常见问题)
- [上传 GitHub 前必读](#上传-github-前必读)
- [License](#license)

---

## 功能特性

| 特性 | 说明 |
| --- | --- |
| Excel 数据驱动 | 测试用例统一存放于 Excel，新增用例无需编写 Python 代码 |
| 单一执行入口 | `testcases/test_runner.py` 参数化执行全部用例，便于统一维护 |
| 接口关联 | 基于 Jinja2 模板 + 全局变量池，实现 Token、订单 ID 等数据在用例间传递 |
| 多维度断言 | 支持 HTTP 响应断言（JSONPath / 文本包含）与 MySQL 数据库断言 |
| 数据提取 | 支持 JSONPath 提取响应数据、SQL 提取数据库数据，并写入全局变量池 |
| 验证码识别 | 集成 `ddddocr`，自动获取并识别登录验证码（生产环境启用） |
| 失败重试 | 基于 `pytest-rerunfailures`，失败用例自动重试 3 次 |
| 环境切换 | 通过 `python run.py test / prod` 切换测试 / 生产环境 |
| 可视化报告 | 自动生成 Allure HTML 报告，按模块 / 场景分组展示 |
| 结果通知 | 执行完成后自动推送飞书群消息，附测试报告链接 |
| 数据清理 | 会话结束后自动执行清理 SQL（`conftest.py`） |

---

## 技术栈

| 组件 | 版本 | 用途 |
| --- | --- | --- |
| Python | 3.9+ | 运行环境 |
| pytest | 8.3.2 | 测试框架 |
| requests | 2.32.3 | HTTP 接口请求 |
| PyMySQL | 1.1.1 | MySQL 数据库操作 |
| jsonpath | 0.82.2 | JSON 响应解析 |
| openpyxl | 3.1.5 | 读取 Excel 测试用例 |
| Jinja2 | 3.1.4 | 用例数据模板渲染 |
| allure-pytest | 2.13.5 | Allure 报告集成 |
| ddddocr | 1.5.6 | 验证码 OCR 识别 |
| pytest-rerunfailures | 15.1 | 失败用例重试 |

---

## 项目结构

```
jkzdh_erp/
├── config/
│   ├── config.py              # 全局配置：Excel 路径、清理 SQL、飞书通知、报告地址
│   ├── env_manager.py         # 环境管理：注入 URL / DB / ENV 环境变量
│   ├── local_config.example.py# 本地配置模板（复制为 local_config.py 后填写）
│   └── local_config.py        # 本地真实配置（已被 .gitignore 忽略，需自行创建）
├── data/
│   ├── 测试用例完整版.xlsx      # 当前执行使用的测试用例文件
│   └── 测试用例.xlsx            # 基础示例用例
├── file/
│   └── 1.jpg                  # 文件上传类用例的测试附件
├── log/
│   └── test.log               # pytest 运行日志
├── report/
│   ├── json_report/           # Allure 原始结果数据
│   └── html_report/           # Allure 生成的 HTML 报告
├── testcases/
│   └── test_runner.py         # 统一测试执行入口（参数化驱动 Excel 用例）
├── utils/
│   ├── allure_utils.py        # Allure 报告初始化（feature/story/title）
│   ├── analyse_case.py        # 解析用例中的请求数据
│   ├── asserts.py             # HTTP 断言 + 数据库断言
│   ├── excel_utils.py         # 读取 Excel 用例
│   ├── extractor.py           # JSONPath / SQL 数据提取
│   ├── ocr_utils.py           # 验证码获取与 OCR 识别
│   ├── send_feishu_msg.py     # 飞书机器人消息推送
│   └── send_request.py        # HTTP 请求 / JDBC 查询封装
├── conftest.py                # 会话级数据清理 fixture
├── pytest.ini                 # pytest 日志配置
├── requirements.txt           # 项目依赖
├── .gitignore                 # Git 忽略规则
└── run.py                     # 一键执行入口（环境变量设置 + 测试 + 报告 + 通知）
```

---

## 环境要求

- Python 3.9 及以上
- MySQL 5.7 / 8.0（数据库断言、数据提取、数据清理需要）
- **Allure 命令行工具**（用于生成 HTML 报告）
  - Windows：`scoop install allure` 或下载 [Allure Release](https://github.com/allure-framework/allure2/releases) 后配置 `bin` 目录到 `PATH`
  - macOS：`brew install allure`
  - 需要本机已安装 Java 8+（Allure 依赖 JRE）
  - 验证：`allure --version`

---

## 快速开始

### 1. 克隆项目

```bash
git clone <your-repository-url>
cd jkzdh_erp
```

### 2. 创建虚拟环境并安装依赖

```bash
python -m venv venv

# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 3. 配置本地环境

复制配置模板并填写实际信息：

```bash
# Windows
copy config\local_config.example.py config\local_config.py

# macOS / Linux
cp config/local_config.example.py config/local_config.py
```

在 `config/local_config.py` 中填写：

- `ENVIRONMENTS`：测试 / 生产环境的基础地址 `URL` 与数据库连接信息
- `FEISHU_WEBHOOK`：飞书群机器人 Webhook 地址
- `REPORT_PATHS`：各环境的测试报告访问地址

> `config/local_config.py` 已被 `.gitignore` 忽略，不会提交到 Git，可以安全存放本地敏感信息。
> 也可以通过环境变量注入（见 [配置说明](#配置说明)），适用于 CI 场景。

### 4. 执行测试

```bash
# 测试环境
python run.py test

# 生产环境
python run.py prod
```

执行完成后会自动：

1. 运行全部启用的用例；
2. 生成 Allure HTML 报告到 `report/html_report`；
3. 推送飞书通知（可通过开关关闭）。

---

## 配置说明

### 环境变量

框架通过环境变量区分执行环境，由 `run.py` 调用 `config/env_manager.py` 在启动时注入。配置优先级为：

**已存在的环境变量 > `config/local_config.py` > 报错提示**

| 变量 | 说明 | 示例 |
| --- | --- | --- |
| `URL` | 接口基础地址，用例中的 `path` 会拼接在其后 | `http://127.0.0.1:9005` |
| `DB` | MySQL 连接信息（字符串形式的字典，代码中通过 `eval` 还原） | `{'host':'127.0.0.1','port':3306,'database':'xingyun','user':'root','password':'***'}` |
| `ENV` | 环境标识，`test` 或 `prod`，影响验证码逻辑与报告地址 | `test` |
| `FEISHU_WEBHOOK` | 飞书机器人 Webhook，覆盖本地配置 | `https://open.feishu.cn/open-apis/bot/v2/hook/***` |
| `FEISHU_IS_SEND` | 是否发送飞书通知，默认 `true` | `false` |
| `PROJECT_NAME` | 通知中的项目名称，默认「星云ERP」 | `星云ERP` |
| `REPORT_PATH` | 测试报告地址，覆盖本地配置 | `http://jenkins/.../allure/` |

> `URL` / `DB` 由 `run.py` 根据命令行参数（`test` / `prod`）自动注入，无需手动设置；
> CI 中可提前设置这两个变量，框架会优先使用环境变量中的值。
> `config/config.py` 在导入时读取 `ENV`，直接使用 `run.py` 启动即可保证顺序正确。

### 全局配置项（`config/config.py`）

| 配置项 | 说明 |
| --- | --- |
| `EXCEL_FILE` | Excel 用例文件路径，默认 `./data/测试用例完整版.xlsx` |
| `SHEET_NAME` | 读取的工作表名称，默认 `Sheet1` |
| `SQL1` / `SQL2` | 会话结束后执行的清理 SQL |
| `WEBHOOK` | 飞书群机器人 Webhook 地址（环境变量 `FEISHU_WEBHOOK` 或本地配置） |
| `PROJECT` | 项目名称，用于通知消息 |
| `FEISHU_IS_SEND` | 是否发送飞书消息的开关 |
| `REPORT_PATH` | 测试报告访问地址（环境变量 `REPORT_PATH` 或本地配置，区分 test / prod） |

---

## 运行测试

### 方式一：一键运行（推荐）

```bash
python run.py test    # 测试环境
python run.py prod    # 生产环境
```

### 方式二：直接使用 pytest

```bash
# 先手动设置环境变量（以 Windows PowerShell 为例）
$env:URL="http://127.0.0.1:9005"
$env:DB="{'host':'127.0.0.1','port':3306,'database':'xingyun','user':'root','password':'***'}"
$env:ENV="test"

pytest -vs ./testcases/test_runner.py --alluredir ./report/json_report --clean-alluredir
allure generate ./report/json_report -o ./report/html_report --clean
allure open ./report/html_report
```

### 方式三：按模块 / 场景过滤

```bash
pytest ./testcases/test_runner.py -k "登录" --alluredir ./report/json_report
pytest ./testcases/test_runner.py -k "销售" --alluredir ./report/json_report
```

---

## 执行流程

```mermaid
flowchart TD
    A[run.py 启动] --> B[注入 URL / DB / ENV 环境变量]
    B --> C[读取 Excel 用例]
    C --> D{is_true 是否为 True}
    D -- 否 --> Z[跳过该用例]
    D -- 是 --> E[Jinja2 渲染用例模板<br/>替换 {{变量}}]
    E --> F[解析请求数据<br/>method / url / headers / params / data / json / files]
    F --> G[发送 HTTP 请求]
    G --> H[HTTP 断言<br/>JSONPath 或文本包含]
    H --> I[数据库断言<br/>可选]
    I --> J[JSONPath / SQL 数据提取<br/>写入全局变量池]
    J --> K[下一用例]
    K --> C
    C --> L[全部执行完成]
    L --> M[生成 Allure HTML 报告]
    L --> N[执行数据清理 SQL]
    M --> O[推送飞书通知]
```

单条用例由 `testcases/test_runner.py` 的四个核心步骤驱动：

1. **解析请求数据**：`analyse_case()`
2. **发送请求**：`send_http_request()`
3. **断言**：`http_assert()` + `jdbc_assert()`
4. **提取**：`json_extractor()` + `jdbc_extractor()`

---

## 测试用例编写规范

用例文件为 `data/测试用例完整版.xlsx`，默认读取 `Sheet1`：

- **第 1 行**：中文字段说明（仅供阅读）
- **第 2 行**：英文字段名（程序读取的 key 行）
- **第 3 行起**：用例数据，`is_true` 为空的整行会被自动跳过

### 字段说明

| 字段 | 中文含义 | 说明 |
| --- | --- | --- |
| `id` | 用例编号 | 唯一编号，展示在报告标题中 |
| `feature` | 模块 | 对应 Allure 的 feature |
| `story` | 场景 | 对应 Allure 的 story |
| `title` | 用例标题 | 对应 Allure 的 title |
| `method` | 请求方式 | GET / POST / PUT / PATCH / DELETE 等 |
| `path` | 请求路径 | 与 `URL` 拼接为完整地址，如 `/auth/login` |
| `headers` | 请求头 | 字符串形式的字典，如 `{"x-auth-token":"{{token}}"}` |
| `params` | URL 参数 | 字符串形式的字典 |
| `data` | 表单参数 | 字符串形式的字典（form-data） |
| `json` | JSON 请求体 | 字符串形式的字典（application/json） |
| `files` | 上传文件 | 字符串形式的字典，如 `{"file": open("file/1.jpg","rb")}` |
| `check` | 断言字段 | JSONPath 字段列表，如 `["code","msg"]`；留空则按文本包含断言 |
| `expected` | 期望结果 | 与 `check` 按顺序一一对应的期望值列表 |
| `sql_check` | 数据库断言 SQL | 查询返回单行单列结果 |
| `sql_expected` | 数据库期望结果 | 与 `sql_check` 的查询结果比较 |
| `jsonExData` | JSON 数据提取 | 字典形式，如 `{"token":"$..token"}` |
| `sqlExData` | 数据库数据提取 | 字典形式，如 `{"ADMIN_NAME":"select mg_name from ..."}` |
| `is_true` | 是否执行 | `TRUE` 执行，其他值跳过 |

### 示例：登录并提取 Token

| 字段 | 值 |
| --- | --- |
| `id` | `2` |
| `feature` | `登录` |
| `story` | `登录成功` |
| `title` | `用户登录成功` |
| `method` | `post` |
| `path` | `/auth/login` |
| `headers` | `{"accept":"application/json, text/plain, */*"}` |
| `data` | `{"username":"1000@admin","password":"admin","sn":get_res_sn_captcha()["sn"],"captcha":get_res_sn_captcha()["captcha"]}` |
| `check` | `["code"]` |
| `expected` | `[200]` |
| `jsonExData` | `{"token": "$..token"}` |
| `is_true` | `TRUE` |

后续用例即可在 `headers` 或参数中通过 `{{token}}` 引用该值。

### 断言规则

- **`check` 有值**：从响应 JSON 中逐个取 JSONPath 结果，与 `expected` 按 `zip` 顺序比较，全部相等才算通过。
- **`check` 为空**：遍历 `expected`，逐个判断其字符串形式是否包含在响应文本中。
- **数据库断言**：`sql_check` 与 `sql_expected` 均非空时执行，比较查询结果与期望值。

---

## 用例关联与数据传递

框架使用 **模块级全局变量池** 保存提取结果：

1. `test_runner.py` 中的 `TestRunner.all` 字典作为全局变量池；
2. 每条用例执行前，用 `jinja2.Template` 渲染用例内容，将 `{{变量名}}` 替换为实际值；
3. 用例执行后，通过 `jsonExData` / `sqlExData` 将新值写回变量池，供后续用例使用。

典型业务链路：

```
获取验证码 → 提取 sn → 登录 → 提取 token
    → 查询销售订单 → 提取 order_id / payTypeId
    → 查看订单详情 → 审核订单 → 删除订单
```

> Excel 中的请求数据通过 `eval` 解析，模板渲染也使用 `eval`。这意味着**用例文件应被视为受信任的代码**，不要执行来源不明的 Excel 文件。

---

## 测试报告

执行完成后生成 Allure HTML 报告：

```bash
# 生成报告
allure generate ./report/json_report -o ./report/html_report --clean

# 本地打开
allure open ./report/html_report

# 或者直接启动临时服务
allure serve ./report/json_report
```

报告中可按 `feature`（模块）与 `story`（场景）分组查看，每条用例标题格式为：

```
ID:2 -- 用户登录成功
```

失败用例会自动重试 3 次（`@pytest.mark.flaky(reruns=3)`）。

---

## 结果通知

`run.py` 执行结束后会调用 `utils/send_feishu_msg.py` 推送飞书消息，内容包括：

- 项目名称
- 执行时间
- 测试报告链接

可通过 `config/config.py` 中的 `FEISHU_IS_SEND` 开关控制是否发送。

---

## 常见问题

**Q1：提示 `allure` 不是内部或外部命令**

未安装 Allure 命令行工具或未加入 `PATH`。安装后执行 `allure --version` 验证。

**Q2：启动时报 `KeyError: 'ENV'`**

`config/config.py` 在导入时依赖 `ENV` 环境变量，请使用 `python run.py test` 或 `python run.py prod` 启动，并确保先设置环境变量再导入配置。

**Q3：数据库连接失败**

检查 `run.py` 中的 `DB` 字典（host、port、database、user、password）以及数据库白名单 / 网络连通性。

**Q4：登录用例验证码错误**

- 测试环境：`ocr_utils.py` 默认使用固定验证码 `aaaa`，需确认被测环境已关闭验证码校验；
- 生产环境：使用 `ddddocr` 自动识别，识别率受图片质量影响，失败时会自动重试。

**Q5：用例没有执行**

检查该行 `is_true` 是否为 `TRUE`，或整行是否为空。

**Q6：日志文件编码 / 中文乱码**

建议使用 UTF-8 编码保存 Excel 与日志；Windows 控制台可执行 `chcp 65001`。

---

## 上传 GitHub 前必读

敏感信息已迁移到 `config/local_config.py`（已被 `.gitignore` 忽略），仓库中只保留占位符模板 `config/local_config.example.py`。上传前仍需确认：

1. **确认本地配置未被跟踪**

   ```bash
   git ls-files config/local_config.py   # 应无任何输出
   git status --ignored config/local_config.py
   ```

2. **清理历史提交中的敏感信息**

   即使当前文件已不含密码，**之前的提交仍可能保留真实凭据**：

   ```bash
   git log -p -- run.py config/config.py
   ```

   如果历史中存在真实密码、Webhook 或内网地址，请使用 `git filter-repo` 或 BFG 清理历史，并**修改数据库密码、重置飞书机器人 Webhook**。仅删除文件或新增提交并不能让旧凭据失效。

3. **忽略运行产物**：报告、日志、缓存等文件不应提交到仓库，项目已提供 `.gitignore`：

```gitignore
# Python
__pycache__/
*.py[cod]
*.egg-info/
.venv/
venv/

# 测试产物
report/
log/
testcases/log/
.pytest_cache/
allure-results/

# IDE
.idea/
.vscode/
.DS_Store

# 本地配置
config/local.py
.env
```

4. **清理已跟踪的产物文件**（如报告、日志已被 Git 跟踪）：

```bash
git rm -r --cached report log testcases/log
git rm -r --cached '**/__pycache__'
```

> 注意：`git rm --cached` 只停止跟踪，不会删除本地文件。如历史提交中已包含密码，需要使用 `git filter-repo` 或 BFG 清理历史。

---

## License

本项目仅用于学习与内部测试实践。使用前请确认已获得被测系统的测试授权，禁止对未授权系统发起自动化请求。
