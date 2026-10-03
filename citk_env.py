# Track A — 猫智能论《最简版》官方验证环境 (CITKGridEnv)
# =============================================================================
# 这是 CIT-K-0 最简版智能体的「规范测试台」：开源、Gymnasium 兼容、可复现、
# 可引用。它精确还原猫智能论原语（红线内）：
#   - 出生记忆空白（Kitten.V/M 初始为空 / 中性）
#   - 感官实时状态向量 s（由环境特征场采样，含噪声）
#   - 感官需求状态 NEED（内生稳态设定点，固定，不依赖外部目标）  [①区可调]
#   - 重叠率舒适度 = exp(-‖s - NEED‖² / 2σ²)  ← 唯一内在奖励，无外部奖励/目标
#   - 静止(STILL) 是一种运动模式（动作 4）
#   - 被动因果记忆：V[场景]=舒服度, M[场景][动作]→后继场景值；一步前瞻决策
#
# 用法：
#   from citk_env import CITKGridEnv, Kitten, run_own_track
#   metrics = run_own_track()
# =============================================================================
import numpy as np
import gymnasium as gym
from gymnasium import spaces

# 红线：NEED 是「机体需求状态」内生设定点，外部不可注入目标
NEED = np.array([0.85, 0.50, 0.15])   # 想要：暖、中光、静  (warm, mid-light, quiet)
SIGMA = 0.22                          # 重叠率锐度
ACTIONS = 5                           # up, down, left, right, STILL
A_NAMES = ["up", "down", "left", "right", "STILL"]


class CITKGridEnv(gym.Env):
    """Gymnasium 兼容的最小猫智能论世界：连续感官场 + 离散网格 + 墙体结构。"""
    metadata = {"render_modes": []}

    def __init__(self, grid_size=12, wall_frac=0.0, step=0.9, seed=1, max_steps=6000):
        super().__init__()
        self.grid_size, self.wall_frac, self.move_step = grid_size, wall_frac, step
        self.max_steps = max_steps
        # 观测 = 实时感官状态向量（3 通道）；动作 = 5 向（含 STILL）
        self.observation_space = spaces.Box(0.0, 1.0, (3,), dtype=np.float64)
        self.action_space = spaces.Discrete(ACTIONS)
        self._build(seed)

    def _build(self, seed):
        rng = np.random.default_rng(seed)
        n = self.grid_size
        # 墙体：边界 + 随机内部墙（不保证连通，演示足够）
        wall = np.zeros((n, n), bool)
        wall[0, :] = wall[-1, :] = wall[:, 0] = wall[:, -1] = True
        interior = rng.random((n, n)) < self.wall_frac
        wall |= interior
        self.wall = wall
        # 3 个感官特征源（高斯场），位置/宽度随机
        self.src = []
        for _ in range(3):
            self.src.append((rng.uniform(1, n - 1), rng.uniform(1, n - 1),
                             rng.uniform(1.5, 3.0)))
        self.free = [(i, j) for i in range(n) for j in range(n) if not wall[i, j]]
        self.step_count = 0
        self.pos = None

    def _sensory(self, pos, noise=0.05):
        x, y = pos
        vals = []
        for cx, cy, w in self.src:
            d2 = (x - cx) ** 2 + (y - cy) ** 2
            vals.append(np.exp(-d2 / (2 * w ** 2)))
        s = np.clip(np.array(vals) + self.np_random.normal(0, noise, 3), 0, 1)
        return s.astype(np.float64)

    def comfort(self, s):
        """重叠率 → 舒适度（唯一内在奖励信号，红线内自生）。"""
        return float(np.exp(-np.sum((s - NEED) ** 2) / (2 * SIGMA ** 2)))

    def model_next(self, action):
        """纯函数：给定动作返回后继感官状态（不移动、不改环境）。供希望关基线作即时舒适先知。"""
        dx, dy = [[0, 1], [0, -1], [-1, 0], [1, 0], [0, 0]][int(action)]
        nx, ny = self.pos[0] + dx * self.move_step, self.pos[1] + dy * self.move_step
        ni, nj = int(round(nx)), int(round(ny))
        if 0 <= ni < self.grid_size and 0 <= nj < self.grid_size and not self.wall[ni, nj]:
            return self._sensory((ni, nj))
        return self._sensory(self.pos)

    def act_greedy_immediate(self, s):
        """希望关基线（纯感官需求）：仅追即时舒适，无记忆、无探索，选后继即时舒适度最高的动作。"""
        vals = [self.comfort(self.model_next(a)) for a in range(ACTIONS)]
        return int(np.argmax(vals))

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        self.step_count = 0
        if seed is not None:
            self._build(seed)  # 允许按 seed 重建世界（Map A / Map B）
        self.pos = self.free[int(self.np_random.integers(len(self.free)))]
        return self._sensory(self.pos), {"pos": self.pos}

    def step(self, action):
        dx, dy = [[0, 1], [0, -1], [-1, 0], [1, 0], [0, 0]][int(action)]
        nx, ny = self.pos[0] + dx * self.move_step, self.pos[1] + dy * self.move_step
        ni, nj = int(round(nx)), int(round(ny))
        if 0 <= ni < self.grid_size and 0 <= nj < self.grid_size and not self.wall[ni, nj]:
            self.pos = (ni, nj)
        s = self._sensory(self.pos)
        self.step_count += 1
        terminated = False
        truncated = self.step_count >= self.max_steps
        return s, self.comfort(s), terminated, truncated, {"pos": self.pos}


# ---------------------------------------------------------------------------
# Kitten：空白出生 + 被动因果记忆（与 CIT-K-0 同构，Gymnasium 无关的策略）
# ---------------------------------------------------------------------------
class Kitten:
    def __init__(self, bins=4, ema=0.2, seed=7):
        self.bins, self.ema = bins, ema
        self.rng = np.random.default_rng(seed)
        self.V = {}   # 场景 -> EMA 舒适度（评估记忆，世界无关，可迁移）
        self.M = {}   # 场景 -> 动作 -> EMA V(后继)（感觉-运动因果记忆）

    def scene(self, s):
        return tuple(np.clip((s * self.bins).astype(int), 0, self.bins - 1))

    def _row(self, sc):
        return self.M.setdefault(sc, {a: 0.5 for a in range(ACTIONS)})

    def act_info(self, s, eps):
        """返回 (动作, 是否探索)。非探索步按记忆 M[场景][动作] 决策（希望开）。"""
        sc = self.scene(s)
        r = self._row(sc)
        if self.rng.random() < eps:
            return int(self.rng.integers(ACTIONS)), True
        vals = np.array([r[a] for a in range(ACTIONS)])
        return int(self.rng.choice(np.flatnonzero(vals == vals.max()))), False

    def act(self, s, eps):
        a, _ = self.act_info(s, eps)
        return a

    def learn(self, s, a, c, s2):
        sc2 = self.scene(s2)
        v2 = self.V.get(sc2, 0.5)
        self.V[sc2] = (1 - self.ema) * v2 + self.ema * c
        r = self._row(self.scene(s))
        r[a] = (1 - self.ema) * r[a] + self.ema * self.V[sc2]


# ---------------------------------------------------------------------------
# 运行协议：返回验证 CIT-K-0 最简版的核心指标
# ---------------------------------------------------------------------------
def rollout(env, kitten, steps, use_true_reward=True, seed=None, transfer_V=None):
    if transfer_V is not None:
        kitten.V = dict(transfer_V)      # 世界无关价值迁移（场景辨认）
    obs, _ = env.reset(seed=seed)
    eps = lambda t: max(0.05, np.exp(-t / 1200.0))
    comf = np.zeros(steps)
    scenes = set()
    for t in range(steps):
        a = kitten.act(obs, eps(t))
        obs2, c, _, trunc, _ = env.step(a)
        reward = c if use_true_reward else float(kitten.rng.random())
        kitten.learn(obs, a, reward, obs2)
        comf[t] = c
        scenes.add(kitten.scene(obs2))
        obs = obs2
        if trunc:
            break
    return comf, len(scenes)


def _pearson(xs, ys):
    xs = np.asarray(xs, float); ys = np.asarray(ys, float)
    if len(xs) < 2 or xs.std() < 1e-9 or ys.std() < 1e-9:
        return float("nan")
    return float(np.corrcoef(xs, ys)[0, 1])


def run_own_track(steps=6000, seedA=1, seedB=2):
    """Track A 主流程：出生→学习、随机奖励消融、场景辨认(价值跨世界一致)。"""
    env = CITKGridEnv(seed=seedA, max_steps=steps)
    kit = Kitten()
    cA, nA = rollout(env, kit, steps, seed=seedA)

    kit_rand = Kitten()
    cR, _ = rollout(env, kit_rand, steps, use_true_reward=False, seed=seedA)

    # 价值函数跨世界一致性：在 Map B 上采样感官场景，检验「Map A 学到的
    # V[场景]=舒适度」是否仍成立（NEED 固定 → V 世界无关，这正是场景辨认）。
    envB = CITKGridEnv(seed=seedB, max_steps=steps)
    rng = np.random.default_rng(99)
    seen, unseen = [], []
    for _ in range(400):
        pos = envB.free[int(rng.integers(len(envB.free)))]
        s = envB._sensory(pos, noise=0.0)
        sc = kit.scene(s)
        v_pred = kit.V.get(sc, 0.5)
        c_true = envB.comfort(s)
        (seen if sc in kit.V else unseen).append((v_pred, c_true))

    corr_seen = _pearson([p for p, _ in seen], [t for _, t in seen])
    mae_seen = float(np.mean([abs(p - t) for p, t in seen])) if seen else float("nan")
    corr_unseen = _pearson([p for p, _ in unseen], [t for _, t in unseen])

    return {
        "track": "A_own_canonical",
        "comfort_first500": round(float(cA[:500].mean()), 4),
        "comfort_last500": round(float(cA[-500:].mean()), 4),
        "comfort_gain": round(float(cA[-500:].mean() - cA[:500].mean()), 4),
        "ablation_random_last500": round(float(cR[-500:].mean()), 4),
        "mapA_sensory_coverage": nA,
        "value_transfer_seen_scenes": len(seen),
        "value_transfer_corr_seen": round(corr_seen, 4) if corr_seen == corr_seen else None,
        "value_transfer_mae_seen": round(mae_seen, 4) if seen else None,
        "value_transfer_corr_unseen": round(corr_unseen, 4) if corr_unseen == corr_unseen else None,
        "comfort_series": [round(float(x), 3) for x in cA[::50]],
    }


def _greedy_run(env, steps, sd):
    """希望关基线（纯感官需求）：仅追即时舒适，无记忆、无探索。"""
    obs, _ = env.reset(seed=sd)
    dwell = 0
    for t in range(steps):
        a = env.act_greedy_immediate(obs)
        obs2, c, _, trunc, _ = env.step(a)
        if c > 0.7:
            dwell += 1
        obs = obs2
        if trunc:
            break
    return dwell / steps


def run_deferral_ablation(steps=6000, seeds=(1, 2, 3, 4, 5)):
    """记忆需求压制/推延感官需求：CIT-K（希望开，记忆 M 驱动）vs 即时舒适贪婪基线（希望关）。

    度量：
      override_rate        —— 非探索步中，CIT-K 的记忆驱动动作 ≠ 即时舒适贪婪动作的比例
                              （直接量化『记忆需求压制感官需求』：决策由记忆而非即时舒适决定）
      citk/greedy_dwell    —— 峰值区（舒适 > 0.7）停留占比；CIT-K 更低 = 会离开舒适区、推延即时满足
      citk_coverage        —— CIT-K 访问的场景数（离开舒适区 → 探索更广）
    """
    env = CITKGridEnv(seed=seeds[0], max_steps=steps)
    override, override_late_list, citk_dwell, cov, greedy_dwell = [], [], [], [], []
    for sd in seeds:
        kit = Kitten(seed=sd)
        obs, _ = env.reset(seed=sd)
        eps = lambda t: max(0.05, np.exp(-t / 1200.0))
        n_non, n_over, dwell = 0, 0, 0
        n_non_late, n_over_late = 0, 0
        scenes = set()
        for t in range(steps):
            a, explored = kit.act_info(obs, eps(t))
            a_g = env.act_greedy_immediate(obs)
            if not explored:
                n_non += 1
                if a != a_g:
                    n_over += 1
                if t >= steps // 2:   # 后半程：记忆已收敛，隔离早期学习噪声混淆
                    n_non_late += 1
                    if a != a_g:
                        n_over_late += 1
            obs2, c, _, trunc, _ = env.step(a)
            if c > 0.7:
                dwell += 1
            scenes.add(kit.scene(obs2))
            kit.learn(obs, a, c, obs2)
            obs = obs2
            if trunc:
                break
        override.append(n_over / n_non if n_non else 0.0)
        override_late_list.append(n_over_late / n_non_late if n_non_late else 0.0)
        citk_dwell.append(dwell / steps)
        cov.append(len(scenes))
        greedy_dwell.append(_greedy_run(env, steps, sd))
    override = np.array(override)
    citk_dwell = np.array(citk_dwell)
    greedy_dwell = np.array(greedy_dwell)
    return {
        "track": "A_deferral",
        "override_rate_mean": round(float(override.mean()), 4),
        "override_rate_se": round(float(override.std() / np.sqrt(len(override))), 4),
        "override_rate_late_mean": round(float(np.mean(override_late_list)), 4),
        "citk_peak_dwell_frac": round(float(citk_dwell.mean()), 4),
        "greedy_peak_dwell_frac": round(float(greedy_dwell.mean()), 4),
        "citk_coverage": round(float(np.mean(cov)), 1),
    }


if __name__ == "__main__":
    import json
    m = run_own_track()
    print(json.dumps(m, indent=2, ensure_ascii=False))
