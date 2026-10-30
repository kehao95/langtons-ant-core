# 自写介质：为什么简单规则会出现复杂行为？
## Self-writing media, causal history, and predictive macro-states

**Synthesis / 解释性研究札记** · 2026-10-30  
**Status:** conceptual synthesis grounded in the linked project theorems; not a new theorem, HC solution, thermodynamic law, or claim of integrability.

**English précis.** A tiny controller coupled to a rewritable two-dimensional environment can store and later retrieve its own past. The scientifically productive question is which distinctions in that history affect future observations, and whether the resulting response equivalence is exactly closed under further physical interactions. Rigidity, semilinearity, and scattering are rigorously established only in their stated domains.

## 1. 真正的动力系统：头部与整张可写平面

经典双色规则：白格向右转并翻黑；黑格向左转并翻白；然后前进一步。完整状态是
`X_t=(B_t,p_t,h_t)`，其中 `B_t` 是**完整有限黑格集合**。若 `q_j` 是第 `j` 次读取的格子，恒等式为

```text
B_T = B_0 XOR {q_0} XOR {q_1} XOR ... XOR {q_(T-1)} .
```

这是对已经确定的**真实轨迹**的精确记账。不能反过来认为不同时间的读写操作可任意交换：提前改变格色可能改变后面的全部位置。头部有四个朝向，不是严格的零状态机器；其历史信息主要由外部平面承载。

**机制解释：** 格色既是数据又影响下一次移动，形成“行动—写入—重访—再寻址”的因果环。空间距离还能安排延时和历史准备。参见 [memory_feedback](../memory_feedback/) 与 [defect_synthesis](../defect_synthesis/)。

**受控见证：** [六黑格族](../defect_synthesis/)保持初始黑格数量和形状不变，仅平移位置，正向十因子违例数为 `6702+47k`，每个有限 `k` 都最终进入 P104。这证明初始黑格数量或黑集本身直径不能统一约束总违例；**并不**证明一个固定输入拥有无限违例。

## 2. 局部语法与几何相容性：刚性是有前提的

转向字词必须符合一个同格重访约束：连续两次读取同一格时，请求的转向必须相反。仅靠抽象有限状态图的闭路，不能保证整条二维轨迹在真实颜色场中可行。

[factor_language](../factor_language/) 给出强烈但**条件性**的结论：若未来的每个十字窗口均来自标准 P104 的循环局部语言，则任意背景最终只能进入 104、28 或 24 的模式；对**有限初始黑场**，另外两种要求无限供应初黑格的尾部被排除。九字窗口不足以强迫任意背景的最终周期性。

这说明“局部词法 × 平面读取约束 × 初始资源条件”能够产生刚性；却没有解释任意有限初态为什么**必然**进入这种局部语言，因为合法语言本身是从标准 104 轨迹中选出的。

把十称为该特定命题的**最小窗口阈值**是有依据的；把104称为“零冲突本征态”或把这一现象称为已证的热力学相变，则目前缺少对应算子、序参量和无条件吸引定理。[wake_synthesis](../wake_synthesis/) 给出的是明确尾迹几何与算术前提下的进一步刚性，不是所有高速唯一性的全称结论。

## 3. 单调时钟与宏观预算：不要把它们误读成有限燃料

[clock_escape](../clock_escape/) 构造了每一步至少增长一的全状态**整数时钟**，以及一个参数化的临界势函数。它们证明固定有限区域内必然首次离开；正方形上界的指数基底 `3` 出现在势函数权重与范围里。这里**没有**证明真实轨迹模拟了三进制加法器，也**没有**证明最坏运行时间具有对应指数下界。

[factor_language](../factor_language/) 对每个真实有限轨迹区间给出

```text
3(t-s) - 26(|B_t|-|B_s|) <= 351 N10(s,t) + 322 .
```

令 `T=t-s`、`DeltaM=|B_t|-|B_s|`，它约束的是三者的共同变化：

```text
N10(s,t) >= [3T-26 DeltaM-322]/351 .
```

**方向不可颠倒。** 低黑格增长率强迫足够多的违例，并非违例必然耗尽某个初始库存。上述六格族甚至否定了“总违例数只依赖初始黑格数量”的任意有限统一上界。完整双色更新还具有可逆性；没有另行建立熵与统计测度前，不称其为严格非平衡热力学定律。

## 4. 条件性的线性化：XOR、半线性与几何保护

[defect_synthesis](../defect_synthesis/) 证明在**固定质量/违例预算**和完整、覆盖的有限幂次模板下，输入坐标与有限可达关系可以有效地落入 Presburger/半线性算术；给定模板的首读成本与违例数具有分段仿射结构。

[one_black](../one_black/) 与 [four_cell_port](../four_cell_port/) 展示无限参数的受保护轨迹、有限列车和历史残留的精确 XOR 处理。它们证明**在指定保护条件成立时**可以使用代数宏；并未证明任意碰撞都可分解或整个系统可积。

“像孤立子”的比喻可以提示下一步去验证两次、三次散射的完整残余是否组合闭合，但不能直接当成多体散射律。

## 5. 宏观秩序的关键：预测等价，而非删除历史

完整经典蚂蚁演化可逆，而我们关心的未来转向或接口响应可以比完整黑场简单。进入标准高速**不要求**不同初态的完整黑场最终相等：未再次读取的尾迹与残余仍然存在。

指定一个严格定义的交互接口 `I`，允许请求序列 `u`；令 `Resp_I(X,u)` 为真实、**连续保留中间完整场**的响应。可以研究

```text
X ~_I Y   iff   every allowed finite request word u
                   gives the same observations and compatible residual replies.
```

若能对正确的宏步骤 `G` 证明一个可计算压缩 `pi` 满足

```text
pi(G(X)) = G_bar(pi(X)),
```

并证明每个被覆盖的**真实物理交互**都被表示，这才得到真正的宏观闭合动力学。一个需要“未来不会再次读取此格”才能决定的状态删减，仍是语义上的愿望，不是可执行商系统。

[four_row_escape](../four_row_escape/) 已给出成功但有限域的样板：在固定四行、同侧反复进入并保留残余颜色的接口下，每个方向/奇偶扇区恰有 269 种响应类型；真实加列操作保持闭合，随后加权图处理耗时。它不代表全平面的状态数有限，却展示了**如何严格证明一个高层描述确实独立运作**。

## 6. 一个需要验证而非宣布的统一解释

```text
局部有限规则
   -> 真实写入历史
   -> 对旧格的有序重访
   -> 可继续制造/读取的新历史？ ----- 或 ----- 残余不再参与指定未来
                                      |
                                      v
                            可组合的宏观响应类型？
```

真正需要区分的是：保存的记忆（black/written field）、**将来可实际消费的记忆**（causal influence）、以及预测目标允许忽略的残余（observational equivalence）。黑格数量、缺陷数、轮廓数、初始支持直径都不能直接代替三者。

**跨系统可迁移的方法论：** 在 Turmites 或其他自写网格代理上，先明确完整微观状态与合法物理接口，再寻找对未来响应封闭的宏观等价关系；用明确的失败见证改进等价类，而不要先宣布“隐藏可积性”“耗散相变”或“有限资源必终止”。

后续的**可证伪研究任务、失败标准和严格接受条件**在 [NEXT_QUESTIONS.md](NEXT_QUESTIONS.md)。所有严谨定理仍以对应模块的 `PROOF.md` 为准。
