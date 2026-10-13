这是一份针对手稿《Every One-Black-Cell Langton Ant Reaches the Period-104 Highway: A Lean-Checked Proof》的审稿与编辑评审报告。本评审聚焦于论文的论证节奏、叙事韵律、章节结构、读者引导以及证明体系架构的清晰度，旨在提供坦诚、具体且以突出贡献为核心的修改意见。

本评审不涉及独立运行代码或对底层数学真理性的形式化认证，亦未查看未渲染的图片图形外观，仅依据所提供的完整手稿文本进行文本学与论证逻辑维度的审读。论文题目固定不变。

---

### 一、 宏观阅读体验与核心叙事线索 (Overall Reading Experience & Core Narrative)

本篇论文在数学写作上展现出了高度的严谨性与结构条理性。作者面对的是一个经典且极具挑战性的离散动力系统问题：将已知的空白平面公路收敛性，推广到包含单个任意初始黑格（缺陷）的全局无界初始状态空间。

**论文的核心数学叙事并非简单的“通过大规模计算机辅助暴力搜索完成穷举”，而是一套精巧的“离散孤立缺陷几何散射理论”（Geometric Scattering Theory for Solitary Defects）：**
1. **降维与截断**：利用有限步空白前缀（9,977步）将全平面 $\mathbb{Z}^2$ 划分为“早期前缀碰撞”与“未触碰后期缺陷”；
2. **仿射通道化**：利用 P104 轨道的时空周期性，将二维无界平面的后期缺陷严格投射到有限个（22个）一维仿射前沿通道 $q = h + dv$；
3. **几何解耦与纯净散射**：剥离复杂的历史唤醒痕迹，在纯净背景下证明深层缺陷沿通道平移等价于干净公路与固定异或（XOR）尾流的叠加，从而使归纳法得以封闭；
4. **历史恢复与 $21+1$ 分歧**：当恢复真实的 702 格历史唤醒区时，动力系统分化为两类迥异的物理图像——21 个普通通道因向前逃逸而与历史唤醒区空间分离；唯独第 22 个通道（Phase 72）发生精确的“反向回散射”，产生反向公路折返并撞击历史区固定单元格，随后经过一段可验证的有限瞬态重新折入正向公路。

**阅读体验的主要症结：**
目前手稿在整体叙事韵律上存在“**证书与实现细节抢占理论叙事焦点**”的倾向。摘要与引言过早堆砌了具体的数字常量（如 9,977, 1,376, 702, 208, 22 等）和 Lean 的验证机制细节，使得读者在尚未完全建立起“几何散射与通道归纳”的物理直觉之前，便被大量证书记账符号所淹没。如果能适当理顺从“物理直觉”到“代数归纳”再到“形式化计算边界”的展开层次，本篇论文的理论穿透力和可读性将显著提升。

---

### 二、 逆向大纲与结构平衡分析 (Reverse Outline & Structural Balance)

#### 1. 各主要章节的作用与读者收获 (Section Payoff)

*   **Abstract & Section 1 (Introduction)**
    *   *作用*：界定 Langton 蚂蚁背景与公路猜想，确立单黑格无界全域收敛定理（Theorem 1.1），给出证明架构全景图（Figure 1）。
    *   *读者收获*：明确本文的主定理、无界性挑战以及基于通道分类与 Lean 形式化的解决路线。
*   **Section 2 (Dynamics, symmetries, and the main theorem)**
    *   *作用*：形式化定义状态机、观察量、四分之一旋转对称性（Lemma 2.2），以及 P104 稳态判定式（Definition 2.1）和空白基准态 $E$ 的边界属性（Proposition 2.3）。
    *   *读者收获*：获得无歧义的操作性定义，理解为何只需研究原点朝北的规范化单黑格状态 $\sigma_q$。
*   **Section 3 (The finite prefix and first-contact coupling)**
    *   *作用*：基于 9,977 步空白轨迹的前缀读集合 $P$（1,376 格）建立一阶差异耦合（Lemma 3.2）与未触碰进入定理（Corollary 3.3）。
    *   *读者收获*：清晰将全平面二分化：落在 $P$ 内的有限搜索 vs. 落在 $P$ 外并直接继承进入状态 $\operatorname{blacken}(q,E)$ 的未触碰状态。
*   **Section 4 (Entry geometry and the 22 frontier channels)**
    *   *作用*：通过 P104 的 40 格支撑集与前进漂移向量 $v$ 定义前沿头集合 $H$（$|H|=22$），并建立进入划分（Proposition 4.1）。
    *   *读者收获*：空间降维完成：无界平面问题被压缩为 22 条一维射线族 $\Sigma_E(h,d)$。
*   **Section 5 (Pristine single-defect scattering)**
    *   *作用*：引入剥离历史的纯净基准态 $B$；建立 XOR 档案归纳原理（Lemma 5.1）；完成纯净散射全深度分类（Proposition 5.2），发现 21 正向 vs. 1 反向的 $21+1$ 谱系。
    *   *读者收获*：理解为何平移缺陷等价于尾流档案叠加，并获知 Phase 72 的反向公路现象。
*   **Section 6 (Restoring the physical history: 21 ordinary channels)**
    *   *作用*：恢复 702 格历史唤醒区 $H_E$，引入通道截止深度 $A_h$，证明几何射线与历史分离引理（Lemma 6.1），封闭 21 个普通物理通道（Proposition 6.2）。
    *   *读者收获*：理解普通通道在足够深之后如何彻底摆脱历史干扰。
*   **Section 7 (Exceptional backscattering and the affine hit law)**
    *   *作用*：深入解析 Phase 72 异常通道：反向公路块、首碰撞点 $c=(20,-22)$、仿射碰撞时间律 $t_{\mathrm{hit}}(n) = t_{\mathrm{hit}}(0) + 208n$（Equation 3）及后碰撞尾部归纳（Proposition 7.1）。
    *   *读者收获*：获得全篇数学上最富技巧性、最生动的动力学碰撞归约与封闭证明。
*   **Section 8 (Universal assembly)**
    *   *作用*：统摄所有分支完成 Theorem 1.1 的综合证明，展示全局证明划分图（Figure 6）。
    *   *读者收获*：见证整个逻辑闭环的完成，确立全平面的无漏洞覆盖。
*   **Section 9 (Lean formalization and finite computation)**
    *   *作用*：说明 Lean 4 模块依赖结构（Table 1）、三片计算叶子、`native_decide` 的可信计算基底（TCB）与复现方式。
    *   *读者收获*：清楚了解形式化证明与本地可执行代码之间的信任边界。
*   **Section 10 & 11 (Related work & Conclusion)**
    *   *作用*：对比文献（Bunimovich-Troubetzkoy, Gajardo 等），总结成果并展望多缺陷问题。
    *   *读者收获*：理解该方法在元胞自动机/离散动力系统领域的坐标。
*   **Appendix (Certificate inventory)**
    *   *作用*：集中列出全部 checked 常量表（Table 2）。
    *   *读者收获*：清晰的数据查阅索引。

#### 2. 结构失衡与行文阻滞分析

*   **前轻后重 vs. 概念突兀**：Section 4 到 Section 5 的过渡缺乏充分的概念铺垫。在 Section 4 结尾处刚定义了带有历史的物理进入态 $\Sigma_E(h,d)$，Section 5 开头突然出现“剥离历史的纯净基准态 $B$”，而未提前向读者解释*为什么*必须先研究纯净态（即平移不变性与 XOR 尾流叠加的代数封闭性）。
*   **Section 6 的代数代入过急**：Section 6 开篇直接罗列参数 $A_h, P_h, L_h$，没有先从几何直觉上与 Section 7 形成对比：为何普通通道只要“走得够深”就能远离历史，而异常通道却“无论多深都会掉头撞向历史”。
*   **Section 8 中代码侵入叙事**：Section 8 在给出 Theorem 1.1 的综合证明后，立刻插入了 Lean 代码行，打断了数学结论落地的叙事高潮，而这些代码完全可以更自然地统一放在 Section 9 中阐述。

---

### 三、 优先编辑问题清单 (Prioritized Editorial Issues)

此处列出 6 项具体的审稿修改建议，按优先级排序，并明确区分“必要澄清”与“风格优化”，文末单独列出未经验证的算法/数学检查点。

---

#### 1. [High Priority - 读者引导] 摘要与引言中“数字记账”过密，遮蔽了散射几何的核心机制
*   **所属章节**：Abstract & Section 1 (第 1-2 段)
*   **原文锚点 (Verbatim Anchor)**：
    > `Twenty-one channels admit an ordinary scattering induction after a channel-specific finite cutoff. The remaining channel first creates a reverse period-104 highway... Three closed finite reports---the blank highway, 1,376 prefix contacts, and the shared scattering certificate---are evaluated with \texttt{native\_decide}.`
*   **读者困难**：摘要与引言第一页塞入了过多孤立常量（9,977, 22, 21, 208, 1,376, 702 等）与实现层词汇（`native_decide`, artifact），使得数学读者在尚未理解“为什么单黑格问题能被视作网格散射”之前，先产生了这是一份系统性能或测试基准报告的错觉。这冲淡了论文最精彩的动力学概念贡献。
*   **性质**：风格优化与读者认知对齐（Stylistic Preference & Reader Orientation）。
*   **具体修改方案**：
    在摘要中弱化单纯数字的连续罗列，强化概念链条：“有限前缀截断 $\to$ 二维向一维仿射通道投影 $\to$ 纯净背景下的 XOR 尾流归纳 $\to$ 恢复历史后的空间逃逸与反向碰撞定律”。将具体的计算叶子名称放在方法说明段落，使摘要前三分之二纯粹服务于动力系统数学图景。

---

#### 2. [High Priority - 证明架构] Section 5 开篇引入“纯净态 $B$”缺乏数学动机解释
*   **所属章节**：Section 5 (第 1 段)
*   **原文锚点 (Verbatim Anchor)**：
    > `The physical state $E$ contains both the active P104 pattern and the entire blank-orbit wake. It is useful first to remove the history and study a pristine boundary state $B$ containing only the 13-cell active pattern with the same pose.`
*   **读者困难**：读者在此处会产生困惑：物理上真实存在的是带有 702 格唤醒历史的 $E$，为什么此时要构造一个人造的、剥离了历史的 $B$？作者没有解释“为什么先除掉历史是必要的数学手段”。本质原因在于：**在全白背景下，周期公路的步进具有严格的空间平移不变性，这使得更深缺陷的相互作用可以精确展开为周期位移与 XOR 差分尾流的代数和；而历史唤醒区打破了这种平移不变性。** 缺少这层点拨，纯净态 $B$ 显得突兀而刻意。
*   **性质**：必要澄清（Necessary Clarification）。
*   **具体修改方案**：
    在第 5 节开头增补动机说明，阐明隔离历史的数学收益——恢复局部网格的平移周期对称性，从而允许通过 XOR 形式代数建立严格的障碍平移归纳法；随后再在第 6、7 节将历史作为固定的非平移障碍逐一恢复。

---

#### 3. [Medium Priority - 概念与代数节奏] Section 5.1 在给出代数公式前缺少对“Same-Outside”几何直觉的交代
*   **所属章节**：Section 5.1 (第 1-2 段)
*   **原文锚点 (Verbatim Anchor)**：
    > `After $n$ clean blocks the difference has the form $$\mathcal A_n(W)=W\oplus(W+v)\oplus\cdots\oplus(W+(n-1)v).$$ ... The proof relates this algebra to orbit equality through a \emph{same-outside} relation: two grids may differ on an archive, but generate identical updates while the common ant path avoids it.`
*   **读者困难**：作者先写出了公式 (1) 的异或累加和 $\mathcal{A}_n(W)$，随后给出了包含 3 个假设的 Lemma 5.1，最后才用半句话附带提及了关键概念 `same-outside`。读者面对公式 (1) 时，难以直观理解“为什么网格可以在很多历史单元格上存在差异，但轨道却完全相同”。事实上，“蚂蚁路径绝不踏入已被修改的差分档案（frozen wake），因而轨道演化对这些差异完全脱敏”是整篇论文归纳法的心脏。
*   **性质**：必要澄清（Necessary Clarification）。
*   **具体修改方案**：
    重构 Section 5.1 的段落顺序：先用几何语言定义“网格差异与蚂蚁轨迹的空间不相交性”（即只要轨迹避开差分集，局部动力学就等同于在未受扰动的网格上运行），再自然引出为什么每增加一个周期的深度，只会在背后沉淀出一个“永久被遗弃的冻结尾流 $W$”，最后再写出公式 (1) 与 Lemma 5.1。

---

#### 4. [Medium Priority - 叙事节奏与反差] Section 6 开篇缺少与 Section 7 的几何宏观对比
*   **所属章节**：Section 6 (第 1-2 段)
*   **原文锚点 (Verbatim Anchor)**：
    > `Write $H_E=\{x:E(x)=1,\ x\notin S\}$. The exact entry certificate gives $|H_E|=702$. For an ordinary head $h$, let $A_h$ be one plus the length of its checked physical direct row. The certificate verifies $P_h\le A_h$.`
*   **读者困难**：Section 6 开篇直接抛出一连串索引符号（$H_E, A_h, P_h, L_h$），缺乏对“为什么 21 个通道是平凡的（Ordinary）”这一几何本质的阐述。读者的视野被限制在微观的索引对齐计算中，失去了宏观图景：**这 21 个通道之所以容易，是因为它们散射出的最终公路方向始终朝向前方或侧方逃逸，随着深度 $d$ 的增加，整个散射包络线与射线锥最终完全移出了位于原点附近的有限历史云 $H_E$；反之，第 22 个通道之所以困难，是因为它转头朝后开回了历史云中。**
*   **性质**：风格优化与叙事节奏（Stylistic Preference & Narrative Rhythm）。
*   **具体修改方案**：
    在 Section 6 开头加入一个高视角的引导段落，建立“空间逃逸锥 vs. 有限历史云”的几何直觉，解释截止深度 $A_h$ 的物理含义就是“完全脱离历史影响的临界深度”，然后再展开具体的参数与引理。

---

#### 5. [Low Priority - 结构洁净度] Section 8 结尾处的 Lean 标识符与代码打断了数学结论的完备感
*   **所属章节**：Section 8 (正文末尾)
*   **原文锚点 (Verbatim Anchor)**：
    > `In Lean, the same assembly is exposed at three levels. The theorem \texttt{Scattering.single\_defect\_scattering} constructs the $21+1$ classification... Finally the exported statement is literally \begin{verbatim} theorem OneBlack.universal_one_black : ∀ s, ExactlyOneBlack s → ReachesP104 s \end{verbatim}`
*   **读者困难**：Section 8 是数学证明的大结局（Universal Assembly），证明了 Theorem 1.1 并给出了全景图 Figure 6。然而在证明刚刚落幕之处，突然穿插了几个具体的 Lean 定理名字和一段裸露的 Lean 代码块，随后紧接着的 Section 9 又是系统性的“Lean formalization”。这种前后穿插打乱了数学总结的厚重感，显得局部排版不够纯粹。
*   **性质**：风格优化（Stylistic Preference）。
*   **具体修改方案**：
    让 Section 8 保持纯粹的数学收束，聚焦于几何与归纳覆盖的完整性；将这几行 Lean 代码与逐层引出关系平移到 Section 9.1（Proof cone）中统一交代。

---

#### 6. [未经验证的技术检查点 - 供作者自查] Definition 2.1 的相位对齐约定与 Equation (4) 的层漂移符号
*   **所属章节**：Section 2.1 (Definition 2.1) 及 Section 7.2 (Equation 4)
*   **原文锚点 (Verbatim Anchor)**：
    *   锚点 A：`In addition its first 104 read colours must equal the fixed word $w_r=...$ A state reaches P104 if $\operatorname{run}(N,s)$ has permanent P104 for some $N\ge0$.`
    *   锚点 B：`$$\operatorname{run}(t_{\mathrm{hit}}(n),\Sigma_E(h_{72},15+n)) = C\oplus\bigoplus_{j=0}^{n-1}(L+jv).$$`
*   **技术自查逻辑与建议**：
    1.  *关于 Definition 2.1 的相位匹配*：定义中明确要求在时间 $N$ 之后的最初 104 个读取颜色必须严格等于空白轨道从 9,977 步开始的固定字 $w_r$（$0 \le r < 104$）。这隐含了一个强约束：状态必须在模 104 的特定“0 相位”处切入公路。尽管在数学上这是完全自洽的（因为如果一个状态在某个非零相位进入公路，只需将 $N$ 向后顺延相应步数以对齐相位 0 即可），但正文中未对“$N$ 的选取始终可以模 104 对齐到标准相位 0”做一句话说明，初读时容易引起审稿人关于“是否存在相位滑动（phase shift）导致无法直接匹配字 $w_r$”的疑虑。建议在定义后加一句澄清。
    2.  *关于 Equation (4) 中漂移向量 $v$ 的正负号与层定义*：在公式 (4) 中，异或项为 $\bigoplus_{j=0}^{n-1}(L+jv)$。已知正向漂移是 $v=(-2,-2)$，反向公路漂移是 $v_r = (2,2) = -v$。深度每增加 1，障碍物在几何上向 $v$ 方向推进了一格。反向公路的起点也向 $v$ 方向延伸了一格。因此，这往返的额外 208 步轨迹所沉淀出的合成尾流层 $L$ 的平移量正是 $+jv$。此处的符号在数学推导上十分优雅，但正文未详细定义 $L$ 到底包含哪些部分（即 $L$ 是单次正向延展尾流与反向回程尾流的复合差分）。建议在正文中明确注明：$L$ 是插入的一个正向块和一个反向块所留下的净 XOR 差分，因此每次增加深度，该差分足迹在空间上整体平移 $+v$。

---

### 四、 建议的结构调整与大纲编排 (Proposed Order & Outline)

**结论：手稿不需要大拆大建式的宏观章节重组。**
现有的章节推进路线（规范化 $\to$ 前缀截断 $\to$ 通道降维 $\to$ 纯净散射 $\to$ 普通历史恢复 $\to$ 异常反向碰撞 $\to$ 综合定理 $\to$ 形式化）非常符合离散几何与动力系统论文的最佳实践。

**建议进行的局部微调（Micro-adjustments）：**

1.  **Section 1 & Abstract**：
    *   精简数字记账，重塑引言节奏：在第 1 节第 3 段引出 Theorem 1.1 之前，强化“从二维无界到有限条一维通道的几何投影”直觉。
2.  **Section 5.0 (前置动机段落)**：
    *   在 Section 5 开头增加一段关于“为什么引入纯净态 $B$”的过渡，阐明其核心目的是**恢复平移对称性以支持 XOR 归纳**。
3.  **Section 5.1 (重排局部顺序)**：
    *   将 `same-outside` 的几何原理前置到公式 (1) 和 Lemma 5.1 之前。
4.  **Section 6.0 (对比引导段落)**：
    *   在 Section 6 开头建立“前向逃逸 vs. 逆向折返”的宏观对比，解释 $A_h$ 的几何本质。
5.  **Section 8 $\to$ Section 9 的代码收口**：
    *   将 Section 8 末尾的 Lean 代码块与具体引理名称移入 Section 9.1，使 Section 8 成为纯粹的数学闭环。

---

### 五、 针对核心问题的三处英文重写建议 (Three Concrete Paragraph Rewrites)

以下提供三处英文段落重写，旨在解决上述影响最大的叙事断层与概念突兀问题。重写严格保留了原有的数学假设与界限，不增添任何未证明的主张。

---

#### Rewrite 1: 增补 Section 5 开头的动机过渡（解释为何需要纯净态 $B$）

*   **修改目标**：解决 Issue 2。在引入 $B$ 之前，向读者解释剔除历史是恢复空间平移对称性的关键步骤，使后续的 XOR 代数归纳顺理成章。
*   **替换原句**（Section 5 开头两句话）：
    > *Existing text:*
    > "The physical state $E$ contains both the active P104 pattern and the entire blank-orbit wake. It is useful first to remove the history and study a pristine boundary state $B$ containing only the 13-cell active pattern with the same pose."

*   **建议替换为 (Proposed Rewrite)**:
    > "At the physical boundary $E$, the active 13-cell highway pattern is embedded alongside an accumulated 702-cell historical wake. Because this static history breaks the spatial translation invariance of the surrounding lattice, analyzing perturbations directly in $E$ confounds the local dynamics of the obstacle with the geometry of past footprints. To isolate the intrinsic scattering mechanism, we first study a pristine boundary state $B$ consisting solely of the active pattern on an otherwise all-white plane, preserving the pose of $E$. In this pristine environment, translating an obstacle by the drift vector $v$ corresponds to shifting the clean highway by exactly one temporal cycle, allowing obstacle increments to be tracked as translation-invariant XOR wake deposits. Once this pristine dynamics is established, Sections~\ref{sec:ordinary} and~\ref{sec:exceptional} restore the physical history as a fixed geometric background."

---

#### Rewrite 2: 重构 Section 5.1 的展开逻辑（在代数公式前先解释 Same-Outside 原理）

*   **修改目标**：解决 Issue 3。在呈现异或累加和公式 (1) 与 Lemma 5.1 之前，先阐明“轨迹脱敏于冻结尾流”的直觉，使代数形式与归纳假设易于理解。
*   **替换原句**（Section 5.1 前两段）：
    > *Existing text:*
    > "For Boolean grids, finite changes compose by exclusive-or. Let $W$ be the finite difference between one clean 104-step block and its translated target... After $n$ clean blocks the difference has the form $$\mathcal A_n(W)=W\oplus(W+v)\oplus\cdots\oplus(W+(n-1)v).$$ The XOR expression retains cancellation between overlapping wakes. The proof relates this algebra to orbit equality through a \emph{same-outside} relation: two grids may differ on an archive, but generate identical updates while the common ant path avoids it."

*   **建议替换为 (Proposed Rewrite)**:
    > "The dynamics on Boolean grids composes local modifications via exclusive-or. Crucially, the ant's update at any moment depends solely on the single cell under its current position. Consequently, if two configurations differ only on a subset of cells that the ant never subsequently visits—a condition we formalize as being *same-outside* that subset—their resulting trajectories and observation sequences remain identical. When an obstacle is displaced by one additional period $v$ down a channel, the ant traverses one additional undisturbed P104 cycle before colliding, depositing a localized footprint difference $W$ before resuming its anchored path. As depth increases by $n$ periods, these differences accumulate into an archived wake:
    > $$
    > \mathcal A_n(W) = W \oplus (W+v) \oplus \cdots \oplus (W+(n-1)v),
    > \tag{1}\label{eq:archive}
    > $$
    > where exclusive-or accounts for potential cancellations in overlapping regions. Provided the forward trajectory remains geometrically separated from this accumulated archive, the perturbed orbit behaves exactly like the base scattering event modulo frozen, unvisited background differences."

---

#### Rewrite 3: 重写 Section 6 开篇引导（建立普通通道与异常通道的几何反差）

*   **修改目标**：解决 Issue 4。在列出截止深度 $A_h$ 与历史单元格集合 $H_E$ 之前，向读者提供“前向逃逸锥”的几何直觉，使读者理解为何通道特异性截止深度足以封闭这 21 个通道。
*   **替换原句**（Section 6 开头前两段）：
    > *Existing text:*
    > "Write $H_E=\{x:E(x)=1,\ x\notin S\}$. The exact entry certificate gives $|H_E|=702$. For an ordinary head $h$, let $A_h$ be one plus the length of its checked physical direct row. The certificate verifies $P_h\le A_h$."

*   **建议替换为 (Proposed Rewrite)**:
    > "Having resolved pristine scattering, we now restore the 702 physical historical cells $H_E = \{x : E(x) = 1,\ x \notin S\}$. The decisive structural dichotomy is geometric: for 21 of the 22 frontier channels, the outgoing scattering trajectory and its eventual P104 corridor propagate outward in directions that permanently move away from $H_E$. While shallow obstacles in these channels may collide with historical cells, pushing the obstacle sufficiently deep translates the entire scattering footprint past the historical cloud. For each such ordinary head $h$, there exists a finite cutoff depth $A_h$ beyond which the obstacle is far enough down the lane that neither the finite scattering transient nor the infinite terminal highway ever intersects $H_E$. Depths below $A_h$ are verified by finite replay, while depths $d \ge A_h$ reduce directly to the pristine archive induction through geometric separation."

---

### 六、 极简修改执行计划 (Minimum-Change Revision Plan)

为了以最小的代码和行文扰动换取最大的可读性改善，建议作者按以下 4 步推进修订：

*   **Step 1: 润色摘要与引言的先导叙事 (Polish Abstract & Intro Leads)**
    *   将摘要中密集的离散数字和 `native_decide` 提法稍微后置或浓缩为方法论概述，突出“几何降维到 22 仿射通道 $\to$ 纯净平移不变性与 XOR 归纳 $\to$ 物理历史恢复与反向回散射定律”的理论主线。
*   **Step 2: 植入关键动机与概念引导过渡句 (Insert Motivational Transitions)**
    *   采纳 **Rewrite 1**，在 Section 5 开头补充剥离历史的数学动机（恢复空间平移对称性）；
    *   采纳 **Rewrite 2**，在 Section 5.1 中将 `same-outside` 的轨迹脱敏直觉置于异或累加公式之前；
    *   采纳 **Rewrite 3**，在 Section 6 开头引入“前向逃逸锥 vs. 有限历史区”的直觉，解释截止深度 $A_h$ 的几何本质。
*   **Step 3: 净化 Section 8 与 Section 9 的叙事分工 (Disentangle Math Assembly from Lean Code)**
    *   将 Section 8 结尾处的 Lean 定理签名与代码块移至 Section 9.1；
    *   在 Section 2.1 的 Definition 2.1 后补添一句关于“公路进入时刻 $N$ 始终可校准对齐至周期相位 0”的简短说明（消除审稿人对相位滑动的技术疑虑）。
*   **Step 4: 细化 Section 7.2 中关于合成尾流层 $L$ 的文字定义 (Clarify Layer $L$ in Eq. 4)**
    *   在 Equation (4) 之后明确写明：$L$ 是单次深度递增所引入的“一个前向公路块与其对应的反向折返公路块”在往返过程中共同留下的净 XOR 差分，从而使平移量 $+jv$ 的符号和物理图像完全清晰自洽。
