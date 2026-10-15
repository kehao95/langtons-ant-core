# 旧黑格读取：全输入有限等待定理

本包不假设轨迹位于固定带、回退有界或黑格质量有界。

给定完整有限状态 X 和 D>=1，定义 S_D：当前格为黑格，而且精确逆推的
前 D 次更新都没有读取该格。这是当前状态上的有限局部谓词。

令 Q=2^D，R 为全部黑格相对蚂蚁的最大无穷范数距离。证明：首次 S_D
事件若会发生，必须发生在 Q(R+2Q+10) 步之前；否则永远不发生，且得到
永久非零平移周期。程序通过有限转弯后缀和整数射线交点核验，无需逐步
运行到远方碰撞时刻。对固定 D，以黑格稀疏列表和二进制坐标为输入，
该首次事件判定的位复杂度是多项式；D 可变时上界为 2^{O(D)} 乘输入长度的多项式。

```sh
python check.py
```

```python
from stale_memory import State, first_stale_read
result = first_stale_read(State(frozenset()), D=128)
print(result['kind'], result.get('event_time'))  # stale_read 197
```

结果 `stale_read` 不是 HIGHWAY 的 NO，也不是非周期证明；
`permanent_no_stale` 证明特定 D 的事件永远不发生，并带有平移周期证据；
用户设置资源上限时可能返回 `inconclusive`。

还证明第 n 次事件若存在则有显式截止界，以及“初态之后制造的黑格被
延迟超过 D 步后消耗”的首次事件截止界。完整证明见 `PROOF.md`。

**没有完成全局非通用性证明。** 无限次重新制造和读取旧黑格仍未被排除；
本包解决一族局部目标，不是任意 HALT 谓词或全局 HIGHWAY 判定。
