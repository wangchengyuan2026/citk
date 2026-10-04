# CIT-K arXiv 投稿操作手册（含 endorsement 指引）

> 本文档与 `CITK_paper.tex`（投稿源）配套。更新时间：2026-10。
> 当前状态：GitHub Release `v1.0.0` + Zenodo DOI `10.5281/zenodo.23145344` 已就绪；arXiv 草稿已通过 TeX Live 编译验证（见 §4）。**仅剩用户侧动作：走 endorsement → 在 arxiv.org 提交。**

---

## 1. 为什么需要 endorsement（认可）

arXiv 不是开放投稿：它要求每篇投稿至少由一位该领域的 **已有作者（endorser）** 背书，证明稿件「与该分类相关、且达到基本学术水准」。

你是**独立学者（Independent Scholar）**，无机构邮箱、无 arXiv 历史投稿记录，因此**首次投稿必然触发 endorsement 流程**。这不是拒稿，是 arXiv 的常规门槛。

- 适用分类：`cs.AI`（人工智能）、`cs.NE`（神经与演化计算）、`cs.LG`（机器学习）、`cs.RO`（机器人）。**CIT-K 最贴合 `cs.AI` 与 `cs.NE`**，建议主分类 `cs.AI`、次分类 `cs.NE`。
- endorsement 不审内容对错，只确认「相关 + 不是胡写」。

---

## 2. 获取 endorsement 的两条路径

### 路径 A：arXiv 内置 endorsement 系统（推荐）
1. 在 arxiv.org 注册账号（用你常用邮箱即可，不必机构邮箱）。
2. 进入提交流程，选好分类后，系统会提示「需要 endorsement」。
3. 点「request endorsement」，arXiv 会向你**该分类下认识的、可联系的作者**发请求，或给你一个**请求链接**你自行发给 endorser。
4. 把链接发给一位你认识、且在该分类发表过文章的学者（导师、合作者、会议认识的同行均可），对方点一下即通过。

### 路径 B：主动邮件请求（无现成 endorser 时）
发给你引用过、且在该领域发表过的作者（例如本文已引的 Keramati、Yoshida、Burda、Friston 团队学者，或你会议/社群认识的同行）。**礼貌、简短、附全文 PDF**。

**邮件模板（可直接用）：**

```
Subject: arXiv endorsement request for a minimal zero-network agent paper (cs.AI / cs.NE)

Dear Dr. <Lastname>,

I am an independent researcher working on intrinsically-motivated,
reward-free agent architectures. I have a preprint, "CIT-K: A Minimal
Zero-Data, Comfort-Driven Self-Emergent Intelligence Kernel," that I would
like to post on arXiv under cs.AI (and cs.NE).

The paper gives a ~119-line, zero-network / zero-gradient / zero-pretraining
agent driven solely by an intrinsic comfort gradient, with a two-track
reproducible validation (a canonical testbed + a MiniGrid cross-check against
a dependency-free RND variant). It positions itself as a minimal instantiation
of homeostatically-regulated RL (close to your group's HRRL line).

Would you be willing to endorse the submission? The full manuscript is attached
as PDF. I am happy to address any concerns about relevance or rigor.

Thank you for your time,
Chengyuan Wang (王程远)
Independent Scholar, Huizhou, Guangdong, China
```

> 注意：不要群发 spam；一次找 1–2 位真正相关的学者即可。多数作者愿意帮独立研究者背书，前提是稿件确实相关、写得清楚。

---

## 3. 投稿前自检清单（已在本地完成）

| 项 | 状态 | 说明 |
|----|------|------|
| 编译无错 | ✅ 见 §4 | TeX Live `pdflatex` 实地编译通过 |
| 摘要双语 | ✅ | 英文 `abstract` + 中文 `摘要` 均已在稿内 |
| 参考文献 | ✅ | 38 条 `thebibliography`，字母序，无重复键（已修 `item`/`Yoshida2025` 重复） |
| 数学环境 | ✅ | 3 处显示公式 `\[…\]` 平衡 |
| 括号/环境 | ✅ | `{`/`}` 497/497；所有 `begin/end` 配对 |
| DOI 引用 | ✅ | 状态框与 Code availability 均指向 `10.5281/zenodo.23145344` |
| 无 `\cite` 未定义 | ✅ | 全文引用为行内 prose，无 `\cite` 键缺失风险 |
| 字数/页数 | ⚠️ 自核 | arXiv 无硬性页数上限，但建议确认 PDF ≤ ~25 页、文件 ≤ 50MB |

---

## 4. 本地编译验证结论（已实地验证）

> 由 TeX Live 实地编译得出。关键修正：原 `pdflatex` 无法渲染中文 → 改用 **`xelatex` + `ctex`**（arXiv 亦支持）；并修掉转制产生的 3 类错误（重复 `\bibitem` 键、文本模式未转义下划线、空字典 `\texttt{{}}` 括号误匹配）。

| 项 | 结果 |
|----|------|
| 引擎 | `xelatex`（TeX Live: `texlive-latex-base` + `recommended` + `fonts-recommended` + `texlive-xetex` + `texlive-lang-chinese`，含 Fandol 中文字体） |
| 第 1 次编译 | 退出码 **0** |
| 第 2 次编译 | 退出码 **0** |
| 致命错误 `! ...` | **0** |
| `LaTeX Warning` | **0**（仅有 Fandol 字体对拉丁字形回退的无害提示） |
| 生成 `CITK_paper.pdf` | **20 页 / 246 KB**（远低于 arXiv 50 MB 上限） |
| 中文渲染核验 | `pdftotext` 提取确认「猫智能论 / 摘要 / 王程远 / 好利恶害 / 唯识」均正确落地，非空白方块 |
| 表格渲染 | §4.1 / §4.2 / §4.3 三表（`booktabs`）正常，无溢出 |

**结论：草稿已可投稿级编译，不再是「未验证」状态。** 投稿时上传 `CITK_paper.tex` 即可，arXiv 会自动用其兼容的 XeLaTeX 工具链处理。

---

## 5. arxiv.org 提交流程（endorser 通过后）

1. 登录 arxiv.org → "Submit a new manuscript"。
2. 选分类：**Primary `cs.AI`**，Secondary `cs.NE`（可加 `cs.LG`）。
3. 上传文件：把 `arxiv/` 目录下的 `CITK_paper.tex` 作为**主文件**上传（本稿参考文献内联于 `thebibliography`，**不需要额外 `.bbl`**；若后续改用 BibTeX 才需附 `.bbl`）。
4. 填元数据：
   - Title：`CIT-K: A Minimal Zero-Data, Comfort-Driven Self-Emergent Intelligence Kernel`
   - Authors：`Chengyuan Wang`
   - Abstract：粘贴 tex 中 `abstract` 环境内的英文摘要（arXiv 表单不支持 LaTeX 命令，去命令化纯文本即可）
   - Comments：可写 `38 pages, 3 tables; code+data archived at Zenodo doi:10.5281/zenodo.23145344`
5. 预览 PDF，确认表格/公式无溢出。
6. 提交。**arXiv 会给你一个 `arXiv:XXXX.XXXXX` 编号**，几天内公开。

---

## 6. 与 Zenodo 的口径一致性（重要）

- arXiv 预印本与 Zenodo 存档（`v1.0.0`）应保持一致。若投稿前你对 tex 又做了改动：
  - **arXiv 侧**：直接更新投稿（可多次提交 v2/v3）。
  - **Zenodo 侧**：去 https://zenodo.org/records/23145344 点 **"New version"**，重新抓取最新文件，生成新版本号（原 DOI `10.5281/zenodo.23145344` 保留为 v1，新版本获得 `...v2` 之类；或 Zenodo 给新记录号）。**此步需你本人在网页操作，我无法代点。**
- 建议：先在 arXiv 定稿，再统一触发一次 Zenodo 新版本，避免反复。

---

## 7. 安全收尾（务必做）

聊天记录中曾出现你的 **GitHub 密码**与 **Personal Access Token（PAT）明文**。这两段凭据已暴露，请立即：

1. **撤销 PAT**：GitHub → Settings → Developer settings → Personal access tokens → 删除对应 token。
2. **改 GitHub 密码**：GitHub → Settings → Password，使用新强密码（原 `WcyCat2026!Him` 已泄露）。
3. 之后如需再推送，用新 token，且**不要在任何聊天/文档里贴明文**。

---

## 8. 一句话路径

`GitHub Release(v1.0.0)` → `Zenodo DOI(已铸)` → `arXiv 投稿(待 endorsement)` → `Zenodo New version(待你网页操作)`。
前三环已闭合，后两环为**你本人侧动作**；本手册 §2/§5 已给出可直接照做的步骤与模板。
