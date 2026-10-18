# L4 · 像素人间 / Pixel Mundane

**把异常、预算与退出路径写进工作流。**

GROUNDSTATE 的多模态工程节点。关注从模型输出到可用结果之间的解析、重试、回退、成本记录与人工复核。

当前状态：**v0.1 离线事件回放器**。用预先记录的适配器事件测试尝试次数和回退路径，不调用模型、浏览器、文件执行器或外部服务。

## 先运行

Python 3.11+，仅标准库。

```bash
python bounded_runner.py examples/fallback-replay.json
python -m unittest discover -s tests -v
```

演示输入包含一次超时、一次错误和一次回退成功，最多消耗三次尝试。`fallback` 存在时预留一次尝试；主路径提前成功则不触发回退。没有可接受结果时输出 `needs_review`，不编造完成结果。

## 当前“接受”的含义

事件 `status` 为 `ok` 且 `payload` 为非空 JSON 对象，才被结构性接受。它不验证语义正确性、事实、授权或任务完成。结果仅是输入事件的回放，`external_actions_executed` 始终为 0。

`reported_cost` 是可选的、由输入方提供的非负数，单位由记录约定。任一尝试费用未知时总额为 `null`，同时保留已知小计。它不查询供应商价格，也不估算成本节约率。

[适配器约定](docs/adapter-contract.md) 描述后续如何接入真实任务。工具执行、超时取消、幂等与持久化仍待实现。

[总纲](https://github.com/nova-frontier/manifesto) · [提出问题](https://github.com/nova-frontier/mundane-agent-kits/issues) · [贡献](CONTRIBUTING.md) · [MIT](LICENSE)
