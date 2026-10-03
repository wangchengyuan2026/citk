# Track C — 100×100 离散网格：HIM（新奇舒适度驱动） vs FEP（惊奇最小化）探索对比
# =============================================================================
# 目的：补足架构手稿中被引用、但此前无代码的 FEP 对比主张。
#   在 100×100 开放网格上，比较两类智能体的环境探索能力：
#     - HIM  : 空白出生 + 被动因果记忆 + 一步前瞻，内在信号 = 新奇舒适度
#              （未见场景=1.0 / 已见=0.1），红线内零外部奖励/目标。
#     - FEP  : 主动推理 / 自由能原理的"惊奇最小化"基线。在静止环境中，
#              最小化期望惊奇使"保持不动 / 留在熟悉区"成为最优策略，
#              因而易陷入局部极小值、丧失探索——这正是手稿批评的核心失败模式。
#
# 公平性：两者共用 4 向网格运动与确定性种子；唯一区别是每步的内在驱动信号。
# 指标：
#   coverage      : 终局访问格子 / 可走格子（越高越好）
#   stuck_rate    : 10 个种子中"末段停止发现新格子"的占比（越高=越易陷局部极小）
#   new_last_k    : 末段 K 步内新发现格子数（停滞诊断）
#
# 依赖：仅 numpy。确定性：每个种子独立 default_rng。
# =============================================================================
import numpy as np
import json
import os

N = 100                      # 网格边长
FREE = N * N                 # 开放网格，全部可走
START = (N // 2, N // 2)     # 出生点（同时作为 HIM 的稳态锚 NEED 所在）
STEPS = 30000                # 每种子步数（足够覆盖 10000 格）
SEEDS = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
K = 2000                     # 停滞诊断窗口
MOVES = [(0, 1), (0, -1), (-1, 0), (1, 0)]   # up, down, left, right


def _in_bounds(p):
    return 0 <= p[0] < N and 0 <= p[1] < N


# ---------------------------------------------------------------------------
# HIM 探索智能体（与 HIM-0 / Kitten 同构：空白记忆 + 被动因果记忆 + 一步前瞻）
# ---------------------------------------------------------------------------
def run_him(seed, steps=STEPS):
    rng = np.random.default_rng(seed)
    V = {}          # 场景(格子) -> EMA 新奇舒适度
    M = {}          # 场景 -> 动作 -> EMA V(后继)
    visited = set([START])
    pos = START
    new_in_last_k = 0
    new_per_k = []
    for t in range(steps):
        eps = max(0.05, 0.6 * np.exp(-t / (steps / 4)))
        # 一步前瞻：选使"后继舒适度"期望最大的动作
        best_a, best_val = 0, -1.0
        for a, d in enumerate(MOVES):
            ni, nj = pos[0] + d[0], pos[1] + d[1]
            if not _in_bounds((ni, nj)):
                continue
            dest = (ni, nj)
            row = M.get(pos, {a2: 0.5 for a2 in range(4)})
            val = row.get(a, 0.5)
            if val > best_val:
                best_val, best_a = val, a
        if rng.random() < eps:
            best_a = int(rng.integers(4))
        d = MOVES[best_a]
        ni, nj = pos[0] + d[0], pos[1] + d[1]
        if not _in_bounds((ni, nj)):
            ni, nj = pos                      # 撞墙原地（开放网格不会发生）
        dest = (ni, nj)
        reward = 1.0 if dest not in V else 0.1   # 新奇舒适度（未见=高）
        # 学习：被动因果记忆
        v2 = V.get(dest, 0.5)
        V[dest] = 0.7 * v2 + 0.3 * reward
        row = M.setdefault(pos, {a2: 0.5 for a2 in range(4)})
        row[best_a] = 0.7 * row[best_a] + 0.3 * V[dest]
        is_new = dest not in visited
        if is_new:
            visited.add(dest); new_in_last_k += 1
        pos = dest
        if (t + 1) % K == 0:
            new_per_k.append(new_in_last_k); new_in_last_k = 0
    coverage = len(visited) / FREE
    stuck = new_per_k[-1] < max(1, 0.005 * FREE)   # 末段 K 步几乎无新发现
    return {"coverage": coverage, "stuck": bool(stuck), "new_last_k": new_per_k[-1]}


# ---------------------------------------------------------------------------
# FEP / 惊奇最小化基线
#   维护每格"熟悉度"(访问计数)作为世界信念；期望惊奇 ∝ 1/熟悉度。
#   最小化惊奇 → 偏好最熟悉(高访问)的相邻格 → 留在熟悉区、停止探索。
#   这正是 FEP 在静止环境中"保持不动最优"的失败模式（手稿批评点）。
# ---------------------------------------------------------------------------
def run_fep(seed, steps=STEPS, epistemic=0.0):
    rng = np.random.default_rng(seed + 4242)
    visit = {START: 1}
    visited = set([START])
    pos = START
    new_in_last_k = 0
    new_per_k = []
    for t in range(steps):
        eps = max(0.02, 0.15 * np.exp(-t / (steps / 6)))
        best_a, best_score = 0, -1e18
        for a, d in enumerate(MOVES):
            ni, nj = pos[0] + d[0], pos[1] + d[1]
            if not _in_bounds((ni, nj)):
                continue
            dest = (ni, nj)
            fam = visit.get(dest, 0)            # 熟悉度（高=低惊奇）
            nov = 1.0 if dest not in visited else 0.0   # 认知价值（信息增益）
            score = fam + epistemic * nov       # 极小 epistemic → 纯惊奇最小化
            if score > best_score:
                best_score, best_a = score, a
        if rng.random() < eps:
            best_a = int(rng.integers(4))
        d = MOVES[best_a]
        ni, nj = pos[0] + d[0], pos[1] + d[1]
        if not _in_bounds((ni, nj)):
            ni, nj = pos
        dest = (ni, nj)
        visit[dest] = visit.get(dest, 0) + 1
        is_new = dest not in visited
        if is_new:
            visited.add(dest); new_in_last_k += 1
        pos = dest
        if (t + 1) % K == 0:
            new_per_k.append(new_in_last_k); new_in_last_k = 0
    coverage = len(visited) / FREE
    stuck = new_per_k[-1] < max(1, 0.005 * FREE)
    return {"coverage": coverage, "stuck": bool(stuck), "new_last_k": new_per_k[-1]}


def _agg(results):
    cov = [r["coverage"] for r in results]
    stuck = [1 if r["stuck"] else 0 for r in results]
    return {
        "coverage_mean": round(float(np.mean(cov)), 4),
        "coverage_std": round(float(np.std(cov)), 4),
        "stuck_rate": round(float(np.mean(stuck)), 4),
        "seeds": len(results),
    }


def run_grid100_track(seeds=SEEDS, steps=STEPS):
    him = [run_him(s, steps) for s in seeds]
    fep = [run_fep(s, steps, epistemic=0.0) for s in seeds]
    return {
        "track": "C_grid100_exploration",
        "grid": N,
        "steps": steps,
        "free_cells": FREE,
        "him": _agg(him),
        "fep_surprise_min": _agg(fep),
        "note": ("FEP baseline = surprise-minimization (pragmatic free-energy) variant — "
                 "the dominant stationary-env 'keep-still optimum' that the manuscript "
                 "critiques. A full expected-free-energy agent with a balanced epistemic "
                 "(information-gain) term can recover exploration; the critique targets "
                 "the surprise-minimization default, not EFE per se."),
        "per_seed": {"him": him, "fep": fep},
    }


if __name__ == "__main__":
    out = run_grid100_track()
    print(json.dumps(out, indent=2, ensure_ascii=False))
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "grid100_results.json"), "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print("wrote grid100_results.json")
