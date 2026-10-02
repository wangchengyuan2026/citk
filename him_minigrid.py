# Track B — 公开基准交叉校验：HIM(零NN被动记忆) vs RND(神经网络内在动机标杆) vs Random
# =============================================================================
# 目的：用「外部可信」的公开基准验证 HIM-0 最简版的同一主张——
#   零训练数据、零外部奖励/目标，纯内在驱动能否从交互中发现世界结构。
# 本文件把内在动机文献的标杆方法 RND（Random Network Distillation, Burda 2018）
# 作为第三个基线同台，直接回应「零 NN 的 HIM 能否赶上 NN 内在动机方法」。
#
# 公平设计：三个 agent 共用同一套策略（epsilon-贪心 + 一步前瞻，记忆图 V/M），
# 唯一差别是「每步内在信号」如何算：
#   - Random : 无学习，地板
#   - HIM    : 新奇计数（1.0 未见场景 / 0.1 已见）—— 零 NN、纯被动记忆
#   - RND    : 随机目标网络 φ(s) 与岭回归预测器 f(s) 的误差 ||f(s)-φ(s)||² —— NN 方法
# 因此差异只来自内在信号质量，正是要验证的命题。
#
# 指标（诚实，不虚报胜率）：
#   cell_coverage       : 访问过的格子 / 可走格子
#   transition_coverage : 经历过的不同 (场景,动作) 对数量（= 体验到的世界动力学广度）
#   rooms_reached       : 在 FourRooms 中到达的房间数（0-4）
#   model_accuracy      : 因果记忆收敛度（确定性动力学下多数后继占优比例）
# =============================================================================
import numpy as np
import gymnasium as gym
import minigrid  # noqa: F401  (注册 MiniGrid 环境)

# MiniGrid 动作子集：左转/右转/前进/切换 + 静止(拾取=空地无操作)
HIM_ACTIONS = [0, 1, 2, 5, 3]   # turn-left, turn-right, forward, toggle, pickup(=STILL no-op)
A_NAMES = ["L", "R", "F", "T", "STILL"]


def scene_of(obs):
    """把自中心符号观测压成「感官场景」键（猫论：实时感官状态）。"""
    return tuple(int(x) for x in np.asarray(obs["image"]).flatten())


class HIMMiniGrid:
    """与 HIM-0 同构：空白记忆 + 被动因果记忆 + 一步前瞻，仅新奇驱动（零 NN）。

    子类可覆写 reward_for(...) 换内在信号（如 RND），策略结构不变。"""
    def __init__(self, ema=0.3, seed=7):
        self.ema = ema
        self.rng = np.random.default_rng(seed)
        self.V = {}      # 场景 -> EMA 新奇舒适度
        self.M = {}      # 场景 -> 动作 -> EMA V(后继)
        self.visits = {}  # 场景 -> 访问次数
        self.T = {}      # 场景 -> 动作 -> Counter(后继场景)  ← 因果记忆

    def _row(self, sc):
        return self.M.setdefault(sc, {a: 0.5 for a in range(len(HIM_ACTIONS))})

    def on_obs(self, obs):
        """每步观测钩子（RND 用来更新预测器；HIM 无需）。"""
        pass

    def reward_for(self, sc2, obs2, sc, a):
        """内在信号：新奇计数（1.0 未见 / 0.1 已见）。"""
        return 1.0 if sc2 not in self.V else 0.1

    def act(self, sc, eps):
        r = self._row(sc)
        if self.rng.random() < eps:
            return int(self.rng.integers(len(HIM_ACTIONS)))
        vals = np.array([r[a] for a in range(len(HIM_ACTIONS))])
        return int(self.rng.choice(np.flatnonzero(vals == vals.max())))

    def learn(self, sc, a, sc2, reward):
        self.visits[sc] = self.visits.get(sc, 0) + 1
        v2 = self.V.get(sc2, 0.5)
        self.V[sc2] = (1 - self.ema) * v2 + self.ema * reward
        r = self._row(sc)
        r[a] = (1 - self.ema) * r[a] + self.ema * self.V[sc2]
        cnt = self.T.setdefault(sc, {}).setdefault(a, {})
        cnt[sc2] = cnt.get(sc2, 0) + 1


class RNDMiniGrid(HIMMiniGrid):
    """RND（Random Network Distillation）基线——内在动机文献标杆 NN 方法。

    纯 numpy 实现（随机目标网络固定 + 岭回归预测器，无需 torch）：
      φ(s) = tanh(W·s + b)        固定随机目标
      f(s) ≈ φ(s)                  岭回归预测器（闭式解，无自动梯度）
      内在奖励 = mean( (f(s) - φ(s))² )   未见状态预测误差大→高探索
    这是文献中的 NN 内在动机方法，作为 HIM 的「带 NN」对照（HIM 本身零 NN）。"""
    def __init__(self, feat_dim=32, lam=1.0, buf=1500, retrain=150, ema=0.3, seed=21):
        super().__init__(ema=ema, seed=seed)
        self.rng = np.random.default_rng(seed)
        self.feat_dim, self.lam, self.buf, self.retrain = feat_dim, lam, buf, retrain
        self.target_W = None
        self.target_b = None
        self.theta = None          # 岭回归系数 (d x feat)
        self.Xbuf, self.Ybuf = [], []
        self.nstep = 0

    def _feat(self, obs):
        return np.asarray(obs["image"], float).flatten() / 10.0

    def _phi(self, s):
        if self.target_W is None:
            d = s.shape[0]
            self.target_W = self.rng.standard_normal((self.feat_dim, d)) * 0.1
            self.target_b = self.rng.standard_normal(self.feat_dim)
        return np.tanh(self.target_W @ s + self.target_b)

    def _predict(self, s):
        if self.theta is None:
            return np.zeros(self.feat_dim)
        return self.theta.T @ s

    def on_obs(self, obs):
        s = self._feat(obs)
        phi = self._phi(s)
        if len(self.Xbuf) < self.buf:
            self.Xbuf.append(s); self.Ybuf.append(phi)
        else:
            j = int(self.rng.integers(self.buf))
            self.Xbuf[j] = s; self.Ybuf[j] = phi
        self.nstep += 1
        if self.nstep % self.retrain == 0 and len(self.Xbuf) >= self.retrain:
            X = np.array(self.Xbuf); Y = np.array(self.Ybuf)
            A = X.T @ X + self.lam * np.eye(X.shape[1])
            self.theta = np.linalg.solve(A, X.T @ Y)

    def reward_for(self, sc2, obs2, sc, a):
        s = self._feat(obs2)
        phi = self._phi(s)
        pred = self._predict(s)
        return float(np.mean((pred - phi) ** 2))


def _room_of(env, pos):
    g = env.unwrapped.width
    mid = (g - 1) // 2
    x, y = pos
    return (1 if x > mid else 0) + 2 * (1 if y > mid else 0)


def _run(env_id, agent, steps, seed, eps_fn):
    env = gym.make(env_id)
    obs, _ = env.reset(seed=seed)
    sc = scene_of(obs)
    cells, rooms, trans = set(), set(), set()
    pos0 = tuple(env.unwrapped.agent_pos)
    cells.add(pos0); rooms.add(_room_of(env, pos0))
    # 专用 rng，使 Random 基线随 seed 完全确定（P1-3 修复：原先用全局未种子化的 np.random.randint）
    rand_rng = np.random.default_rng(seed + 777)
    if agent:
        agent.on_obs(obs)
    for t in range(steps):
        if agent:
            a_idx = agent.act(sc, eps_fn(t))
        else:
            a_idx = int(rand_rng.integers(len(HIM_ACTIONS)))
        action = HIM_ACTIONS[a_idx]
        obs2, _, term, trunc, _ = env.step(action)
        sc2 = scene_of(obs2)
        reward = agent.reward_for(sc2, obs2, sc, a_idx) if agent else 0.0
        if agent:
            agent.on_obs(obs2)
            agent.learn(sc, a_idx, sc2, reward)
        pos = tuple(env.unwrapped.agent_pos)
        cells.add(pos); rooms.add(_room_of(env, pos))
        trans.add((sc, a_idx))
        sc = sc2
        if term or trunc:
            env.reset(seed=seed)
    env.close()
    return cells, rooms, trans, (agent.T if agent else {})


def _model_accuracy(T):
    """因果记忆收敛度：已体验的 (场景,动作) 中，多数后继场景占优(>0.9)的比例。
    确定性动力学下越高 = 因果记忆越准（结构被发现）。"""
    conf = total = 0
    for sc, acts in T.items():
        for a, nxt in acts.items():
            tot = sum(nxt.values())
            if tot >= 2:
                conf += (max(nxt.values()) / tot > 0.9); total += 1
    return conf / total if total else float("nan")


def run_minigrid_track(env_id="MiniGrid-Empty-8x8-v0", steps=3000,
                       seeds=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10), eps0=0.6):
    eps_fn = lambda t: max(0.05, eps0 * np.exp(-t / (steps / 3)))
    him_cells, him_rooms, him_trans, him_acc = [], [], [], []
    rnd_cells, rnd_rooms, rnd_trans, rnd_acc = [], [], [], []
    rand_cells, rand_rooms, rand_trans = [], [], []
    for s in seeds:
        h = HIMMiniGrid(seed=100 + s)
        c, rm, tr, T = _run(env_id, h, steps, s, eps_fn)
        him_cells.append(len(c)); him_rooms.append(len(rm)); him_trans.append(len(tr))
        him_acc.append(_model_accuracy(T))
        r = RNDMiniGrid(seed=200 + s)
        c2, rm2, tr2, T2 = _run(env_id, r, steps, s, eps_fn)
        rnd_cells.append(len(c2)); rnd_rooms.append(len(rm2)); rnd_trans.append(len(tr2))
        rnd_acc.append(_model_accuracy(T2))
        c3, rm3, tr3, _ = _run(env_id, None, steps, s, eps_fn)
        rand_cells.append(len(c3)); rand_rooms.append(len(rm3)); rand_trans.append(len(tr3))
    free = _free_cells(env_id, seeds[0])
    def m(vals): return round(float(np.mean(vals)), 4)
    def sd(vals): return round(float(np.std(vals)), 4)
    def cov(vals): return [min(1.0, c / free) for c in vals]
    return {
        "track": "B_minigrid_public",
        "env_id": env_id,
        "steps": steps,
        "n_seeds": len(seeds),
        "seeds": list(seeds),
        "him_cell_coverage": m(cov(him_cells)),
        "him_cell_coverage_std": sd(cov(him_cells)),
        "rnd_cell_coverage": m(cov(rnd_cells)),
        "rnd_cell_coverage_std": sd(cov(rnd_cells)),
        "rand_cell_coverage": m(cov(rand_cells)),
        "rand_cell_coverage_std": sd(cov(rand_cells)),
        "him_transition_coverage": int(round(m(him_trans))),
        "him_transition_coverage_std": sd(him_trans),
        "rnd_transition_coverage": int(round(m(rnd_trans))),
        "rnd_transition_coverage_std": sd(rnd_trans),
        "rand_transition_coverage": int(round(m(rand_trans))),
        "rand_transition_coverage_std": sd(rand_trans),
        "him_rooms_reached": m(him_rooms),
        "him_rooms_reached_std": sd(him_rooms),
        "rnd_rooms_reached": m(rnd_rooms),
        "rnd_rooms_reached_std": sd(rnd_rooms),
        "rand_rooms_reached": m(rand_rooms),
        "rand_rooms_reached_std": sd(rand_rooms),
        "him_model_accuracy": m(him_acc),
        "him_model_accuracy_std": sd(him_acc),
        "rnd_model_accuracy": m(rnd_acc),
        "rnd_model_accuracy_std": sd(rnd_acc),
    }


def _free_cells(env_id, seed):
    env = gym.make(env_id)
    env.reset(seed=seed)
    g = env.unwrapped.grid
    n = sum(1 for i in range(g.width) for j in range(g.height)
            if g.get(i, j) is None)
    env.close()
    return n


if __name__ == "__main__":
    import json
    for eid in ["MiniGrid-Empty-8x8-v0", "MiniGrid-FourRooms-v0"]:
        print(json.dumps(run_minigrid_track(eid), indent=2, ensure_ascii=False))
