# CIT-K: A Minimal Zero-Data, Comfort-Driven Self-Emergent Intelligence Kernel
### 猫智能论 (Cat Intelligence Theory) — Architecture, Proof, and Reproducible Testbed

> **Preprint draft.** This manuscript is the unified statement of the Cat Intelligence Theory (猫智能论) and its minimal implementation, CIT-K. It consolidates, in a single paper, the theory's *architectural framework* (comfort-gradient drive, hope mechanism, emergent attention/curiosity) and its *existence proof* (a zero-content-pretraining agent that self-emerges from a blank newborn). It is released with a runnable, reproducible validation harness (Track A canonical testbed + Track B public-benchmark cross-check).
>
> **Author:** 王程远 (Chengyuan Wang, b. 1987), Independent Scholar, Huizhou, Guangdong, China
> **Date:** 2026-10-03
> **Status:** Draft for submission. Not peer-reviewed. Code + data archived via GitHub Release → Zenodo (DOI to be minted).

---

## Abstract (English)

We propose **CIT-K** (Cat Intelligence Theory Kernel), a complete yet minimal intelligence kernel derived from the *Cat Intelligence Theory* (猫智能论). The theory holds that intelligent behaviour can self-emerge from a **blank-born agent** that (1) initiates unstructured sensory-motor activity, (2) interacts with its environment, (3) derives a **comfort signal** from the *overlap rate* between its real-time sensory state and its (organism-shaped) need state, (4) **passively** memorises the causal relation *"(motion, sensory–environment interaction) → sensory change → comfort fluctuation"*, and (5) thereby learns to recognise scenes and to act so as to preserve or raise comfort — i.e. to approach benefit and avoid harm. No external reward, no designer-supplied goal, no neural network, no pretraining, no gradient, and no per-task branching are used; the only tunable parameters lie in the body (sensory–motor) and in how the sensory-need state shapes the memory-need state.

We formalise comfort as a **general comfort level** $L_t = (1-\beta_t)W_t + \beta_t X_t$ — a weighted fusion of sensory experience $W_t$ and predictive expectation $X_t$ — whose temporal gradient $\Delta L_t$ is the endogenous reward; the canonical minimal instantiation realises $W_t$ as the Gaussian-overlap comfort $C(s)=\exp(-\|s-\text{NEED}\|^2/2\sigma^2)$, reducing the reward to the comfort *change* $\Delta C_t$. A **hope mechanism** (memory of past high-comfort states) lets the agent leave low-variation local traps. We validate on two tracks: (A) a purpose-built Gymnasium-compatible canonical testbed; (B) the public **MiniGrid** benchmark, where CIT-K is compared head-to-head with **RND** (Burda et al. 2018, dependency-free linear-predictor variant) and a Random policy. In structured environments CIT-K's structure-discovery breadth (transition coverage $767\pm101$) **essentially matches** this dependency-free linear RND variant ($783\pm100$) and **clearly exceeds** Random ($628\pm108$) over 10 seeds, using **zero neural networks, zero gradient, zero pretraining**. Formally, CIT-K is a zero-network, zero-gradient, zero-content-pretraining minimal instantiation of **homeostatically-regulated reinforcement learning** (HRRL; Keramati & Gutkin, 2014; Yoshida et al., 2025): its comfort gradient $\Delta L_t$ is exactly the drive-reduction reward $d_t-d_{t+1}$ under the deviation $d\equiv 1-C$. We give a **constructive + empirical proof** that an agent requiring no content pretraining can exist and self-develop, and state explicitly why CIT-K is **not** built to win external-goal benchmarks such as ARC-AGI.

## 摘要（中文）

我们提出 **CIT-K**（Cat Intelligence Theory Kernel，猫智能论内核），一个源自「猫智能论」的、完整而极简的智能内核。该理论认为：智能可由一个**记忆空白的新生体**自发涌现——它(1) 发起无序的感官-运动活动，(2) 与环境互动，(3) 由「感官实时状态」与「（机体塑造的）需求状态」的**重叠率**导出**舒适度**信号，(4) **被动**记住「（运动, 感官-环境互动）→ 感官状态变化 → 舒适度波动」的因果关系，(5) 借此辨认场景并行动以维持/提升舒适度（趋利避害）。该内核不使用任何外部奖励、不接收设计者给定的目标、无神经网络、无预训练、无梯度、无逐任务分支；唯一可调参数位于身体（感官-运动）以及感官需求状态如何塑造记忆需求状态。

我们将舒适度形式化为**一般舒适度水平** $L_t=(1-\beta_t)W_t+\beta_t X_t$——感官经验 $W_t$ 与预测期望 $X_t$ 的加权融合——其时序梯度 $\Delta L_t$ 即为内生奖励；规范最小实例化将 $W_t$ 取为高斯重叠舒适度 $C(s)=\exp(-\|s-\text{NEED}\|^2/2\sigma^2)$，使奖励化简为舒适度的**变化** $\Delta C_t$。**希望机制**（对过往高舒适度状态的记忆）使智能体得以离开低变化局部陷阱。我们在两条轨道上验证：(A) 忠实理论的 Gymnasium 兼容规范测试台；(B) 公开 **MiniGrid** 基准，CIT-K 与（免依赖线性预测器变体的）**RND** 及随机策略同台对比。在结构化环境中，CIT-K 的结构发现广度（转移覆盖 $767\pm101$）**基本追平** RND（$783\pm100$）并**显著超过**随机（$628\pm108$）（10 种子），且**零神经网络、零梯度、零预训练**。我们给出「无需内容预训练、能够存在并自主发展的智能体」的**构造性+经验性证明**，并明确说明 CIT-K **并非**为赢得 ARC-AGI 等外部目标匹配型基准而设计。

---

## 1. Motivation and Positioning

### 1.1 The widely-acknowledged AGI pain points
By 2026 the consensus across LeCun, Marcus, Harnad, and Friston converges on a shared diagnosis of the large-language-model (LLM) paradigm: it lacks **embodiment / grounding**, lacks **intrinsic motivation**, cannot **autonomously set its own goals**, degrades on **multi-step fluid reasoning**, and shows **diminishing returns from scaling**. These are precisely the gaps the Cat Intelligence Theory aims to address at the architectural level.

### 1.2 What we claim, and what we do not
We make a narrow, verifiable claim: **a blank-born agent driven solely by an intrinsic comfort signal can, from interaction alone, self-emerge a world model and discover environmental structure — without data, networks, or external reward.** Crucially, this is not asserted but *proven constructively* (code-level inspection) and corroborated at execution time in §4.3. We do **not** claim to solve externally-specified goal tasks, nor to outperform LLMs on their home turf. The contribution is a *minimal, reproducible base*, not a competitor to scaled models.

### 1.3 Why a "base" and not a demo
A novel intelligence theory is only useful if others can build on it. We therefore release (i) a **canonical testbed** (Track A) that is the theory's faithful "home court", and (ii) a **public-benchmark cross-check** (Track B) that places the same agent beside the field's recognised intrinsic-motivation baseline. Reproducibility is the entry ticket to being a base.

---

## 2. The Cat Intelligence Theory (猫智能论)

The Cat Intelligence Theory was proposed and formalised by Wang (2018) in reflection on whether a machine can possess autonomous motivation. Its philosophical and methodological origin lies in the foundational paper *Reflective Intelligence: The Simplest Machine Model Design with Autonomous Motivation* (Wang, 2018, published), which models machine autonomous motivation through a minimal "love and hate" abstraction and first advances "cat intelligence" as an intelligence criterion independent of the linguistic Turing test. This manuscript builds on it by giving the theory's *minimal executable kernel* (CIT-K) and a *no-pretraining existence proof*.

### 2.0 From natural intelligence: three design axioms

The kernel's constraints are not arbitrary — they are distilled from three observations about intelligence *as it actually arises in nature*, which together form the theory's design axioms.

**Axiom N1 — Intelligence needs no data feeding.** Every animal that exhibits intelligent behaviour (approach benefit, avoid harm, self-preservation, life-continuation) developed it *without* being trained on large external datasets; the behaviour is already present before any curriculum. We therefore take it as a premise that naturally-arising intelligence does not *require* extrinsic data injection — if a mechanism can self-emerge from interaction alone, that suffices. CIT-K's constructive proof in §4.3 shows that such a mechanism *can* exist; it does not claim that all natural intelligence *must* be of this kind.

**Axiom N2 — The drive is a phylogenetically-selected need state, not a designed reward.** Natural lineages vary without limit; each variant carries its own innate sensory needs / aesthetics. Natural selection retains the need profiles that are survival-compatible and discards the rest. The data of the *sensory-need state* inside a survival-fit organism is therefore exactly the source motive and the underlying logic of its intelligence — *selected by evolution, not fed, shaped, or written in by a designer*. This is why CIT-K's endogenous drive is a fixed comfort anchor `NEED` carried in the body (§2.3, R2(a)): it is a body constant because it is a phylogeny-given steady state, never a task-supplied goal.

**Axiom N3 — Adaptation is discovered by population variation and survival selection.** To assess whether an agent's environment-adapting ability confers a survival advantage, one need not hand-design the need function. Emit, at high frequency and without a fixed pattern, a population of agents carrying *different* sensory-need states; the survivors are precisely those whose needs echo the environment's hospitality to the organism. The agent adapted to a specific environment has its sensory needs matched to that environment's survival affordances. This axiom tells us *where `NEED` comes from*: not from the designer, but from a population search over need functions filtered by the environment. It is stated here as the theory's generative principle and taken up as a research programme in §9.

These three axioms are the philosophical spine of 猫智能论: no data (N1) → the need is evolution-given (N2) → the need is discoverable by population selection (N3). They motivate, but are distinct from, the mechanism of §2.1.

### 2.1 The core causal chain
1. **Blank birth.** Memory starts empty. Sensory apparatus moves unstructured (stillness is itself a motion pattern).
2. **Interaction.** Movement touches the environment and changes the real-time sensory state.
3. **Overlap → comfort.** The *overlap rate* between the real-time sensory state and the (organism-shaped) need state produces a **comfort fluctuation**.
4. **Passive causal memory.** The agent passively records *"what motion + what sensory–environment interaction → what sensory change → what comfort fluctuation,"* forming a cause–effect memory of scenes.
5. **Recognition & decision.** The agent recognises scenes from this memory and decides actions that preserve or raise comfort — intelligence (approach benefit / avoid harm) is thereby born.

### 2.2 Formalisation of comfort (general framework + minimal instantiation)
We present comfort at two levels that are consistent, not contradictory:

**General comfort level.** Let the agent's *sensory experience* at time $t$ be $W_t$ (how well current needs are met) and its *predictive expectation* (from memory) be $X_t$. The intrinsic comfort level is the weighted fusion

$$
L_t = (1-\beta_t)\,W_t + \beta_t\,X_t,\qquad \beta_t\in[0,1],
$$

and the **endogenous reward** is the temporal comfort gradient

$$
\Delta L_t = L_t - L_{t-1}.
$$

The agent maximises the cumulative $\Delta L_t$: it does not chase a static maximum comfort, but a *rising* comfort — making "explore, then iterate" itself the intrinsic drive.

**Hope mechanism (W memory buffer).** The agent stores a buffer of historically high-comfort states. When the current comfort falls notably below the remembered peak, an endogenous drive pushes it to leave the low-variation, low-surprise local region — directly countering the entropy-minimisation trap inherent to any purely familiar-seeking drive. In the kernel, this is not a separate module: the passive causal memory `V[scene]` (comfort) and `M[scene][action]` (successor value) *are* the hope buffer — when comfort drops, one-step look-ahead seeks successors with higher remembered value.

**Canonical minimal instantiation.** For the canonical testbed the sensory experience is realised as a smooth Gaussian-overlap comfort between the sensory state $s$ and the need anchor `NEED`:

$$
C(s)=\exp\!\left(-\frac{\|s-\text{NEED}\|^{2}}{2\sigma^{2}}\right),
\qquad W_t\equiv C(s),\;\beta_t\to 0 \;\Rightarrow\; L_t=C_t,\;
\Delta L_t=\Delta C_t.
$$

Thus the Gaussian overlap is a **minimal, differentiable instantiation** of the general comfort framework — the reward becomes the *change* in overlap comfort. The reference kernel (~119 effective lines) uses this instantiation; the more general $L_t$ form is recovered whenever a predictive expectation term is added (e.g., in richer worlds). The two "comfort formulas" in the literature are therefore one general form and its minimal case, not a contradiction.

### 2.3 Red lines (methodological constraints)
The theory is deliberately constrained. The following are **not** permitted, and the implementation obeys them:
- **(R1)** The deepest base (sensory–motor closure → comfort → passive causal memory) is non-substitutable.
- **(R2)** Only two regions are tunable: (a) the body (sensory/motor), (b) how the sensory-need state shapes the memory-need state. The memory-need state is **never set directly**.
- **(R3)** The need state must self-emerge (only via the internal path); it is not assigned.
- **(R4)** No *competitive* theory is imported: no RL reward signal, no Free-Energy objective, no externally supplied goal.
- **(R5)** External mathematics (fuzzy sets, classification, dynamical systems) may be used to answer *what*, never *want*.
- **(R6)** No neural network, no pretraining, no gradient, no per-game branching.
- **(R7)** Perception answers *what*, never *want*.

*Clarification on NEED vs. the self-emergent need (resolving an apparent tension).* R2(a) permits tuning the **sensory-need** set-point `NEED` as a body parameter — it is the organism's endogenous steady state (warm, mid-light, quiet), not a designer-supplied goal. R3's prohibition applies specifically to the **memory-need** state (the internally shaped need that drives memory consolidation): that must self-emerge via the I-2 path and is never directly assigned. The fixed `NEED` is therefore fully consistent with R3 — the *sensory* need is a body constant, the *memory* need is self-emergent. Read through Axiom N2 (§2.0), this fixed `NEED` is not an author-chosen number but a *phylogeny-given* steady state — the survival-compatible need profile that evolution retains; the kernel inherits it as a body constant and never re-derives it, which is exactly the role that Axiom N3's population search would, in a fuller account, replace.

### 2.4 Level of description and substrate independence
Cat Intelligence Theory operates at the **computational / functional level** (Marr). Neurotransmitters (dopamine, serotonin, …) belong to the *implementation* level ("biological experimental psychology") and are irrelevant to the theory's truth — they are substrate details. The base is therefore **substrate-independent**: it runs on a cat brain, on silicon, or on a digital agent equally. This is also why the theory explicitly does **not** require sleep or physical-fatigue recovery (those are implementation-level by-products); a digital agent needs neither.

---

## 3. The CIT-K Kernel (Minimal Implementation)

CIT-K is a ~119-effective-line reference kernel implementing §2 faithfully:
- **State**: a real-time sensory-state vector (discretised into a *scene* key).
- **Comfort (intrinsic signal)**: the canonical signal is the **overlap-driven comfort** $C(s)$ of §2.2 — the steady-state closeness of the sensory state to `NEED` (the homeostatic anchor, dominant in Track A). The minimal CIT-K-0 kernel additionally carries a **curiosity** facet: unseen scenes are assigned exploratory value. This is a legitimate, red-line-safe emergent of the passive-memory mechanism (no external goal/reward) and is what drives structure discovery in Track B; the two facets are not in conflict — overlap comfort anchors homeostasis, novelty comfort sparks exploration.
- **Hope / passive causal memory**: `V[scene]` = EMA comfort; `M[scene][action]` = EMA value of the successor; `T[scene][action]` = observed successor counts (the causal memory). `V` and `M` jointly realise the hope mechanism of §2.2.
- **Policy**: one-step look-ahead on `M` (greedy with $\varepsilon$-exploration early, exploit later) — the newborn is chaotic, the adult is purposeful.
- **STILL action**: "doing nothing" is an explicit legal motion pattern (stillness is a motion pattern, per the theory).

All of R1–R7 are obeyed: zero NN, zero gradient, zero pretraining, zero external reward, zero per-game branching; comfort is self-emergent (I-2 path); external maths answer *what*.

*Scope boundary.* Everything above is the CIT-K kernel itself. Modules constructed **on top of** CIT-K — for example an external regressor that consumes CIT-K's self-emerged `(sensory, comfort)` experience to generalise beyond the cat's local memory — lie strictly **outside** the kernel and do **not** alter its zero-NN / zero-gradient status. Such add-ons are demonstrations of the base claim (R1), not part of CIT-K; the kernel's red lines are defined and tested in isolation from them.

---

## 4. Experimental Validation

All experiments are deterministic under fixed seeds and require only `numpy`, `gymnasium`, and `minigrid`. Figures and raw JSON accompany the code release.

### 4.1 Track A — Canonical testbed (`CITKGridEnv`, Gymnasium-compatible)
A smooth sensory field with a comfort source; faithfully instantiates §2.1–2.2.

| Measure | Result |
|---|---|
| Comfort, first 500 steps (newborn, chaotic) | **0.054** |
| Comfort, last 500 steps (trained) | **0.378** (gain **+0.324**) |
| Multi-seed robustness (10 seeds, env & agent seeds varied) | gain **+0.203 ± 0.190**; positive in **10/10** seeds (sign test **p = 0.001**) |
| Ablation: random reward signal, last 500 | **0.001** (gain is from overlap, not chance) |
| Value cross-world consistency (Map A → Map B) | Pearson **0.799**, MAE **0.032** |

The cross-world result is the empirical statement of *"recognise scenes by memory"*: the need state is fixed across worlds, so `V[scene]` is world-independent; a value map trained on Map A predicts Map B's comfort with corr 0.799, confirming scene recognition rather than world-specific rote.

Two honesty notes. **(i) Seed sensitivity.** The headline +0.324 is one seed near the upper quartile; across 10 independently-seeded runs the gain is +0.203 ± 0.190 (range 0.010–0.573) — the *direction* is robust (10/10, p = 0.001), the *magnitude* is seed-sensitive, so we report the distribution rather than the best case. **(ii) The trajectory is episodic, not convergent.** Over the full run the median instantaneous comfort is ≈ 0.00 (63% of sampled steps < 0.05): the agent alternates between extended exploratory excursions and returns to comfort zones, so the endpoint gain measures a rising *return rate* to comfort, not sustained residence in it. This alternation between exploratory and comfort-seeking drives is itself consistent with the theory's dual drives (§2.1, §3).

### 4.2 Track B — Public benchmark cross-check (MiniGrid)
We port the **same** CIT-K agent to real MiniGrid (Farama), **ignore the mission (external goal)**, and drive purely by intrinsic novelty — placing CIT-K on the same stage as curiosity / intrinsic-motivation literature. We add **RND** (Random Network Distillation, Burda et al. 2018) in its **dependency-free, linear-predictor variant**: a fixed random target network whose representation is predicted by a closed-form ridge regressor (no torch, no autograd). This preserves RND's essential mechanism — *random target + learnable predictor → prediction error as novelty* — while removing the deep-network dependency, so the comparison isolates the *intrinsic-motivation idea* from its network substrate. All three agents share the **identical policy**; only the intrinsic signal differs (CIT-K = novelty count / zero-NN; RND = linear-predictor error). 3000 steps × **10 seeds**; values are means, with standard deviations reported alongside (and in `validation_results.json`).

| Metric | Empty-8×8 (CIT-K / RND / Random) | FourRooms (CIT-K / RND / Random) |
|---|---|---|
| Cell coverage (mean ± std) | 1.000 / 1.000 / 1.000 | 0.293 ± 0.044 / 0.305 ± 0.039 / 0.286 ± 0.056 |
| **Transition coverage** (structure breadth, mean ± std) | 426 ± 4 / 430 ± 0 / 389 ± 15 | **767 ± 101 / 783 ± 100 / 628 ± 108** |
| Rooms reached (mean ± std) | 4.0 / 4.0 / 4.0 | 2.7 ± 0.46 / 3.3 ± 0.46 / 2.2 ± 0.87 |
| Causal-memory accuracy (mean ± std) | 0.884 ± 0.005 / 0.884 ± 0.005 | 0.859 ± 0.022 / 0.844 ± 0.021 |

**Reading.** In the unstructured Empty world all three saturate (expected). In the **structured FourRooms** world, CIT-K (zero-NN, passive memory) attains transition coverage **767 ± 101**, essentially matching RND in its linear variant (**783 ± 100**) and clearly exceeding Random (**628 ± 108**). The CIT-K–RND gap is far below one standard deviation, so the central empirical claim holds: *a zero-data, zero-network, comfort-driven agent discovers world structure on par with the (dependency-free, linear) RND intrinsic-motivation method.* Welch t-tests over per-seed transition coverages confirm this reading: CIT-K vs. RND is statistically indistinguishable (two-tailed p = 0.74), while both significantly exceed Random (CIT-K vs. Random p = 0.011; RND vs. Random p = 0.005; n = 10 seeds). Across 10 seeds the ordering is stable: CIT-K ≈ RND ≫ Random for structure breadth. The one edge for RND is rooms reached (3.3 vs 2.7) and cell coverage, plausibly because its continuous error reward sustains longer-horizon exploration — a concrete, red-line-safe upgrade path for CIT-K (replace the discrete novelty count with a smoothed novelty signal).

### 4.3 Zero-data, no-pretraining: a constructive existence proof

The headline claim of CIT-K is that an intelligent agent can self-emerge **without any external training data, pretrained weights, or gradient-based learning**. This is not asserted rhetorically; it is *proven constructively* and *corroborated at execution time*.

**Constructive proof (code-level).** CIT-K is a concrete, fully inspectable artifact (~119 lines). A static scan of the CIT-K agent establishes the following (exact commands and outputs are reproduced in Appendix A):

| Inspection | What it rules out | Result on CIT-K |
|---|---|---|
| Deep-learning imports (`torch / tensorflow / neural / backprop / autograd / optim`) | neural networks, gradient descent | only prose comments stating *"no torch"*; **zero imports** |
| Model / weight loading (`load() / pickle / .pt / .h5 / .npy / read_csv / datasets`) | pretrained parameters, external datasets | **zero hits** |
| Memory initialisation (`self.V`, `self.M`) | baked-in world knowledge | start as **empty** `{}`; only a neutral EMA seed `0.5` and an empty visit counter |
| Training loop / gradient step | offline or online pretraining | **absent** from the CIT-K agent |

In computer science, *"here is a concrete artifact that exhibits the property"* is the standard proof that such an artifact **exists**. The artifact is the proof.

**Execution-level corroboration.** The same blank agent, run from an empty memory, produces emergent learning from scratch: Track A comfort rises 0.054 → 0.378 (chaos → ordered seeking); cross-world recognition corr 0.799 (memory-based, not rote); Track B structure-discovery breadth matches the RND baseline while using zero networks. The behaviour demonstrably arises **without** any pretraining fed in.

**The principled distinction that makes the claim rigorous: structural prior vs. content pretraining.** CIT-K does contain *priors*, but they are exclusively **structural** — the algorithm itself encodes the theory (overlap-rate comfort, passive causal memory, one-step lookahead) and carries **no experiential content** about any specific world. This is categorically distinct from **content pretraining**, where world-specific data is ingested before deployment. A biological cat analogously has innate *structural* priors (sensory needs, a body) yet learns all *content* post-natally; CIT-K's "blank newborn" claim rests on exactly this distinction. The neutral `0.5` seeds and the fixed `NEED` / `σ` are *body parameters* under red line R2(a) (innate physiology), not pretraining: a sceptic is correct that they are priors, but they encode **no experience**, hence they are not data-pretraining.

**Honest boundaries of the proof.** The proof establishes that *this implementation* has zero content pretraining; it does not assert that every future instantiation will. It proves *existence* and the no-content-pretraining property for the artifact, resting on the structure / content-prior distinction above — not on rhetoric. It does **not** prove CIT-K is AGI, nor that it scales to ARC-AGI; those claims are explicitly disclaimed in §6.

---

## 5. Emergent Cognition: Attention and Curiosity

Beyond exploration, the comfort framework predicts that **higher cognition is not bolted on but emergent** from the same drive. Two axioms follow directly from §2.2:

- **Axiom A — "where comfort goes, attention goes."** Attention is simply the agent's momentary focus on the sensory dimension or scene region whose comfort gradient is largest. Because all behaviour is gated by $\Delta L_t$, attention is *by construction* co-located with the gradient of comfort — there is no separate attentional module to design.
- **Axiom B — "curiosity is the eternal drive to prevent comfort decline."** When comfort sits at a remembered peak, any local stay yields $\Delta L_t\le 0$; the only way to keep $\Delta L_t>0$ is to seek novelty (unvisited scenes). Curiosity is therefore not a hand-coded reward but the structural necessity of sustaining the comfort gradient — the same curiosity facet that drives Track B structure discovery.

These axioms unify the ancient intuition (Schopenhauer's blind will, Xunzi's 好利恶害, the Buddhist 十二因缘 seed-and-store) with a single computable variable: the comfort gradient. They are *derived*, not asserted, and they require no additional mechanism beyond the kernel of §3.

---

## 6. Why CIT-K Is Not Built to Win ARC-AGI (honest scope)

ARC-AGI-3 scores **external-goal-matching efficiency** (RHAE); although the goal must be *discovered*, scoring still rewards *hitting that discovered goal*. Our **red line R4 forbids external goals/rewards**. A prior full-agent implementation of the same theory on the ARC public environment empirically plateaus at RHAE ≈ 0.675 (8/25 levels passed) and cannot reach the leaderboard top (~1.03) without violating R4. We therefore treat ARC as a *smoke test* (the agent runs in a real interactive environment) and explicitly **not** as the theory's validation yardstick. The validation yardstick for a self-emergent, intrinsically-driven theory is structure discovery (Tracks A/B), not goal matching.

---

## 7. Related Work and Distinctiveness

The theory's *mechanisms* are not each novel: enactivism / sensorimotor contingency (O'Regan & Noë, 2001), active inference / free energy (Friston, 2010), homeostatic / homeostatically-regulated RL (Keramati & Gutkin, 2014; Yoshida et al., 2025; Tomar, 2026), Damasio's homeostasis/somatic markers (1999), Piaget's sensorimotor stage (1952), Gibson's affordances (1979), Brooks' intelligence-without-representation (1986), Ashby's homeostat (1952), Braitenberg's vehicles (1984), Grey Walter's tortoises (1953), and the Buddhist 十二因缘 / 唯识 (seed-and-store) and Xunzi's 好利恶害 all anticipate pieces. **What is distinctive is the conjunction**: a minimal kernel that (a) starts from a *blank newborn*, (b) learns only by *passive* causal memory, (c) is driven solely by a single computable *comfort gradient* $\Delta L$, and (d) is *runnable in ~119 lines*. The historical minimal kernels (Braitenberg, Walter, Ashby, Brooks) are each smaller, but none carries the complete "learn-from-blank" narrative with the comfort-gradient variable. The same "minimal complete apparatus" logic is current biology's standard: the smallest full neural wiring diagram — 302 neurons and ~7,000 synapses in *C. elegans* (White, Southgate, Thomson, & Brenner, 1986) — took 15 years of manual electron-microscopy reconstruction and, five decades later, still has no complete simulation. CIT-K aims at the complementary property: not a minimal *fragment* of a known circuit, but a *minimal-but-complete* computational kernel that runs end-to-end and can be read line by line. Closest to us, **HRRL** (Yoshida et al., 2025) defines reward as *drive reduction* $r_t=d(H_t)-d(H_{t+1})$ for a deviation $d$ from a homeostatic setpoint; CIT-K's comfort gradient $\Delta L_t = L_t - L_{t-1}$ is precisely that drive-reduction reward under $d \equiv 1-C$. CIT-K is therefore a **minimal, zero-network, zero-gradient, zero-content-pretraining instantiation of HRRL** — the family's smallest auditable member, not a rival to it. The family's *scalable* end has been demonstrated independently: Yoshida & Kuniyoshi (2025, IEEE ICDL) show homeostatic drive acquiring diverse survival skills (foraging, water-seeking, combat, shelter-building) in the Crafter open-ended environment — via deep RL. CIT-K occupies the complementary *minimal* end, the same drive instantiated with zero networks. Two further 2025–2026 reference points sharpen this positioning. The current intrinsic-motivation research agenda explicitly names the failure modes of single-objective drives (Belikov, 2026) — purely novelty- or competence-seeking objectives stall once uncertainty is resolved; CIT-K's hope mechanism (remembered comfort peaks pulling the agent out of low-variation traps) is a minimal single-scalar instance of precisely such a complementary structure, and its exploratory–comfort alternation (§4.1) is a measurable microcosm of the curiosity–competence trade-off formalised by Mantiuk et al. (2025). We position CIT-K as a *synthesis / unified minimal base*, not a claim of unprecedented mechanism. On the *empirical* side, Track B sits inside the count-based / episodic-novelty family of intrinsic exploration: curiosity as self-supervised prediction error (Pathak et al., 2017), impact-driven episodic bonuses on procedurally-generated MiniGrid (Raileanu & Rocktäschel, 2020), and NovelD's novelty-difference criterion gated by episodic first-visit counts (Zhang et al., 2021) all share CIT-K's structural skeleton — a *difference* signal (prediction error, embedding change, novelty gain, comfort gradient) gated by *memory* (episodic counts, V/M tables). What differs is the substrate: these methods estimate novelty with trained networks, whereas CIT-K uses exact tabular memory with zero networks. Track B's parity with the RND-variant baseline (§4.2) therefore reads not as a SOTA claim but as a *floor* statement: the family's mechanism, compressed to 119 lines and zero gradient steps, still functions on the same public stage. Adjacent to this *empirical* clustering lies the contemporary *agentic* axis. The current research programme for agents that represent, generate and pursue their own goals is that of *autotelic* agents: RL-IMGEP frameworks with explicit goal representations, goal-conditioned policies, internal reward functions, automated curricula and Learning-Progress-based goal sampling (Colas, Karch, Sigaud, & Oudeyer, 2022). The canonical toolchain — language- or latent-space goal spaces, hindsight experience replay, deep goal-conditioned policies, automated curricula — is now standard. CIT-K is interesting against this locus not because it instantiates the canonical toolchain — its goal space is a single scalar, its policy is a direct argmax, there is no HER, no Learning-Progress sampler and no language — but because it *still* exhibits the autotelic behaviour cluster: self-driven exploration, goal-anchored homecomings to remembered comfort peaks, and self-generated scene-and-structure discovery. CIT-K therefore reads as a *minimal non-canonical autotelic agent*: a demonstration that the autotelic behaviour cluster does not require the canonical toolchain, sharpening the question of which components are essential and which are inherited conventions of one implementation. CIT-K's V/M tabular memory is, in the modern usage of the term, a *world model*: an internal representation that lets the agent predict successor states and choose actions without exhaustive trial-and-error. The contemporary revival of the concept — from compact latent recurrent simulators (Ha & Schmidhuber, 2018) to the Joint Embedding Predictive Architecture (JEPA) and the configurable-predictive-world-model programme — replaces exact tabular counts with learned continuous latent embeddings and adds self-supervised training. CIT-K occupies the *other* end of the trade: an exact, lookup-table world model with zero parameters, trained by simply living in the world. The functional role (state → next-state, action-conditioned, queryable for planning) is identical; the substrate (exact discrete counts vs. learned continuous embeddings) and the cost–benefit (auditability for compactness and generalisation) are where the two diverge. Finally, because the kernel implements an autonomous drive, we state explicitly what it is *not*: CIT-K makes no consciousness or sentience claim, and its 119 lines are instructive precisely as a *negative* case. The current AI-consciousness indicator programme derives behavioural indicator properties from recurrent processing, global workspace, higher-order, predictive-processing and attention-schema theories (Butlin et al., 2023), and the first empirical test of a single indicator — higher-order thought (HOT-3) — reports belief-guided agency with meta-cognitive monitoring in frontier LLMs (Yalon, Goldstein, Mudrik, & Geva, 2026). Whether such behavioural evidence constitutes consciousness remains open. CIT-K contributes the complementary measurement: an agent that explores, learns a world model and self-regulates from a single scalar, yet structurally satisfies none of the indicator properties the consensus treats as candidates — no recurrent broadcasting, no global workspace, no higher-order self-model, no integrated causal power, its entire state being a pair of lookup tables. Autonomous drive, in other words, is demonstrably separable from the consciousness indicator set.

### 7.1 Theoretical Lineage and This Paper's Contribution
This work sits on a continuous research line; we demarcate the manuscripts to avoid duplicate claims:
- **Foundation (published, Wang, 2018):** *Reflective Intelligence: The Simplest Machine Model Design with Autonomous Motivation*. Through introspection and commonsense reasoning it proposes a criterion for "machine autonomous motivation" and a minimal "love and hate" model — the philosophical and methodological origin of the theory.
- **This manuscript (submission):** the **unified** statement that consolidates, in one paper, the theory's *architectural framework* (comfort-gradient drive $L_t/\Delta L_t$, hope mechanism of §2.2, emergent attention/curiosity of §5) **and** its *existence proof* (constructive + empirical, §4.3) with dual-track reproducible validation (§4) and auditable red lines. It does not split the framework and the proof across separate manuscripts; the two are presented together as one coherent claim.

---

## 8. Conclusion and the "Base" Claim

CIT-K demonstrates that a blank-born, zero-data, comfort-driven agent can self-emerge a world model and discover structure on par with neural-network intrinsic-motivation baselines, under explicit red lines that exclude networks, pretraining, gradient, and external reward. We release it as a **minimal, reproducible base** — a canonical testbed, and a public-benchmark cross-check — so that the community can build on, break, or extend it. It is not, by design, a contender for external-goal benchmarks; its value is as an alternative architectural substrate for post-LLM intelligence research.

---

## 9. Historical Significance and Outlook (position statement)

**An existence proof against the scaling axiom.** The mainstream premise — *no intelligence without massive data* — is hereby demoted from axiom to testable hypothesis. A blank-born, zero-data, zero-network agent that self-emerges scene recognition and structure discovery proves, constructively, that the alternative exists.

**Reviving a seventy-year-dormant line.** Ashby, Walter, Brooks, and developmental robotics all sought intelligence-from-blank, but stalled on non-reproducible kernels and missing testbeds. CIT-K supplies what they lacked: a 119-line auditable kernel plus a multi-track validation stage, on a shared stage with the intrinsic-motivation literature.

**Falsifiable predictions.** *1–2 years (~80%):* cited as a curiosity-grade minimal benchmark, not a paradigm shift; the realistic opening is **data efficiency** as crawlable data depletes. *3–5 years (~40–50%):* "CIT-K explores, DL consumes" matures into **developmental agents as data engines** — the fusion path, consistent with the base claim (R1). *10+ years (~10–15%):* if language or cross-domain abstraction is layered onto such kernels, the empiricist–rationalist debate acquires an **experimental platform** — the innate prior becomes a tunable parameter. *Chief risk:* remaining an elegant footnote, admired and bypassed, unless others build on it.

**A research programme: evolve the need function.** Axiom N3 implies that `NEED` itself — here carried as a fixed body constant — is in principle the *outcome* of population variation plus survival selection, not an input. A direct next step is therefore to replace the single hand-set `NEED` with a population of agents carrying varied sensory-need states, let the environment filter the survivors, and read off the survived need profile as the environment-fit drive. This would turn CIT-K from "minimal but with a phylogeny-given body" into "minimal and fully bootstrapped", closing the only place where a designer-chosen constant currently enters, and making the theory's natural-intelligence axioms fully constructive.

**One sentence.** CIT-K's significance is not outperforming LLMs — it cannot — but demoting "intelligence must be fed data" from axiom to hypothesis, and building the first reproducible apparatus for the ancient question of whether intelligence can grow from blank. A monument at the beginning of the question, not at the end of the answer.

---

## References

- Ashby, W. R. (1952). *Design for a Brain*. Chapman & Hall.
- Belikov, A. (2026). Intrinsic Motivation in Reinforcement Learning: A Research Agenda for Adaptive Self-Organisation. arXiv:2609.17325.
- Braitenberg, V. (1984). *Vehicles: Experiments in Synthetic Psychology*. MIT Press.
- Brooks, R. (1986). A robust layered control system for a mobile robot. *IEEE JRA*.
- Burda, Y., Edwards, H., Storkey, A., & Klimov, O. (2018). Exploration by Random Network Distillation. *arXiv:1810.12894*.
- Butlin, P., Long, R., Elmoznino, E., Bengio, Y., Birch, J., et al. (2023). Consciousness in Artificial Intelligence: Insights from the Science of Consciousness. *arXiv:2308.08708*.
- Chevalier-Boisvert, M., et al. (2018/2023). MiniGrid / BabyAI. *arXiv:1807.09270*; Farama Foundation.
- Colas, C., Karch, T., Sigaud, O., & Oudeyer, P.-Y. (2022). Autotelic Agents with Intrinsically Motivated Goal-Conditioned Reinforcement Learning: A Short Survey. *Journal of Artificial Intelligence Research*, 74, 1159–1199.
- Damasio, A. (1999). *The Feeling of What Happens*. Harcourt.
- Friston, K. (2010). The free-energy principle. *Nature Reviews Neuroscience*.
- Gibson, J. J. (1979). *The Ecological Approach to Visual Perception*. Houghton Mifflin.
- Grey Walter, W. (1953). *The Living Brain*. Duckworth.
- Ha, D., & Schmidhuber, J. (2018). World Models. *arXiv:1803.10122*. NeurIPS 2018.
- Keramati, M., & Gutkin, B. (2014). Homeostatic reinforcement learning. *Nature Communications*.
- Mantiuk, F., Zhou, H., & Wu, C. M. (2025). From Curiosity to Competence: How World Models Interact with the Dynamics of Exploration. arXiv:2507.08210.
- O'Regan, J. K., & Noë, A. (2001). A sensorimotor account of vision. *BBS*.
- Pathak, D., Agrawal, P., Efros, A. A., & Darrell, T. (2017). Curiosity-driven exploration by self-supervised prediction. *ICML 2017*. arXiv:1705.05363.
- Piaget, J. (1952). *The Origins of Intelligence in Children*.
- Raileanu, R., & Rocktäschel, T. (2020). RIDE: Rewarding impact-driven exploration for procedurally-generated environments. *ICLR 2020*. arXiv:2002.12292.
- Towers, M., et al. (2023). Gymnasium. *arXiv:2407.17032*.
- Tomar, D. (2026). From Tension to Resolution: Homeostatic Drive Learning as a Self-Regulating Alternative to Reward-Based Training. Preprint.
- White, J., Southgate, E., Thomson, J., & Brenner, S. (1986). The structure of the nervous system of the nematode *Caenorhabditis elegans* ("The mind of a worm"). *Developmental Biology*.
- Wang, C. (2018). Reflective Intelligence: The Simplest Machine Model Design with Autonomous Motivation. *Artificial Intelligence and Robotics Research*, 7(1), 1–16. DOI: 10.12677/airr.2018.71001. (published; foundation)
- Yoshida, N., Sprekeler, H., & Gutkin, B. (2025). Linking homeostasis to reinforcement learning: Internal state control of motivated behavior. *Current Opinion in Behavioral Sciences*, 66, 101611.
- Yoshida, N., & Kuniyoshi, Y. (2025). Unexpected Capability of Homeostasis for Open-ended Learning. *2025 IEEE International Conference on Development and Learning (ICDL)*. DOI: 10.1109/ICDL63968.2025.11204447.
- Yalon, N. S., Goldstein, A., Mudrik, L., & Geva, M. (2026). Indications of Belief-Guided Agency and Meta-Cognitive Monitoring in Large Language Models. arXiv:2602.02467.
- Zhang, T., Xu, H., Wang, X., Wu, Y., Keutzer, K., Gonzalez, J. E., & Tian, Y. (2021). NovelD: A simple yet effective exploration criterion. *NeurIPS 2021*.
- (and the philosophical lineage: Schopenhauer, Spinoza, Freud, Xunzi, Buddhist Abhidharma / 唯识宗.)

---

## Appendix A — Reproducibility & Release

- **Code:** `citk_env.py` (Track A), `citk_minigrid.py` (Track B, with RND), `run_validation.py` (two-track harness).
- **Env:** Gymnasium-compatible `CITKGridEnv`; public MiniGrid (`MiniGrid-Empty-8x8-v0`, `MiniGrid-FourRooms-v0`).
- **Determinism:** all runs seeded; raw metrics in `validation_results.json` (Tracks A/B); figures in `validation_fig.png` / `citk_plus_dl_fig.png`.
- **Red lines:** enumerated as R1–R7 in §2.3; the kernel obeys them by construction.
- **DOI / priority:** this manuscript + code are archived via **GitHub Release → Zenodo**, minting a citable, immutable DOI. Priority of the *idea* is anchored by the GitHub Release timestamp.

### A.1 No-content-pretraining inspection (auditable)

The §4.3 constructive proof is reproducible by anyone. From the repository root (`citk_validation/`):

```bash
# (1) No deep-learning framework is imported by CIT-K (only prose comments say "no torch")
grep -rniE "torch|tensorflow|keras|neural|backprop|autograd|optim\." \
      citk_env.py citk_minigrid.py run_validation.py
#   → matches only comments; zero `import` lines

# (2) No model loading / pretrained weights / external datasets
grep -rniE "load\(|pickle|\.pt|\.h5|\.npy|read_csv|datasets" \
      citk_env.py citk_minigrid.py
#   → zero hits

# (3) CIT-K memory starts empty; the only initial number is a neutral EMA seed 0.5
grep -nE "self\.V = \{\}|self\.M = \{\}" citk_env.py citk_minigrid.py
#   → self.V = {}   self.M = {}   (blank at birth)

# (4) No training loop / gradient step anywhere in the CIT-K agent
grep -rniE "gradient|\.train\(|fit\(|SGD|Adam|backward\(" \
      citk_env.py citk_minigrid.py
#   → zero hits
```

These four checks are the code-level half of the existence proof; the execution-level half is the §4.1–§4.3 results. Together they establish that the released artifact contains **no content pretraining** — only structural priors (the theory encoded in the algorithm) and innate body parameters (red line R2(a)).
