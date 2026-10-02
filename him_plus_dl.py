# =============================================================================
# 下一步工作原型：HIM（零训练猫） + 外挂深度学习（协作，非作弊）
# -----------------------------------------------------------------------------
# 概念：
#   HIM 最简版（Kitten，零 NN / 零预训练 / 零梯度）从空白自主探索，产出
#   「趋利避害」内容 = 它的局部价值/舒适度记忆 V[场景] 与因果记忆 M。
#   我们把这张「猫自主探索产物」喂给一个 *外挂* 的深度学习模块（此处用一个
#   免依赖 numpy MLP 代表），让它学会 HIM 的舒适度场并 *泛化* 到猫没去过
#   的感官状态。
#
# 为什么不是作弊（红线合规 + R1 基座愿景）：
#   - HIM 核心始终零 NN / 零预训练 / 零梯度，本次完全不改、不碰。
#   - 外挂 DL 是独立模块，只消费 HIM *自涌现* 的 (感官状态, 舒适度) 样本；
#     标签是 HIM 的内在舒适度，没有任何外部奖励 / 世界标注被注入。
#   - 这是「两种底层理论合作」：HIM=落地探索者+局部记忆（零训练）；
#     DL=全局函数逼近器（需训练，但仅由 HIM 自举，而非由世界预训练）。
#   - 恰好兑现 R1：HIM 是「别人/别的模块可在其上建构的基座」。
#
# 分工证明：猫的局部记忆只认得 *访问过的* 场景（未见过默认 0.5）；
#          外挂 MLP 训练后能 *外推* 到未见感官状态——这是猫单独做不到的。
# =============================================================================
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from him_env import HIMGridEnv, Kitten, NEED, SIGMA

RNG = np.random.default_rng(1234)


# ---------------------------------------------------------------------------
# 外挂深度学习模块：最小 numpy MLP（2 隐藏层, ReLU, 手动反向传播）
# 代表「外挂的深度学习」——它是独立的、需要梯度训练的消费方。
# ---------------------------------------------------------------------------
class ExtMLP:
    def __init__(self, dims, lr=0.02, seed=11):
        r = np.random.default_rng(seed)
        self.W = [r.standard_normal((dims[i + 1], dims[i])) * np.sqrt(2.0 / dims[i])
                  for i in range(len(dims) - 1)]
        self.b = [np.zeros(dims[i + 1]) for i in range(len(dims) - 1)]
        self.lr = lr
        self.rng = np.random.default_rng(seed + 1)

    def forward(self, x):
        a = np.asarray(x, float)
        self._a = [a]
        for i in range(len(self.W)):
            z = self.W[i] @ a + self.b[i]
            a = np.maximum(0.0, z) if i < len(self.W) - 1 else 1.0 / (1.0 + np.exp(-z))
            self._a.append(a)
        return float(np.asarray(a).item())

    def backward(self, x, y):
        yhat = self._a[-1]
        d = (yhat - y) * yhat * (1.0 - yhat)          # dMSE/dz at sigmoid output
        gW, gb = [], []
        for i in reversed(range(len(self.W))):
            gb.insert(0, d)
            gW.insert(0, np.outer(d, self._a[i]))
            if i > 0:
                d = (self.W[i].T @ d) * (self._a[i] > 0)   # ReLU 导数
        for i in range(len(self.W)):
            self.W[i] -= self.lr * gW[i]
            self.b[i] -= self.lr * gb[i]

    def fit(self, X, Y, epochs=400, bs=64):
        X, Y = np.asarray(X, float), np.asarray(Y, float)
        n = len(X)
        for _ in range(epochs):
            idx = self.rng.permutation(n)
            for i in range(0, n, bs):
                for x, y in zip(X[idx[i:i + bs]], Y[idx[i:i + bs]]):
                    self.forward(x)        # 缓存 self._a
                    self.backward(x, y)

    def predict(self, X):
        return np.array([self.forward(x) for x in np.asarray(X, float)])


def _mae(a, b):
    return float(np.mean(np.abs(np.asarray(a) - np.asarray(b))))


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------
def main():
    STEPS = 6000
    # --- 阶段 1：HIM 零训练自主探索（与论文 Track A 同源，核心不动） ---
    env = HIMGridEnv(seed=1, max_steps=STEPS)
    kit = Kitten(seed=7)
    obs, _ = env.reset(seed=1)
    eps = lambda t: max(0.05, np.exp(-t / 1200.0))
    samples = []
    for t in range(STEPS):
        a = kit.act(obs, eps(t))
        obs2, c, _, trunc, _ = env.step(a)
        kit.learn(obs, a, c, obs2)
        samples.append((obs.copy(), float(c)))
        obs = obs2
        if trunc:
            break
    X = np.array([s for s, _ in samples])
    Y = np.array([c for _, c in samples])
    visited_scenes = set(kit.scene(s) for s in X)

    # --- 阶段 2：外挂 DL 消费 HIM 自涌现样本（仅在 HIM 产物上训练） ---
    n = len(X)
    perm = RNG.permutation(n)
    n_tr = int(0.8 * n)
    tr, te = perm[:n_tr], perm[n_tr:]
    mlp = ExtMLP([3, 16, 16, 1], lr=0.04, seed=11)
    mlp.fit(X[tr], Y[tr], epochs=800, bs=64)
    pred_te = mlp.predict(X[te])
    mlp_test_mae = _mae(pred_te, Y[te])

    # --- 平凡基线对照（同一训练集 X[tr]，Kimi-K3 验收要求）：DL 必要性必须
    # 经得住常数/线性/kNN 的检验，否则"需要深度学习"不成立 ---
    def ridge_fit(Xtr, Ytr, lam=1e-4):
        Xb = np.hstack([Xtr, np.ones((len(Xtr), 1))])
        return np.linalg.solve(Xb.T @ Xb + lam * np.eye(Xb.shape[1]), Xb.T @ Ytr)

    def ridge_pred(w, Xq):
        return np.hstack([Xq, np.ones((len(Xq), 1))]) @ w

    def knn_pred(Xtr, Ytr, Xq, k=5):
        out = np.empty(len(Xq))
        for i, x in enumerate(Xq):
            idx = np.argsort(np.linalg.norm(Xtr - x, axis=1))[:k]
            out[i] = Ytr[idx].mean()
        return out

    w_lin = ridge_fit(X[tr], Y[tr])
    y_const = float(Y[tr].mean())

    # --- 阶段 3：分工证明 —— 外推到 HIM 局部记忆够不到的未见感官状态 ---
    # 在 [0,1]^3 上铺一张密集网格（729 点），大部分是 HIM 没精确访问过的
    # 感官组合；比较 MLP 泛化预测 vs 平凡基线 vs HIM 局部查表（未见默认 0.5）。
    g = np.linspace(0.02, 0.98, 9)
    grid = np.array([[i, j, k] for i in g for j in g for k in g], float)
    true_c = np.array([float(np.exp(-np.sum((s - NEED) ** 2) / (2 * SIGMA ** 2))) for s in grid])
    mlp_pred = mlp.predict(grid)
    lin_pred = ridge_pred(w_lin, grid)
    knn = knn_pred(X[tr], Y[tr], grid)
    const_pred = np.full(len(grid), y_const)
    him_lookup = np.array([kit.V.get(kit.scene(s), 0.5) for s in grid])  # 猫的局部记忆

    mlp_dense_mae = _mae(mlp_pred, true_c)
    lin_dense_mae = _mae(lin_pred, true_c)
    knn_dense_mae = _mae(knn, true_c)
    const_dense_mae = _mae(const_pred, true_c)
    him_dense_mae = _mae(him_lookup, true_c)
    mlp_dense_corr = float(np.corrcoef(mlp_pred, true_c)[0, 1])
    lin_dense_corr = float(np.corrcoef(lin_pred, true_c)[0, 1])
    knn_dense_corr = float(np.corrcoef(knn, true_c)[0, 1])

    # --- 图：固定 s[2]=NEED[2]，看一张 2D 切片（真值 / MLP / kNN / 猫查表） ---
    s2_fixed = NEED[2]
    gg = np.linspace(0.02, 0.98, 40)
    GG0, GG1 = np.meshgrid(gg, gg)
    slab = np.stack([GG0.ravel(), GG1.ravel(),
                     np.full(GG0.size, s2_fixed)], 1)
    true_slab = np.array([float(np.exp(-np.sum((s - NEED) ** 2) / (2 * SIGMA ** 2))) for s in slab]).reshape(40, 40)
    mlp_slab = mlp.predict(slab).reshape(40, 40)
    knn_slab = knn_pred(X[tr], Y[tr], slab).reshape(40, 40)
    him_slab = np.array([kit.V.get(kit.scene(s), 0.5) for s in slab]).reshape(40, 40)

    fig, ax = plt.subplots(1, 4, figsize=(18, 4.3))
    fig.suptitle("HIM (zero-training cat) experience consumed by regressors  |  "
                 "comfort field: truth vs MLP vs kNN vs HIM local lookup", fontsize=11)
    for axx, mat, title in [
        (ax[0], true_slab, "Truth (overlap comfort)"),
        (ax[1], mlp_slab, "External MLP\n(trained on HIM's samples)"),
        (ax[2], knn_slab, "kNN baseline (trivial,\ntrained on same samples)"),
        (ax[3], him_slab, "HIM local lookup (0.5 on\nunvisited scenes)"),
    ]:
        im = axx.imshow(mat, origin="lower", extent=[0, 1, 0, 1], vmin=0, vmax=1, cmap="viridis")
        axx.set_title(title, fontsize=9)
        axx.set_xlabel("sensory ch0"); axx.set_ylabel("sensory ch1")
    fig.colorbar(im, ax=ax, shrink=0.8, label="comfort")
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig("/workspace/him_validation/him_plus_dl_fig.png", dpi=130)
    plt.close(fig)

    metrics = {
        "concept": "HIM zero-training exploration -> external regressors consume emergent (s,comfort) -> generalize",
        "him_samples_collected": int(n),
        "him_visited_scenes": int(len(visited_scenes)),
        "external_mlp": "numpy MLP 3->16->16->1, ReLU+SGD, trained ONLY on HIM's autonomous (s,comfort) samples",
        "trivial_baselines_same_train_set": "constant / ridge-linear / kNN(k=5) trained on the SAME 80% train split (Kimi-K3 acceptance requirement)",
        "mlp_test_mae_on_experienced": round(mlp_test_mae, 4),
        "dense_unseen_grid_mae": {
            "external_mlp": round(mlp_dense_mae, 4),
            "knn_k5": round(knn_dense_mae, 4),
            "linear_ridge": round(lin_dense_mae, 4),
            "constant": round(const_dense_mae, 4),
            "him_local_lookup": round(him_dense_mae, 4),
        },
        "dense_unseen_grid_corr_true": {
            "external_mlp": round(mlp_dense_corr, 4),
            "knn_k5": round(knn_dense_corr, 4),
            "linear_ridge": round(lin_dense_corr, 4),
        },
        "interpretation": (
            "Any sufficiently flexible regressor can consume HIM's self-emerged experience "
            "stream and generalise beyond the cat's local memory (MLP %.3f, kNN %.3f, vs "
            "HIM lookup %.3f MAE on unseen states). Deep learning is NOT specifically "
            "required here — trivial kNN matches or beats the small MLP; DL's expected "
            "advantage lies on high-dimensional perceptual inputs where kNN fails. The "
            "cooperation claim is therefore scoped to 'HIM's experience stream is "
            "consumable and generalisable', not 'HIM needs deep learning'. HIM itself "
            "stays zero-training/zero-NN throughout."
            % (mlp_dense_mae, knn_dense_mae, him_dense_mae)
        ),
    }
    with open("/workspace/him_validation/him_plus_dl_results.json", "w") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)
    print(json.dumps(metrics, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
