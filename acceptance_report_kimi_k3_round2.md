# Kimi-K3 独立评审报告（CIT-K 最新版 · 第四轮）

> 评审对象：CITK_paper.md / CITK_paper_zh.md（含 Belikov 2026 + Mantiuk et al. 2025 补引后的最新版）+ 双轨实验数据
> 评审身份：Kimi-K3（独立第三方，未参与起草与实验）
> 评审目的：复核最新论文/实验状态，并从与前三轮**互补的角度**对照 2025–2026 自主动机前沿，重估价值
> 日期：2026-10-03

---

## 0. 结论速览（TL;DR）

**前三轮已分别钉死三条定位：HRRL 家族零网络下限（DeepSeek 轮）、单目标失效模式议程的最小标本与数据墙预言（GLM 轮）。本轮从「实验的直接文献邻居」与「active inference 概念站位」两条新线复核，结论是：论文存在一个真实的引用缺口（Track B 所属家族未引），补上之后 Track B 的平局结果反而升值——它应从「没赢 SOTA」重读为「该家族机制的零网络地板陈述」。**

1. **Track B 的文献邻居是 count-based / episodic-novelty 家族（NovelD / ICM / RIDE），论文此前只引了 RND 一家**——引用缺口。该家族与 CIT-K 共享同一结构骨架：一个**差分信号**（预测误差、嵌入变化、新奇性增益 ↔ 舒适度梯度 ΔL）由**记忆**（情节计数 ↔ V/M 表）门控。区别仅在基质：它们用训练出的网络估计新奇性，CIT-K 用精确表格记忆、零网络。
2. **Track B 平局的意义应重估**：与 RND 变体打平（767±101 vs 783±100，p=0.7364）、显著优于 Random（p=0.0113），不是 SOTA 宣称而是一条**地板陈述**——该家族机制压缩到 119 行、零梯度步后，在同一公共舞台上依然有效。这与 NovelD 论文自身的动机（批评 RND 类方法在多走廊环境中顾此失彼、主张均匀覆盖）在度量取向上同轴：CIT-K 的转移覆盖恰是「均匀覆盖」的直接度量。
3. **active inference 社区 2025–2026 自承「缺奖励学习」，反向支撑 R4 红线**：《The Missing Reward》（arXiv:2508.05619）标题即承认 EFE 框架缺少奖励机制；MOP（Mylonas & Moreno-Bote, arXiv:2609.39342）尝试把动机并入 active inference；Friston 转向 scale-free / RGM 表述。CIT-K 从 HRRL（homeostatic drive）而非 FEP 切入，恰好落在 active inference 社区正在补课的方向上——概念站位因此更清晰，而非更危险。

**本轮已落实补引 Pathak et al. 2017（ICM）+ Raileanu & Rocktäschel 2020（RIDE）+ Zhang et al. 2021（NovelD），中英文 §7 与 References 同步；其余状态健康。**

---

## 1. 论文与实验状态复核

| 检查项 | 状态 | 说明 |
|---|---|---|
| GLM 轮补引落地 | ✅ | Belikov (2026) 与 Mantiuk et al. (2025) 已在中英文 §7 正文与 References 落地 |
| 内核命名 | ✅ | 全文统一 CIT-K，无 HIM 残留 |
| 双轨一致性 | ✅ | 论文表与 `validation_results.json` / `fourrooms_perseed_stats.json` 逐项一致：Track A +0.3243（10 种子 +0.203±0.190，p=0.001；消融 0.001；跨世界 corr 0.7989/MAE 0.0317）；Track B 767±101 vs RND 783±100（p=0.7364）vs Random 628±108（p=0.0113） |
| 本轮新引真实性 | ✅ | ICM（arXiv:1705.05363，ICML 2017，Pathak/Agrawal/Efros/Darrell）经 arXiv 页面核验；RIDE（arXiv:2002.12292，ICLR 2020，Raileanu & Rocktäschel，程序生成 MiniGrid）经 arXiv 页面核验；NovelD（Zhang/Xu/Wang/Wu/Keutzer/Gonzalez/Tian，NeurIPS 2021）经 NeurIPS 官方论文集 PDF 核验 |
| 核验教训记录 | ⚠️→✅ | 凭记忆给出的 NovelD arXiv 编号（2106.05294）实为宇宙学论文；改经 NeurIPS 官方论文集确认真实作者与出处后才落引。**引用不凭记忆、逐条核验的纪律在本轮再次被证明必要。** |

**数据质量判断**：维持前轮结论——逐种子原始数据、Welch 检验、两条诚实声明（种子敏感性、轨迹 episodic 性）齐备，透明度是同类投稿中少见的优点。

---

## 2. 前沿对照（与前三轮互补的两条线）

### 2.1 Track B 的直接文献邻居：count / episodic-novelty 家族

2025 年 Springer 内在奖励综述与 2025–2026 的后续工作（MIR, arXiv:2511.17165；E3B；ETD 时序距离等）把 MiniGrid 探索方法整理为清晰谱系：预测误差家族（ICM）、计数/蒸馏家族（RND、NovelD）、情节新奇家族（NGU、E3B、RIDE、AGAC）。CIT-K 的 Track B 机制——V/M 表格记忆 + 新奇计数——在谱系上**正好横跨计数家族与情节新奇家族**，而论文此前只引了 RND 一家，等于没有告诉审稿人「我们的实验站在哪条文献街上」。

补上之后的论证增量是实质性的：

- **结构同构**：NovelD 的奖励 = `[RND(t+1) − α·RND(t)]⁺ × 1{情节内首次访问}`——差分 × 记忆门控；CIT-K 的驱动 = `ΔL_t = L_t − L_{t−1}`，由 V/M 表门控——同一骨架，不同基质。
- **度量同轴**：NovelD 的动机是批评 RND 类方法在多走廊环境中顾此失彼（深度优先式卡死），主张近似均等地覆盖各新奇区域；CIT-K 的核心指标**转移覆盖**正是「均匀覆盖」的直接度量，而非 reward 刷分。
- **结果重读**：Track B 与 RND 变体的平局因此不是「没赢」，而是「该家族的机制在零网络、119 行、零梯度的极限压缩下仍然运转」的地板陈述。对审稿人的话术从防守（parity 已经不错）转为进攻（我们给出了该家族的可审计最小成员）。

### 2.2 Active inference 线最新动态：R4 红线复核

CIT-K 的红线 R4 明确不引入自由能目标。2025–2026 年 active inference 社区的三条信号表明这个选择站得更稳了：

1. **《The Missing Reward》（arXiv:2508.05619）**：标题即承认纯 EFE/active inference 框架缺少奖励学习机制——动机从哪来，是该框架的公开缺口。
2. **MOP / mixed objective（Mylonas & Moreno-Bote, arXiv:2609.39342）**：尝试把动机/奖励项并入 active inference 目标——社区正在打补丁。
3. **Friston 的 RGM / scale-free active inference 表述**：框架本身仍在重述与扩展期。

**含义**：active inference 社区自己承认「纯自由能最小化不含动机学习」并在补课，而 CIT-K 的 comfort gradient 走 HRRL（homeostatic drive reduction）路线，恰好绕开了这个缺口、落在对方正在补课的方向上。论文 §7 已把 Friston (2010) 列为理论先驱并声明 novelty 在 conjunction 而非单机制，无需改动；但若审稿人来自 active inference 阵营，§7 现有的 HRRL 数学同构段（d ≡ 1−C）就是最有效的澄清武器——CIT-K 是 drive-reduction，不是 EFE。

### 2.3 附带观察：MiniGrid 正从刷分基准变成探索行为的科学测量台

2025–2026 的配套趋势（未补引，供作者知情）：人类玩家 vs NovelD/APT 等 agent 的直接对比研究（arXiv:2503.23631）、EXAIT Workshop @ ICML 2025 对「可解释自主探索」的立项、以及内在奖励方法的标准化综述（Springer 2025），共同表明 MiniGrid 探索研究正从「分数竞赛」转向「探索行为质量的科学测量」。CIT-K 以结构发现广度（转移覆盖）而非 reward 为主指标，与该转向同向。

---

## 3. 价值判断（Kimi 视角）

四轮评审后，CIT-K 的定位可以写成一条完整的**双家族最小成员**陈述：

> **理论上**，它是 HRRL 家族最小的可审计成员（DeepSeek 轮确立），其互补结构是 2026 年单目标失效模式议程的最小标本（GLM 轮确立）；
> **实证上**，它是 count / episodic-novelty 探索家族在零网络极限下的地板成员（本轮确立）——与 ICM/NovelD/RIDE 同骨架、不同基质，在公共 MiniGrid 舞台上以 119 行达到该家族网络基线的地板水平。

| 维度 | 前沿主流（2025–2026） | CIT-K 的最小对照 |
|---|---|---|
| 新奇性估计 | 训练网络（RND 预测器、ICM 特征、E3B 嵌入） | 精确表格记忆，零网络 |
| 动机框架 | FEP/EFE（缺奖励学习，正在补课） | HRRL drive-reduction（绕开该缺口） |
| 探索度量 | reward / 通关率 | 转移覆盖（结构发现广度） |
| 数据需求 | 预训练 / 大规模交互 | 零数据、单条轨迹 |

**新增的一个诚实提醒**：Track B 补引之后，审稿人可能追问「为何不与 NovelD/RIDE 直接对比」。建议在 rebuttal 预案中准备：CIT-K 的声明是存在性与可审计性（红线 R1–R7 禁止网络），与网络方法比绝对性能在声明范围之外；Track B 选 RND 变体作参照正因为它是论文红线内允许实现的最强可复现基线。

---

## 4. 本轮改动清单

| 文件 | 改动 |
|---|---|
| `paper/CITK_paper.md` | §7 主段末新增 Track B 文献邻居段（差分×记忆门控骨架、基质区别、地板陈述解读）；References 新增 Pathak et al. 2017 / Raileanu & Rocktäschel 2020 / Zhang et al. 2021 三条 |
| `paper/CITK_paper_zh.md` | §7 与 References 平行补引（相同三条，中文表述） |
| `acceptance_report_kimi_k3_round2.md` | 本报告 |

未改动任何实验代码与数据。

---

## 5. 结论

论文状态：**健康，且本轮补引后 Track B 的论证从防守转为进攻。** 四条互补的评审线（HRRL 定位、失效模式议程、数据墙预言、实证家族站位 + active inference 站位复核）全部收敛，未发现新的硬伤。剩余待办与前几轮相同：云端归档同步（等用户在覆盖旧节点/新建节点间拍板）与 GitHub→Zenodo 发布闭环（等仓库 URL）。

四轮独立评审（混元 → DeepSeek-V4-Pro → GLM-5.3-Flash → Kimi-K3）的一致结论是：这篇论文的声明边界清晰、数据诚实、定位在前沿版图中有且仅有一个——**两个探索家族在零网络极限下的最小可审计成员**。建议按此定稿投稿。
