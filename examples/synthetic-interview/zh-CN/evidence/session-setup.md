# AI 合成测试：实际会话初始化记录

以下是主代理实际发送给 `collaboration.spawn_agent` 的参数与收到的返回值。没有显式指定模型或推理强度；宿主未返回其实际值，因此相应字段标为“未记录”。

## 候选人

参数：`task_name="synthetic_candidate"`，`fork_turns="none"`。

实际启动消息原文：

> 请读取并执行 E:\.github\interview-skill\examples\synthetic-interview\inputs\candidate-agent-task.md。你是这次 AI 合成测试的独立候选人代理，只使用该任务指定的合成材料和能力设定。当前先准备并按任务返回 READY，之后等待实际面试官问题。

工具返回句柄：`/root/synthetic_candidate`。

候选人实际初始化回复：`READY`。此回复不计入面试对话。

## 面试官

参数：`task_name="synthetic_interviewer"`，`fork_turns="none"`。

实际启动消息原文：

> 请读取并执行 E:\.github\interview-skill\examples\synthetic-interview\inputs\interviewer-agent-task.md。你是这次 AI 合成测试的独立面试官代理，请加载任务指定的已安装 interview-skill 和正常面试资料，开始真实模拟技术面试。每次只完成一轮面试官发言，并按任务保存原文、等待主代理转发实际候选人回复。

工具返回句柄：`/root/synthetic_interviewer`。

## 隔离安装

常见个人安装路径下没有发现 `interview-skill/SKILL.md`，故使用内置安装器在测试目录新增隔离副本：

```text
install-skill-from-github.py --repo Yong-yuan-X/interview-skill --path . --name interview-skill --ref 4f493b07f1e2cdcac0d050a5abbf5b6b620bde93 --dest E:\.github\interview-skill\examples\synthetic-interview\installed-skills --method download
```

实际控制台输出：

```text
Installed interview-skill to E:\.github\interview-skill\examples\synthetic-interview\installed-skills\interview-skill
```

退出码：`0`。主代理随后逐字节核对 18 个已安装文件，全部与记录提交的 Git blob 一致，详见 `installed-snapshot.json`。没有将全局技能发现或全局安装当作已经验证的能力。
