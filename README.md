# interview-skill

A practical AI interview skill for developers with 0–3 years of experience, offering JD- and resume-based technical, comprehensive, and HR interview practice with structured reviews.

[简体中文](README.zh-CN.md)

## Install in Codex

Copy this prompt into Codex. Its built-in `$skill-installer` downloads and installs the skill from GitHub; you do not need to download or clone the project manually. This route requires Codex to be able to run the installer's Python script and access GitHub.

```text
$skill-installer Install interview-skill from https://github.com/Yong-yuan-X/interview-skill.
The skill entry point is SKILL.md at the repository root. Use --repo Yong-yuan-X/interview-skill --path . --name interview-skill and keep supporting files, including references/, assets/, and scripts/.
```

## Usage

After installation, invoke `$interview-skill` in your next message. For a new interview, provide the target JD and your resume; project links, code, and portfolios are optional.

The default is a realistic technical interview. You can specify the mode, interview type, and target experience level. The target level follows your choice, then a clear JD requirement; otherwise, the skill asks you to clarify. For example:

```text
$interview-skill Start an interview.
Mode: coaching; interview type: technical; target level: new graduate.
I'll provide the JD and resume next.
```

| Workflow | Purpose and feedback |
| --- | --- |
| Realistic simulation | Consolidated feedback at the end of the round |
| Coaching | Feedback after each main question and its follow-ups |
| Historical review | Analyze existing records or reports; no new JD or resume required |
| Weakness retest | Test previously weak areas with new questions; feedback at the end by default |

### Python and scoring

The scoring script requires Python 3.10+ and uses only the standard library. If Python or script execution is unavailable, interviews can still proceed and scores can be calculated using the formula; the report will state that the script was not run. See the [scoring rules](references/evaluation.md#run-the-scoring-script) and [script instructions](references/scoring-input.md).

### If Codex does not recognize the skill

If you cannot invoke the skill, restart Codex. If it is still missing, ask Codex to check the installation directory, skill name, and supporting files.

## Examples and validation

See the [Chinese and English AI synthetic interviews](examples/synthetic-interview/README.md) for original dialogues, scored reports, and validation records. Each run documents its verification scope and known issues.

## Future updates

This skill is still being designed and developed. Insights from personal conversations with HR professionals at Tencent, Google, OpenAI, and ByteDance help refine the interview flow and feedback to better reflect real-world job interviews. These suggestions do not represent their employers' official positions. Star this repository ⭐ to follow future updates!
