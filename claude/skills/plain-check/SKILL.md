---
name: plain-check
description: Audit prose against the plain-register rules without rewriting it. Reports undefined specialist terms, metaphor-nouns standing in for real things, dangling references, missing verbs, overlong sentences, punctuation pivots, paraprosdokian shapes and self-narration tells. Use when the user says "plain check", "check the register", "did plain register run on this", "does this still hold up", "audit the language", or before circulating any document, deck or email. Also run automatically at the end of the plain-register skill. Args, an optional path to the file to check. With no args, check the material in the conversation.
---

# Plain check

Audits text against the rules in the `plain-register` skill. It reports. It does not rewrite.

Use it in two situations. The first is on a document you did not just write, to answer "does this still hold up." The second is at the end of a `plain-register` rewrite, as the last step before returning.

## Why this exists

It is hard to tell by eye whether the register has been applied, or whether something slipped through. A worked example shows why. This paragraph had been through `plain-register` and still read badly:

> The machinery behind it, from the arrangement agreement. Walking away had a price on both sides. The REIT would have paid a $42.1M termination fee, and the buyers a $47.7M reverse fee. [...] The ten-year envelope on the Capex tab is the public-data model of the same object.

It scores Flesch-Kincaid grade 7.7 and reading ease 61.3. That is better than the grade-10 target. Every readability formula passes it.

The formulas measure only two things, which are average sentence length and average syllables per word. This passage is not too wordy. It is too compressed. Eight separate failures live inside short sentences made of short words, so no formula can see any of them.

That is why the checks below are structural rather than statistical.

## Run the script first

```
python3 ~/.claude/skills/plain-check/check.py <path>
```

It reads .md, .txt, .docx and .pptx. Pass `--stdin` to check text from the conversation instead of a file. Pass `--verbose` to see every candidate instead of the first 40.

The script finds candidates. It does not judge them. Every list will contain false positives, which is intended, because a missed problem costs more than a candidate you dismiss in two seconds.

### It separates labels from prose

The register rules exempt headings, card titles, chart captions, table cells and footers, because those are labels rather than prose. So the script sorts every chunk of text into one of the two before it checks anything.

Sentence-level checks run on prose only. That covers sentence length, punctuation pivots, references, and missing verbs. Term checks run on everything, because a label can carry undefined jargon just as easily. The paraprosdokian check also runs on labels, because headlines and card titles are where that shape lives.

A chunk is treated as a label if it is a heading, a table cell, a title placeholder, a line of eight words or fewer with no closing punctuation, or a line in all capitals. Text that repeats on three or more slides is treated as a running footer and counted once.

This matters most on decks. Without the split, a 14-slide deck reports over a hundred false fragments, and the report becomes unusable.

### Two checks are deliberately tuned to under-report

The fragment check only fires when a sentence opens with a determiner or preposition and contains nothing that could be a verb. A real fragment that starts with a noun or a verb slips past. That is a deliberate trade, because no verb list can ever be complete, and a noisy report does not get read.

The elided-clause check uses a stricter test than the fragment check, so it does not accept a word ending in "s" as a verb. In a short trailing clause, an "s" word is far more likely to be a plural noun.

## Then judge each list

The script cannot tell a real problem from a false positive. Read the source text and decide.

**Acronyms, long words, terms of art, capitalised mid-sentence.** These four lists are one question asked four ways. For each item, is it defined where it first appears? An acronym must be expanded. A term of art built from ordinary words needs a definition, because its everyday meaning misleads. "Data room" and "cap rate" are made of common words and still need explaining. A name that is capitalised mid-sentence is usually a product, a tab or a defined term, so say what it is.

**Metaphor-noun candidates.** A metaphor used as a noun stands in for a real thing that never gets named. "The machinery behind it" names nothing. "The ten-year envelope" names nothing. Either name the real thing, or define the metaphor on first use. A metaphor is fine once the reader knows what it points at.

**Reference candidates.** Every "it", "this", "that" and "the same X" must point to something named in the same sentence or the one immediately before. If the referent sits two sentences back, the reader has to hold it in memory while reading, which is exactly the unpacking work the register exists to remove.

**Fragments.** A sentence with no verb. Labels are already excluded, so anything reaching this list is prose that lost its verb. Read the source, because an unusual verb can still slip through the detector.

**Clauses with an elided verb.** "The REIT would have paid a $42.1M fee, and the buyers a $47.7M fee" drops "would have paid" from the second half. The reader has to carry it forward. Write the verb out.

**Sentences over 25 words, colon or dash pivots, parallel-contrast pairs.** These are the checks the `plain-register` skill already listed. The script now finds them exactly rather than by eye.

**Paraprosdokian candidates.** A paraprosdokian is a setup followed by a twist ending that makes the reader go back and re-read the setup. "Four steps, and only one of them is yours." "Everything about billing changed. Your invoice didn't." The register bans them outright, with no exceptions, so every real one must be rewritten as plain statements. Say what the setup meant, then what the payoff meant, in separate sentences.

**Ownership idioms.** A possessive followed by an infinitive. "Is the firm's to hold", "is theirs to decide", "the call is yours to make." The sentence says a party owns the act but never says the party does it, so the reader has to work out who holds or decides. Rewrite to say who does what. Plain possessive nouns such as "the firm's fee" do not match, because no verb follows them.

The script finds two shapes. Shape A is one sentence, marked `A` in the list. It has a setup, then a comma with "and" or "yet", or "but", or a colon, semicolon or dash, then a short tail that opens on a limiter ("only", "just", "never", "none", "nothing", "nobody") or ends on a negation ("didn't", "is not"). Shape B is two sentences, marked `B` and shown as `first || second`. The second is short and ends on a bare auxiliary or a negation, so it reads as an elided contradiction. Items tagged `(label)` came from a heading, title or table cell.

Expect false positives. "And only if both halves are plain" fires shape A and is fine. "She said it would rain. It did." fires shape B and is a judgment call. Read each candidate and ask one question. Does the ending force a re-read of the beginning? If yes, it is banned. If the ending simply continues the thought, dismiss it.

**Self-narration candidates.** The text talking about itself or about its writer. The first family announces the register: "Here is the plain read", "put simply", "to be clear". The second family declares intent or restraint: "so I will stick to what it means", "I won't speculate", "we'll keep this brief". Both are banned, because the announcement adds nothing and declared restraint implies the unwanted thing was on the table. The fix is to delete the announcement and keep the content. A scope limit the reader actually needs survives as a fact about the material ("The card carries the full numbers. This section explains what they mean."). Two false-positive classes to dismiss by hand: quoted speech that happens to contain a tell, and a real commitment by a team ("We will stick to the schedule"), which is a claim about future behavior rather than narration.

## The readability scores are a floor, not a pass

The script prints Flesch-Kincaid grade and Flesch reading ease. Both are computed from the same two inputs, so they always agree. They are one measurement shown twice, not two findings.

Use them one way only. A grade above 12 means the text definitely needs work. A good score means nothing at all.

Never report a good score as evidence that a document passed. It is not evidence. The demonstration rewrite of the passage above fixed all eight failures and moved the grade by 0.8, which is inside the noise from rewording one sentence.

## What to return

A short verdict, then the findings. Group findings by the section they came from. For each one, quote the phrase and say what to do.

If nothing survives judgment, say so plainly and say which checks ran. Do not pad it.

If the text is stamped (see below), say when it was stamped and whether it still passes. A document can be stamped and still drift, because someone edited it afterwards.

## Related

- `plain-register`, the rewrite skill. This check is its last step.
