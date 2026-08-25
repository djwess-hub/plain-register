# Plain register for Claude Code

Two Claude Code skills and the rules file they share.

1. `plain-register` rewrites prose into a plain expository register. One idea per sentence, common words, terms defined on first use, no aphorisms or twist endings. It targets roughly a grade-10 reading level. It is meant for documents that go in front of partners, executives or clients.
2. `plain-check` audits prose against the same rules without rewriting it. It comes with `check.py`, a script that finds the mechanical failures a reader's eye skips, such as undefined terms, dangling references, missing verbs and twist endings.
3. `plain-register.md` is the one file that holds the rules. Both skills read it. It also works as a Claude Code output style, so you can make the register apply to every response.

## Install

```
git clone https://github.com/djwess-hub/plain-register.git
cd plain-register
bash install.sh
```

The script copies five files into `~/.claude/` and does not overwrite anything already there. Pass `--force` to overwrite.

If you would rather copy by hand, the layout is:

```
~/.claude/skills/plain-register/SKILL.md
~/.claude/skills/plain-register/stamp.py
~/.claude/skills/plain-check/SKILL.md
~/.claude/skills/plain-check/check.py
~/.claude/output-styles/plain-register.md
```

Then restart Claude Code.

## Use

- `/plain-register path/to/file.md` rewrites a file, runs the check, and stamps the file with the date.
- `/plain-check path/to/file.md` audits a file and reports findings. It does not change the file.
- With no path, either skill works on the text in the conversation.
- To have Claude write every reply in the register, run `/output-style` and pick "Plain register". This is optional.

You can also run the scripts directly.

```
python3 ~/.claude/skills/plain-check/check.py report.md
python3 ~/.claude/skills/plain-register/stamp.py report.md --date 2026-08-25
python3 ~/.claude/skills/plain-register/stamp.py --read report.md
```

## Requirements

- Python 3. Both scripts use only the standard library for `.md`, `.txt` and `.docx`.
- `python-pptx` is needed only if you want `check.py` to read `.pptx` decks. Install it with `pip3 install python-pptx`.

## Why the checker is structural

Readability formulas measure only two things. Those are sentence length and syllable count. A passage can score well and still be too compressed to follow. So `check.py` looks for shapes instead. It separates labels (headings, captions, table cells) from prose, runs sentence-level checks on prose only, and reports candidates for a person to judge. The `plain-check` skill explains how to judge each list.

## Editing the rules

Edit `~/.claude/output-styles/plain-register.md`. Both skills read that file, so one edit changes everything.
