# 贡献到 像素人间

先提交一个具体问题：输入是什么、要检验什么、怎样判定失败、成本边界在哪里。
研究节点是职责划分，不绑定个人、学校或职务。任务可在 Issue 中自愿认领。

1. 新建 Issue，标注 `proposal`、`measurement` 或 `failure-report` 的意图（标签可后续补充）。
2. 提交最小复现：环境版本、输入、运行命令、完整结果和限制。
3. PR 中说明实际完成的工作；运行 `python -m unittest discover -s tests -v`。
4. 示例或模拟数据必须标明来源。真实日志公开前去除身份信息、凭证和未经许可的材料。

仅修正文案时无需新增测试。行为变更应补充能捕获该问题的测试。
跨节点的接口或评价口径请先到 [总纲 RFC](https://github.com/nova-frontier/manifesto/tree/main/rfcs) 讨论。
