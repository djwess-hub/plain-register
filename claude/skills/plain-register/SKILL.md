---
name: plain-register
description: Rewrite prose into a plain expository register for circulated, executive-facing material. One idea per sentence, common words, explicit connectives, implications spelled out, no aphorisms or compressed pivots. Target roughly grade-10 reading level. Use when the user says "plain register", "simplify the language", "high school reading level", "one concept per sentence", "make it easier to read", or when drafting any document, deck or email that will circulate to partners, executives or clients. Args, an optional path to the file to rewrite. With no args, apply to the material in the conversation.
---

# Plain register

A register for anything that leaves the chat and goes in front of a partner, an executive or a client. It is the default for that kind of document.

Applies to: circulated documents, briefs, memos, board and client material, slide body text, and speaker notes.
Does not apply to: chat, unless the user has turned on the "Plain register" output style. Chat can stay dense, because the reader is present and can ask what a phrase meant.

## The rule

**The rules live in one file. Read it before rewriting anything.**

```
~/.claude/output-styles/plain-register.md
```

That file holds the rule list and a calibration example. It is the only copy. It doubles as the Claude Code output style, so the skill and the style stay in step and cannot drift apart.

Edit the rules there, never here.

What this skill adds on top of those rules is the procedure below. That covers how to work through a document, what to check before returning, and how to stamp the result.

**Stop doing this**, restated here as the short version of what to hunt for:

- Compressed aphorisms. "Dashboards depreciate, models appreciate."
- Paraprosdokians. A setup, then a twist ending that makes the reader re-read the setup. "Four steps, and only one of them is yours." "Everything about billing changed. Your invoice didn't." Hard ban, no exceptions. The rules file has the full definition and a rewrite example.
- Self-narration. The text announcing its own register ("Here is the plain read") or the writer declaring intent or restraint ("so I will stick to what it means"). Delete the announcement and keep the content. The rules file has the full definition and a rewrite example.
- Conceptual pivot phrases that make the reader do the unpacking. "False by construction." "Calendar-bound long poles."
- Surprising word pairings, and large words used in unexpected ways.
- Multi-idea sentences, especially the colon-pivot and the parallel-contrast pair.

Getting wordier is fine and expected. The document's job is transfer, not style.

## How to apply

1. Read the whole piece first. Find the aphorisms and the pivot phrases. They are usually the lines the author is proudest of, and they are the ones that cost the reader the most.
2. Rewrite each one as two or three plain sentences that say the thing directly.
3. Split every sentence carrying more than one idea.
4. Replace uncommon words with common ones, unless the uncommon word is a defined term the audience needs. Then define it on first use.
5. Add the connective that was implied. If two sentences sit next to each other because one causes the other, write "so" or "because".
6. Leave headings, labels, card titles and chart captions short. They are labels, not prose. Do rewrite any label that is itself a compressed pivot.
7. Keep the author's claims exactly. This is a register change, not an edit of the argument. Do not soften, hedge, or drop a point while simplifying it.
8. Do not rewrite code, identifiers, commands, file paths, quoted text, or any prescribed format. That includes quotations from a source, legal or contractual wording, citations, and required templates. Rewriting a quote to make it plainer is misquoting the source. Leave the original intact and put the plain explanation next to it.

## Checks before returning

Run the `plain-check` skill. It is the last step, and it is not optional.

```
python3 ~/.claude/skills/plain-check/check.py <path>
```

That script finds the mechanical failures exactly, rather than by eye. Read the `plain-check` skill for how to judge what it reports, because the script produces candidates and cannot tell a real problem from a false positive.

The failures it looks for are the ones that survive a rewrite most often. Specialist terms left undefined. Metaphors used as nouns, standing in for a real thing that never gets named. References like "this" or "the same X" whose referent sits too far back. Sentences missing a verb. Clauses with the verb elided. Paraprosdokians, in both the one-sentence and the two-sentence shape, in prose and in labels.

Then check by hand what no script can see.

- Confirm every hedge, condition, number and scope limit in the original survived. Simplifying a qualified claim tends to flatten it into a flat assertion. "May hold under these conditions" must not become "is true."
- Confirm nothing got quietly deleted. Length going up is expected.
- Confirm the claims are unchanged. This is a register change, not an edit of the argument.

### Do not trust a readability score

The check script prints Flesch-Kincaid grade and Flesch reading ease. Treat a bad score as proof of a problem. Never treat a good score as proof of success.

Here is why. This paragraph had been through this skill and still read badly.

> The machinery behind it, from the arrangement agreement. Walking away had a price on both sides. The REIT would have paid a $42.1M termination fee, and the buyers a $47.7M reverse fee. [...] The ten-year envelope on the Capex tab is the public-data model of the same object.

It scores grade 7.7 and reading ease 61.3, which beats the grade-10 target. It contains eight separate failures. The formulas measure sentence length and syllable count, and nothing else. This passage is not too wordy. It is too compressed, so every failure hides inside short sentences made of short words.

Rewriting it to fix all eight failures moved the grade by 0.8. That is inside the noise from rewording a single sentence.

## Stamp the file when done

The user needs to be able to tell whether this skill has run. So stamp every file you rewrite.

```
python3 ~/.claude/skills/plain-register/stamp.py <path> --date YYYY-MM-DD
```

Pass today's date explicitly, because the script does not guess it.

Markdown gets a `plain_register:` line in frontmatter, which Dataview can query. Word and PowerPoint get a document property that readers never see. The script refuses to write a file that Office has open, which it detects from the `~$` lock file.

To read an existing stamp instead of writing one:

```
python3 ~/.claude/skills/plain-register/stamp.py --read <path>
```

A stamp records that the skill ran on that date. It does not prove the file still passes, because someone may have edited it afterwards. When that matters, run `plain-check` again.

## Related

- `plain-check`, the audit skill. Run it as the last step here, and on its own to check a document you did not just write.
- Drafted language is a starting point. The user will re-voice it into their own words, so flag analytical-sounding phrases and offer plainer alternatives.
