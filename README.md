# HIM · 极简零数据、舒适度驱动、自涌现智能内核

**作者 / Author:** 王程远（1987年生），广东惠州，自由学者
**Chengyuan Wang (b. 1987), Independent Scholar, Huizhou, Guangdong, China**

HIM（Heuristic-Intrinsic, Minimal）是「猫智能论」的最简可执行内核：一个记忆空白的新生体，仅靠内在舒适度信号（模糊集面重叠度）自涌现世界模型并发现环境结构——**无数据、无神经网络、无预训练、无梯度、无外部奖励、无逐任务分支**。

## 仓库内容 / Contents
- `him_env.py` — 轨道 A：HIMGridEnv + Kitten（零 NN、零梯度、零预训练）
- `him_minigrid.py` — 轨道 B：MiniGrid Empty-8x8 / FourRooms + RND 线性变体基线
- `him_grid100.py` — 轨道 C：100×100 网格 HIM vs FEP（惊奇最小化）探索对比
- `run_validation.py` — 三轨总装
- `him_plus_dl.py` — 「HIM 探索、外挂 DL 消费」协作原型（基线对照面板）
- `paper/HIM_paper_zh.md` — 中文版投稿稿
- `paper/HIM_paper.md` — 英文版投稿稿（权威稿）
- `*.json` / `*.png` — 实测数据与逐种子存证
- `docs/` — 多模型独立验收与终审记录（supplementary）

## 前置文献 / Prior work
- (Wang, 2018) 反思智能：存在自主动机的最简机器模型设计。*人工智能与机器人研究*, 7(1):1–16. DOI: 10.12677/airr.2018.71001.（已发表，基石；本文的理论起源）
- 注：HIM 的架构框架（舒适度梯度驱动、希望机制、涌现注意力/好奇心）与无预训练存在性证明已**合并于本文单一投稿稿**，不再单独成稿。

## 复现 / Reproduce
```bash
pip install -r requirements.txt
python run_validation.py            # 三轨验证（A/B/C）
python him_plus_dl.py              # 协作原型
```
无内容预训练的可审计证明见英文稿附录 A.1（四条 grep 命令真复现）。

## 发布 / Release
代码与论文经 **GitHub Release → Zenodo** 归档，铸出不可变 DOI（arXiv 因账号限制未走）。原始发布包亦存于 WorkBuddy 资料库。

## 许可 / License
代码以 MIT 许可证开源（见 `LICENSE`）；论文以预印本形式发布，保留作者署名。
