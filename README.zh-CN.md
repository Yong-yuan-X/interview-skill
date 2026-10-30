# interview-skill

面向 0–3 年经验开发者的实用型 AI 面试 Skill，基于岗位 JD 和简历，提供技术面、综合面和 HR 面的模拟训练与结构化复盘。

[English](README.md)

## 安装到 Codex

将下面的提示词直接复制给 Codex，由内置的 `$skill-installer` 从 GitHub 下载并安装，无需手动下载或克隆项目。此方式需要 Codex 能运行安装器的 Python 脚本并访问 GitHub。

```text
$skill-installer 请从 https://github.com/Yong-yuan-X/interview-skill 安装 interview-skill。
技能入口位于仓库根目录 SKILL.md，请使用 --repo Yong-yuan-X/interview-skill --path . --name interview-skill，保留 references/、assets/、scripts/ 等配套文件。
```

## 使用方法

安装完成后，从下一轮消息开始通过 `$interview-skill` 调用。新面试需提供目标岗位 JD 和个人简历，项目链接、代码和作品集可选。

默认采用真实模拟、技术面，可自行指定模式、类型和目标经验级别。目标级别优先按用户指定，其次参考 JD 的明确要求；仍不明确时会询问。例如：

```text
$interview-skill 开始面试。
模式：教练模式；面试类型：技术面；目标级别：校招／应届。
我接下来会提供 JD 和简历。
```

| 模式 | 用途与反馈 |
| --- | --- |
| 真实模拟 | 全轮结束后统一反馈 |
| 教练训练 | 每道主问题及其追问结束后反馈 |
| 历史复盘 | 分析已有面试记录或报告，无需新 JD 和简历 |
| 薄弱点复测 | 针对已有薄弱点换题复测，默认全轮结束后反馈 |

### Python 与评分

评分脚本需要 Python 3.10+，仅使用标准库。无 Python 或无法执行脚本时，仍可面试并按公式评分，报告会注明未运行脚本。详见 [评分规则](references/evaluation.md#run-the-scoring-script) 和 [脚本说明](references/scoring-input.md)。

### 技能未被识别时

若无法调用，请重启 Codex；仍未识别时，让 Codex 检查安装目录、技能名称及资源完整性。

## 示例与验证

查看[中英文 AI 合成面试示例](examples/synthetic-interview/README.md)，包含原始对话、评分报告与验证记录。验证范围和已知问题见各示例说明。

## 后续更新

本 Skill 仍在设计与开发中，参考了与来自 Tencent、Google、OpenAI、ByteDance 等企业的 HR 个人交流时获得的建议，持续打磨面试流程与反馈设计，力求让训练更贴近真实求职场景。相关建议不代表其任职企业的官方立场。欢迎 Star ⭐，关注后续更新！
