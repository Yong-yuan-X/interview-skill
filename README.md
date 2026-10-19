# interview-skill

A practical AI interview skill for real-world job preparation, featuring JD- and resume-based mock interviews, targeted practice, and structured performance reviews.

[简体中文](README.zh-CN.md)

## Future updates

This skill is still being designed and developed. Insights from personal conversations with HR professionals at Tencent, Google, OpenAI, and ByteDance help refine the interview flow and feedback to better reflect real-world job interviews. These suggestions do not represent their employers' official positions. Star this repository ⭐ to follow future updates!

## Install in Codex

Copy this prompt into Codex. Its built-in `$skill-installer` downloads and installs the skill from GitHub; you do not need to download or clone the project manually. This route requires Codex to be able to run the installer's Python script and access GitHub.

```text
$skill-installer Install interview-skill from https://github.com/Yong-yuan-X/interview-skill.
The skill entry point is SKILL.md at the repository root. Use --repo Yong-yuan-X/interview-skill --path . --name interview-skill and keep supporting files, including references/, assets/, and scripts/.
```

## Usage

After installation, invoke `$interview-skill` in your next message. For a first new interview, provide the target JD and your resume. You can also specify the mode, interview type, and target experience level; unspecified settings follow the skill's existing rules. Project links, code, and portfolios are optional. For example:

```text
$interview-skill Start an interview.
Mode: coaching; interview type: technical; target level: new graduate.
I'll provide the JD and resume next.
```

Supported workflows include realistic simulations, coaching, historical reviews, and weakness retests. Historical reviews only require existing interview records or reports.

### Python and scoring

The scoring script requires Python 3.10+ and uses only the standard library. If Python or script execution is unavailable, interviews can still proceed and scores can be calculated using the formula; the report will state that the script was not run. See the [scoring rules](references/evaluation.md#run-the-scoring-script) and [script instructions](references/scoring-input.md).

### If Codex does not recognize the skill

If you cannot invoke the skill, restart Codex. If it is still missing, ask Codex to check the installation directory, skill name, and supporting files.
