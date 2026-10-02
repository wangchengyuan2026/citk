# HIM：一个极简的零数据、舒适度驱动、自涌现智能内核
### 猫智能论（Cat Intelligence Theory）——形式化内核与可复现测试台

> **预印本草稿。** 本稿是猫智能论（猫智能论）及其最简实现 HIM 的权威陈述。它与一套可运行、可复现的验证工具（轨道 A 规范测试台 + 轨道 B 公开基准交叉校验）一同发布。
>
> **作者：** 王程远（1987年生），广东惠州，自由学者
> **日期：** 2026-10-01
> **状态：** 投稿 arXiv + 获取 Zenodo DOI 的草稿。未经同行评审。

---

## 摘要（中文）

我们提出 **HIM**（Heuristic-Intrinsic, Minimal，启发式-内在-极简），一个源自「猫智能论」的、完整而极简的智能内核。该理论认为：智能可由一个**记忆空白的新生体**自发涌现——它(1) 发起无序的感官-运动活动，(2) 与环境互动，(3) 由「感官实时状态」与「（机体塑造的）需求状态」的**重叠率**导出**舒适度**信号，(4) **被动**记住「（运动, 感官-环境互动）→ 感官状态变化 → 舒适度波动」的因果关系，(5) 借此辨认场景并行动以维持/提升舒适度（趋利避害）。该内核不使用任何外部奖励、不接收设计者给定的目标、无神经网络、无预训练、无梯度、无逐任务分支；唯一可调参数位于身体（感官-运动）以及感官需求状态如何塑造记忆需求状态。我们将舒适度形式化为**模糊集"面重叠"度**（规范口径），并在约 119 行参考内核中以**高斯核平滑代理**实现该逐点接近度。我们在两条轨道上验证：(A) 忠实理论的 Gymnasium 兼容规范测试台；(B) 公开 **MiniGrid** 基准，HIM 与（免依赖、线性预测器变体的）**RND** 及随机策略同台对比。在结构化环境中，HIM 的结构发现广度（转移覆盖 767）**基本追平** RND（783）并**显著超过**随机（628）（10 种子均值±标准差，HIM 与 RND 之差远小于一个标准差）——且**零神经网络、零梯度、零预训练**。我们认为这使 HIM 成为他人可借以构建的候选**基座**，区别于大模型范式；并明确说明其为何**并非**为赢得 ARC-AGI 等外部目标匹配型基准而设计。

## Abstract (English)

We propose **HIM** (Heuristic-Intrinsic, Minimal), a complete yet minimal intelligence kernel derived from the *Cat Intelligence Theory* (猫智能论). The theory holds that intelligent behaviour can self-emerge from a **blank-born agent** that (1) initiates unstructured sensory-motor activity, (2) interacts with its environment, (3) derives a **comfort signal** from the *overlap rate* between its real-time sensory state and its (organism-shaped) need state, (4) **passively** memorises the causal relation *"(motion, sensory–environment interaction) → sensory change → comfort fluctuation"*, and (5) thereby learns to recognise scenes and to act so as to preserve or raise comfort — i.e. to approach and avoid harm. No external reward, no goal provided by the designer, no neural network, no pretraining, no gradient, and no per-task branching are used; the only tunable parameters lie in the body (sensory–motor) and in how the sensory-need state shapes the memory-need state. We formalise comfort as a **fuzzy-set surface-overlap** degree (canonical) and implement a **Gaussian-kernel smooth surrogate** of the pointwise closeness in a ~119-line reference kernel. We validate on two tracks: (A) a purpose-built Gymnasium-compatible canonical testbed faithful to the theory, and (B) the public **MiniGrid** benchmark, where HIM is compared head-to-head with **RND** (Random Network Distillation, Burda et al. 2018) in its **dependency-free, linear-predictor variant** (random target network + closed-form ridge predictor, no torch) and a Random policy. In structured environments HIM's structure-discovery breadth (transition coverage 767) **essentially matches** RND (783) and **clearly exceeds** Random (628), over 10 seeds (mean ± std; the HIM–RND gap is far below one standard deviation) — while using **zero neural networks, zero gradient, zero pretraining**. We argue this positions HIM as a candidate *base* (substrate) on which others may build, distinct from the large-model paradigm, and we state explicitly why it is **not** designed to win external-goal-matching benchmarks such as ARC-AGI.

---

## 1. 动机与定位

### 1.1 广被承认的 AGI 痛点
截至 2026 年，LeCun、Marcus、Harnad、Friston 等对大语言模型（LLM）范式形成了共同的诊断：它缺乏**具身 / 落地**，缺乏**内在动机**，无法**自主设定目标**，在**多步流体推理**上退化，且面临**规模扩张的收益递减**。这些恰恰就是猫智能论试图在架构层面解决的问题。

### 1.2 我们主张什么，不主张什么
我们提出一个狭窄、可验证的主张：**一个仅凭内在舒适度信号驱动的新生体，仅从交互出发，就能自涌现一个世界模型并发现环境结构——无数据、无网络、无外部奖励。** 关键的是，这不是空口断言，而是**构造性证明**（代码级取证）并在 §4.3 获得执行级佐证。我们**不**主张解决外部指定的目标任务，也**不**主张在 LLM 的主场上胜出。本工作的贡献是一个*极简、可复现的基座*，而非对标规模化模型的竞争者。

### 1.3 为何是"基座"而非"演示"
一种新智能理论只有当他人能在其上建构时才有价值。因此我们发布：(i) 一个**规范测试台**（轨道 A），它是理论忠实的"主场"；(ii) 一个**公开基准交叉校验**（轨道 B），把同一智能体置于该领域公认的内在动机基线之侧。可复现性是一块基座的入场券。

---

## 2. 猫智能论

猫智能论由王程远在反思"机器能否拥有自主动机"时提出并形式化（Wang, 2018）。其哲学与方法论原点见奠基性论文《反思智能：存在自主动机的最简机器模型设计》（Wang, 2018，已发表）：该文以"爱与恨"的极简抽象模型刻画机器自主动机，并首次将"猫智能"作为一条独立于语言图灵测试的智能判据。本稿在其之上，给出该理论的*最小可执行内核*（HIM）与*无预训练存在性证明*。

### 2.1 核心因果链
1. **空白出生。** 记忆初始为空。感官装置以无序方式运动（静止本身也是一种运动模式）。
2. **互动。** 运动触及环境并改变实时感官状态。
3. **重叠 → 舒适度。** 实时感官状态与（机体塑造的）需求状态之间的*重叠率*产生一次**舒适度波动**。
4. **被动因果记忆。** 智能体被动记录*"何种运动 + 何种感官-环境互动 → 何种感官变化 → 何种舒适度波动"*，形成对场景的因果记忆。
5. **辨认与决策。** 智能体凭此记忆辨认场景，并决定维持或提升舒适度的动作——智能（趋利避害）由此诞生。

### 2.2 舒适度的形式化（规范口径）
遵循已定口径，舒适度是一个**模糊集"面重叠"度**。令需求状态与感官状态为定义域 $x$ 上的隶属函数 $\mu_{\text{need}}(x)$ 与 $\mu_{\text{sens}}(x)$（"需求面"是不规则的，并非单一标量）。**重叠率**即模糊**子集度**

$$
O \;=\; \frac{\sum_x \min(\mu_{\text{need}}(x),\,\mu_{\text{sens}}(x))}{\sum_x \mu_{\text{need}}(x)},
\qquad \text{comfort} = f(O),\;\; f \text{ 单调}.
$$

标量除法形式（*感官 ÷ 需求*）只是日常叙述中的退化简写；它**不是**工作定义。基于差值的逐分量接近度 $1 - |Q_2 - M|$ 是此重叠的一个**逐点原语**（小偏差下单调、近似线性的代理），也是内核所逼近的概念目标。参考内核实现的是该逐点接近度的**高斯核平滑代理**——$\exp(-\|s - \text{NEED}\|^{2} / 2\sigma^{2})$——它在保持单调结构的同时具备可微性与数值稳定性；它是重叠原语的**忠实而非逐字**的实现。舒适度与重叠**成正比**（而非恒等等于）；施加一个单调变换，与内核一致。（选取高斯形式是为了平滑/稳定；理论下任何重叠原语的单调性代理都是可接纳的。）

### 2.3 红线（方法论约束）
该理论受到刻意约束。以下**不被允许**，且实现遵守它们：
- **(R1)** 最深的基座（感官-运动闭环 → 舒适度 → 被动因果记忆）不可替换。
- **(R2)** 仅两个区域可调：(a) 身体（感官/运动），(b) 感官需求状态如何塑造记忆需求状态。记忆需求状态**绝不直接设定**。
- **(R3)** 需求状态必须自涌现（仅经由内部通路）；它不是被指派的。
- **(R4)** 不引入*竞争*理论：无 RL 奖励信号，无自由能目标，无外部供给的目标。
- **(R5)** 外部数学（模糊集、分类、动力学系统）可用来回答*是什么*，绝不回答*想要什么*。
- **(R6)** 无神经网络，无预训练，无梯度，无逐游戏分支。
- **(R7)** 感知回答*是什么*，绝不回答*想要什么*。

*关于 NEED 与自涌现需求的澄清（化解表面张力）。* R2(a) 允许把**感官需求**设定点 `NEED` 作为身体参数调节——它是机体的内源稳态（温暖、中等光照、安静），而非设计者供给的目标。R3 的禁止专门适用于**记忆需求**状态（驱动记忆巩固的那部分内部塑造的需求）：它必须经由 I-2 通路自涌现，且绝不直接指派。因此固定的 `NEED` 与 R3 完全相容——*感官*需求是身体常数，*记忆*需求是自涌现的。

### 2.4 描述层级与基质无关性
猫智能论运作于 Marr 的**计算 / 功能层级**。神经递质（多巴胺、血清素……）属于*实现*层级（"生物实验心理学"），与理论的真伪无关——它们是基质细节。因此基座是**基质无关**的：它同样可以跑在猫脑上、硅基上或数字智能体上。这也正是该理论明确**不要求**睡眠或体力恢复（那些是实现层级的副产物）的原因；一个数字智能体二者都不需要。

---

## 3. HIM 内核（最简实现）

HIM 是一个约 119 有效行的参考内核，忠实实现 §2：
- **状态**：一个实时感官状态向量（离散化为一个*场景*键）。
- **舒适度（内在信号）**：规范信号是 §2.2 的**重叠驱动舒适度**——感官状态对 `NEED`（稳态锚点，在轨道 A 中主导）的稳态接近度。最简 HIM-0 内核另带一个**好奇**侧面：未见场景被赋予探索价值。这是被动记忆机制一个合法的、红线安全的涌现（无外部目标/奖励），也是驱动轨道 B 结构发现的动力；两个侧面并不冲突——重叠舒适度锚定稳态，新奇舒适度激发探索。
- **被动因果记忆**：`V[场景]` = 舒适度 EMA；`M[场景][动作]` = 后继价值的 EMA；`T[场景][动作]` = 观测到的后继计数（因果记忆）。
- **策略**：对 `M` 的一步前瞻（早期 ε-探索的贪心，后期利用）——新生儿混沌，成年体有目的。
- **STILL 动作**："什么都不做"是一个显式合法的运动模式（静止即运动模式，契合理论）。

R1–R7 全部遵守：零 NN、零梯度、零预训练、零外部奖励、零逐游戏分支；舒适度自涌现（I-2 通路）；外部数学回答*是什么*。

*范围边界。* 以上皆是 HIM 内核本身。建构在 HIM **之上**的模块——例如一个消费 HIM 自涌现的 `(感官, 舒适度)` 经验、以泛化到猫的局部记忆之外的外部回归器（见本文之外的独立*下一步工作*计划）——严格**位于**内核之外，且**不改变**其零 NN / 零梯度状态。此类附加物是基座主张（R1）的示范，而非 HIM 的一部分；内核的红线是在与它们隔离的条件下定义并被检验的。

---

## 4. 实验验证

所有实验在固定种子下确定可复现，仅需 `numpy`、`gymnasium` 与 `minigrid`。图与原始 JSON 随代码发布一同提供。

### 4.1 轨道 A — 规范测试台（`HIMGridEnv`，Gymnasium 兼容）
一个带舒适源的光滑感官场；忠实实例化 §2.1–2.2。

| 度量 | 结果 |
|---|---|
| 舒适度，前 500 步（新生、混沌） | **0.054** |
| 舒适度，末 500 步（已训练） | **0.378**（增益 **+0.324**） |
| 多种子稳健性（10 种子，环境与智能体种子均变化） | 增益 **+0.203 ± 0.190**；**10/10** 种子为正（符号检验 **p = 0.001**） |
| 消融：随机奖励信号，末 500 步 | **0.001**（增益来自重叠，而非偶然） |
| 价值跨世界一致性（地图 A → 地图 B） | Pearson **0.799**，MAE **0.032** |

跨世界结果是*"凭记忆辨认场景"*的经验陈述：需求状态跨世界固定，故 `V[场景]` 与世界无关；在地图 A 上训练出的价值图以 corr 0.799 预测地图 B 的舒适度，确认是场景辨认而非世界特定的死记。

两条诚实注记。**(i) 种子敏感性。** 头条 +0.324 是上四分位附近的一颗种子；在 10 次独立种子运行中，增益为 +0.203 ± 0.190（范围 0.010–0.573）——*方向*稳健（10/10，p = 0.001），*幅度*对种子高度敏感，因此我们报告分布而非最佳个案。**(ii) 轨迹是间歇性的，而非收敛性的。** 全程的中位瞬时舒适度 ≈ 0.00（63% 的采样步 < 0.05）：智能体在漫长的探索性游荡与返回舒适区之间交替，因此末端增益衡量的是*返回舒适区的频率*上升，而非持续驻留其中。这种探索-趋舒驱动的交替本身契合理论的双驱动（§2.1、§3）。

### 4.2 轨道 B — 公开基准交叉校验（MiniGrid）
我们把**同一** HIM 智能体移植到真实 MiniGrid（Farama），**忽略任务（外部目标）**，纯粹由内在新奇驱动——将 HIM 置于好奇心 / 内在动机文献的同一舞台。我们加入 **RND**（Random Network Distillation，Burda 等 2018）的**免依赖、线性预测器变体**：一个固定的随机目标网络，其表示由一个闭式岭回归预测器预测（无 torch、无 autograd）。这保留了 RND 的本质机制——*随机目标 + 可学习预测器 → 预测误差即新奇*——同时去除了深度网络依赖，从而使对比隔离出*内在动机思想*与其网络基质。三个智能体共用**同一套策略**；唯一区别是内在信号（HIM = 新奇计数 / 零 NN；RND = 线性预测器误差）。3000 步 × **10 种子**；数值为均值，标准差一并报告（并存于 `validation_results.json`）。

| 指标 | Empty-8×8（HIM / RND / Random） | FourRooms（HIM / RND / Random） |
|---|---|---|
| 格子覆盖（均值 ± 标准差） | 1.000 / 1.000 / 1.000 | 0.293 ± 0.044 / 0.305 ± 0.039 / 0.286 ± 0.056 |
| **转移覆盖**（结构广度，均值 ± 标准差） | 426 ± 4 / 430 ± 0 / 389 ± 15 | **767 ± 101 / 783 ± 100 / 628 ± 108** |
| 到达房间数（均值 ± 标准差） | 4.0 / 4.0 / 4.0 | 2.7 ± 0.46 / 3.3 ± 0.46 / 2.2 ± 0.87 |
| 因果记忆准确率（均值 ± 标准差） | 0.884 ± 0.005 / 0.884 ± 0.005 | 0.859 ± 0.022 / 0.844 ± 0.021 |

**解读。** 在无结构 Empty 世界中三者均饱和（符合预期）。在**有结构 FourRooms** 世界中，HIM（零 NN、被动记忆）取得转移覆盖 **767 ± 101**，基本追平其线性变体的 RND（**783 ± 100**）并显著超过随机（**628 ± 108**）。HIM–RND 之差远小于一个标准差，故中心经验主张成立：*一个零数据、零网络、舒适度驱动的智能体，在结构发现上达到（免依赖、线性的）RND 内在动机方法的水平。* 对 per-seed 转移覆盖的 Welch t 检验确认了这一解读：HIM 对 RND 统计上不可区分（双尾 p = 0.74），而二者均显著超过随机（HIM 对随机 p = 0.011；RND 对随机 p = 0.005；n = 10 种子）。在 10 种子下排序稳定：结构广度上 HIM ≈ RND ≫ Random。RND 唯一的优势在于到达房间数（3.3 对 2.7）与格子覆盖，可能因其连续误差奖励维持了更长视野的探索——这是一条具体、红线安全的 HIM 升级路径（以平滑新奇信号替换离散新奇计数）。

### 4.3 零数据、无预训练：一个构造性存在性证明

HIM 的头条主张是：一个智能体可以**无需任何外部训练数据、预训练权重或基于梯度的学习**而自涌现。这不是修辞上的断言，而是**构造性地证明**并获**执行级佐证**。

**构造性证明（代码级）。** HIM 是一件具体、完全可检视的成品（约 119 行）。对 HIM 智能体的静态扫描确立了以下事实（精确命令与输出在附录 A 复现）：

| 检视 | 排除的内容 | 在 HIM 上的结果 |
|---|---|---|
| 深度学习 import（`torch / tensorflow / neural / backprop / autograd / optim`） | 神经网络、梯度下降 | 仅有注明 *"no torch"* 的散文注释；**零 import** |
| 模型 / 权重加载（`load() / pickle / .pt / .h5 / .npy / read_csv / datasets`） | 预训练参数、外部数据集 | **零命中** |
| 记忆初始化（`self.V`、`self.M`） | 内嵌的世界知识 | 起始为**空** `{}`；仅一个中性 EMA 种子 `0.5` 与一个空访问计数器 |
| 训练循环 / 梯度步 | 离线或在线预训练 | HIM 智能体中**缺失** |

在计算机科学中，*"这里有一件展现该性质的具体成品"*就是此类成品**存在**的标准证明。成品即证明。

**执行级佐证。** 同一空白智能体，从空记忆出发，从零产生自涌现的学习：轨道 A 舒适度由 0.054 升至 0.378（混沌 → 有序寻求）；跨世界辨认 corr 0.799（基于记忆，而非死记）；轨道 B 结构发现广度追平 RND 基线，同时零网络。该行为明显是**没有**任何预训练喂入的情况下产生的。

**使主张严谨的原则性区分：结构先验 vs. 内容预训练。** HIM 确实包含*先验*，但它们专属于**结构性**——算法本身编码了理论（重叠率舒适度、被动因果记忆、一步前瞻），且对任一具体世界**不含任何经验内容**。这与**内容预训练**有本质区别，后者是在部署前灌入世界特定数据。生物猫类似地拥有先天的*结构*先验（感官需求、一具身体），却于出生后习得全部*内容*；HIM 的"空白新生儿"主张正立足于这一区分。中性 `0.5` 种子与固定的 `NEED` / `σ` 是红线 R2(a) 下的*身体参数*（先天生理），而非预训练：怀疑者说它们是先验是对的，但它们编码**零经验**，故并非数据预训练。

**证明的诚实边界。** 该证明确立的是*本实现*零内容预训练；它并不断言每个未来实例都将如此。它为成品证明了*存在性*与无内容预训练性质，建立在上述结构 / 内容先验区分之上——而非修辞。它**不**证明 HIM 是 AGI，也不证明它能扩展到 ARC-AGI；这些主张在 §5 被显式免责。

---

## 5. 为何 HIM 不为赢得 ARC-AGI 而设计（诚实范围）

ARC-AGI-3 计分的是**外部目标匹配效率**（RHAE）；尽管目标必须被*发现*，计分仍奖励*命中该被发现的目标*。我们的**红线 R4 禁止外部目标/奖励**。同一理论先前在 ARC 公开环境上的完整智能体实现，经验上停滞于 RHAE ≈ 0.675（25 关过 8 关），且在不违反 R4 的前提下无法触及排行榜顶端（约 1.03）。因此我们视 ARC 为一个*冒烟测试*（智能体能在真实交互环境中运行），并显式**不**将其作为理论的验证标尺。一个自涌现、内在驱动理论的验证标尺是结构发现（轨道 A/B），而非目标匹配。

---

## 6. 相关工作与独特性

该理论的*机制*并非各自新颖：生成认知 / 感官运动偶发性（O'Regan & Noë, 2001）、主动推理 / 自由能（Friston, 2010）、稳态 RL（Keramati & Gutkin, 2014）、Damasio 的稳态 / 躯体标记（1999）、Piaget 的感官运动阶段（1952）、Gibson 的可供性（1979）、Brooks 的"无表征智能"（1986）、Ashby 的稳态机（1952）、Braitenberg 的车辆（1984）、Grey Walter 的乌龟（1953），以及佛教的十二因缘 / 唯识（种子与储藏）与荀子的"好利恶害"皆预见了若干片段。**独特之处在于它们的合取**：一个 (a) 从*空白新生儿*出发、(b) 仅靠*被动*因果记忆学习、(c) 仅由单一可计算的*重叠率舒适度*驱动、(d) 可在约 119 行内跑通的极简内核。历史上的极简内核（Braitenberg、Walter、Ashby、Brooks）各自更小，但无一承载带有重叠率舒适度变量的完整"从空白学习"叙事。我们将 HIM 定位为一个*综合 / 统一极简基座*，而非对机制前所未有的主张。

### 6.1 理论谱系与本文定位
本文工作处于一条连贯的研究线，需明确各稿边界以免重复声明：
- **基石（已发表，Wang, 2018）：** 《反思智能：存在自主动机的最简机器模型设计》。以思辨与常识推理提出"机器自主动机"判据与"爱与恨"最简模型，是本理论的哲学与方法论原点。
- **架构框架（未发表手稿，HIM 单篇，中英双语；Wang, 2026）：** 《基于内稳态内驱力的自主智能体架构（HIM）：Homeostatic Intrinsic Motivation》。将理论落地为可计算的"舒适度梯度 ΔL"驱动与"希望机制"，并在 100×100 网格中对比主动推理（FEP）。该（中英双语）手稿是本稿 HIM 架构表述的直接前身。
- **本稿（投稿）：** 在基石的哲学原点与架构框架之上，贡献**构造性 + 经验性的"无内容预训练智能体存在"证明**、双轨可复现验证、红线可审计性与逐字节可复现性。本文不重复架构框架的 ΔL/希望机制论述，而是在其之上完成"能否无预训练存在"的证明。

---

## 7. 结论与"基座"主张

HIM 证明了一个空白出生、零数据、舒适度驱动的智能体，在明确排除网络、预训练、梯度与外部奖励的红线之下，能够自涌现一个世界模型并发现结构，达到神经网络内在动机基线的水平。我们将其发布为一个**极简、可复现的基座**——一个规范测试台加一个公开基准交叉校验——以便社区在其上构建、打破或扩展。按其设计，它并非外部目标基准的竞争者；其价值在于作为后 LLM 智能研究的一种替代架构基质。

---

## 8. 历史意义与展望（立场声明）

**针对规模公理的一个存在性证明。** 主流前提——*无海量数据即无智能*——由此从公理降级为可检验假设。一个空白出生、零数据、零网络的智能体，自涌现出场景辨认与结构发现，构造性地证明替代方案存在。

**复兴一条沉睡七十年的线。** Ashby、Walter、Brooks 与发展机器人学都曾寻求"从空白长出智能"，但停滞于不可复现的内核与缺失的测试台。HIM 补上了他们所缺的：一个 119 行可审计内核加一个双轨验证舞台，与内在动机文献同台。

**可证伪的预见。** *1–2 年（~80%）：* 被引为好奇级极简基准，而非范式转向；现实的切入点是**数据效率**随可爬取数据枯竭而凸显。*3–5 年（~40–50%）：* "HIM 探索、DL 消费"成熟为**作为数据引擎的发展式智能体**——融合路径，与基座主张（R1）一致。*10 年以上（~10–15%）：* 若在此类内核上叠出语言或跨域抽象，"经验主义 vs. 先验论"之争将获得一个**实验平台**——先天先验变成一个可调旋钮。*主要风险：* 若无人其上构建，则沦为被赞叹、被引用、被绕开的优雅脚注。

**一句话。** HIM 的意义不在胜过大模型——它不能——而在把"智能必须靠数据喂养"从公理降为假设，并为"智能能否从空白长出"这一古老问题造出第一台可复现的装置。问题开端处的纪念碑，而非答案终点的纪念碑。

---

## 参考文献

- Ashby, W. R. (1952). *Design for a Brain*. Chapman & Hall.
- Braitenberg, V. (1984). *Vehicles: Experiments in Synthetic Psychology*. MIT Press.
- Brooks, R. (1986). A robust layered control system for a mobile robot. *IEEE JRA*.
- Burda, Y., Edwards, H., Storkey, A., & Klimov, O. (2018). Exploration by Random Network Distillation. *arXiv:1810.12894*.
- Chevalier-Boisvert, M., et al. (2018/2023). MiniGrid / BabyAI. *arXiv:1807.09270*; Farama Foundation.
- Damasio, A. (1999). *The Feeling of What Happens*. Harcourt.
- Friston, K. (2010). The free-energy principle. *Nature Reviews Neuroscience*.
- Gibson, J. J. (1979). *The Ecological Approach to Visual Perception*. Houghton Mifflin.
- Grey Walter, W. (1953). *The Living Brain*. Duckworth.
- Keramati, M., & Gutkin, B. (2014). Homeostatic reinforcement learning. *Nature Communications*.
- O'Regan, J. K., & Noë, A. (2001). A sensorimotor account of vision. *BBS*.
- Piaget, J. (1952). *The Origins of Intelligence in Children*.
- Towers, M., et al. (2023). Gymnasium. *arXiv:2407.17032*.
- （以及哲学谱系：Schopenhauer、Spinoza、Freud、荀子、佛教阿毗达磨 / 唯识宗。）
- Wang, C. (2018). 反思智能: 存在自主动机的最简机器模型设计 [Reflective Intelligence: The Simplest Machine Model Design with Autonomous Motivation]. *人工智能与机器人研究 (Artificial Intelligence and Robotics Research)*, 7(1), 1–16. DOI: 10.12677/airr.2018.71001. （已发表，基石）
- Wang, C. (2026). 基于内稳态内驱力的自主智能体架构（HIM）：Homeostatic Intrinsic Motivation [Homeostatic Intrinsic Motivation (HIM): An Autonomous Agent Architecture Based on Homeostatic Drive]. 预印本（单篇，中英双语手稿，待 arXiv/Zenodo 标识）.

---

## 附录 A — 可复现性与发布

- **代码：** `him_env.py`（轨道 A）、`him_minigrid.py`（轨道 B，含 RND）、`run_validation.py`（双轨工具）。
- **环境：** Gymnasium 兼容的 `HIMGridEnv`；公开 MiniGrid（`MiniGrid-Empty-8x8-v0`、`MiniGrid-FourRooms-v0`）。
- **确定性：** 所有运行均设种子；原始指标在 `validation_results.json`；图在 `validation_fig.png`。
- **红线：** 在 §2.3 列为 R1–R7；内核按其构造遵守它们。
- **DOI：** 本稿 + 代码经 GitHub Release → Zenodo 归档，铸造可引用、不可变的 DOI。*想法*的优先权由同步发布的 arXiv 预印本锚定。

### A.1 无内容预训练检视（可审计）

§4.3 的构造性证明任何人可复现。从仓库根目录（`him_validation/`）：

```bash
# (1) HIM 不 import 任何深度学习框架（仅有散文注释说 "no torch"）
grep -rniE "torch|tensorflow|keras|neural|backprop|autograd|optim\." him_env.py him_minigrid.py run_validation.py
#   → 仅匹配注释；零 `import` 行

# (2) 无模型加载 / 预训练权重 / 外部数据集
grep -rniE "load\(|pickle|\.pt|\.h5|\.npy|read_csv|datasets" him_env.py him_minigrid.py run_validation.py
#   → 零命中

# (3) HIM 记忆初始为空；唯一初始数字是一个中性 EMA 种子 0.5
grep -nE "self\.V = \{\}|self\.M = \{\}" him_env.py him_minigrid.py
#   → self.V = {}   self.M = {}   （出生即空白）

# (4) HIM 智能体文件中无任何训练循环 / 梯度步
grep -rniE "gradient|\.train\(|fit\(|SGD|Adam|backward\(" him_env.py him_minigrid.py
#   → 零命中
```

这四条检查是存在性证明的代码级一半；执行级一半是 §4.1–§4.2 的结果。二者共同确立所发布成品包含**零内容预训练**——仅含结构先验（编码在算法中的理论）与先天身体参数（红线 R2(a)）。

> **投稿前 TODO：** (1) 替换 `[您的姓名]`；(2) 将此 markdown 转为 LaTeX（数学部分已内联兼容 `\usepackage`）；(3) 将 `validation_fig.png` 嵌入为图 1；(4) 确认 Zenodo/GitHub 关联与 arXiv 投稿日期；(5) 添加 ORCID / 联系方式。
