# Characters

Use **one Markdown file per significant character**.

This directory is the canonical character bible.

A character file should contain enough information that a different writer or LLM can write the character months later without:
- changing their basic appearance;
- flattening their personality;
- inventing contradictory history;
- forgetting relationships;
- resetting emotional development;
- making everyone speak in the same voice.

Do not over-document irrelevant trivia.

Record details when they:
- affect behaviour;
- affect continuity;
- distinguish the character;
- matter to relationships;
- are likely to reappear.

---

## Character categories

Every named character can optionally be assigned a structural category.

### Anchor

Appears across a substantial portion of the book or series.

May lead more than one story.

### Recurring

Appears in multiple stories and has an ongoing life.

### Bridge

Connects otherwise separate character networks.

### Story-local

Important inside one story but not expected to recur.

### Background continuity

A small recurring figure used to make locations or institutions feel persistent.

A category can change later.

A Story-local character may unexpectedly become useful enough to promote to Recurring.

---

## Naming files

Recommended:

```text
first-last.md
```

Examples:

```text
mara-vale.md
tomas-enn.md
sister-avel.md
```

For people without conventional names:

```text
the-ash-prince.md
old-nara.md
captain-ivo.md
```

---

## Recommended character file

```markdown
# Full name

## Metadata
- Character ID:
- Status: alive / dead / missing / unknown
- Narrative role: anchor / recurring / bridge / story-local / background
- First appearance:
- Latest appearance:
- POV character: yes / no
- Home:
- Occupation:
- Affiliations:

## Identity
- Full name:
- Known as:
- Age at first appearance:
- Birth date / year if known:
- Gender:
- Pronouns:
- Species / ancestry if relevant:
- Culture / nationality:
- Social class / status:
- Religion / worldview if relevant:

## Appearance

### Stable traits
- Height/build:
- Hair:
- Eyes:
- Skin:
- Distinguishing features:
- Voice:
- Typical clothing:
- Scars/tattoos/marks:

### Changeable traits
- Current injuries:
- Current hairstyle:
- Current clothing changes:
- Magical alterations:
- Other temporary details:

## First impression

What does a stranger notice first?

## Personality

### Core traits
Use a small number of specific traits with evidence.

### Contradictions
What apparently incompatible qualities coexist?

### Strengths

### Weaknesses

### Habits

### Values

### Prejudices / blind spots

### Fears

### Desires

### Boundaries
What will they refuse to do?

### Under pressure
How do they behave when:
- frightened;
- angry;
- ashamed;
- attracted to someone;
- exhausted;
- given power;
- losing control?

## Voice / speech

### General cadence

### Vocabulary

### Formality

### Humour

### Swearing

### Verbal habits

### What they do not say

### Dialogue examples
Include 3-6 short representative lines.

## Skills and limitations

### Skilled at

### Adequate at

### Bad at

### Magical abilities

### Magical limitations

### Physical limitations

### Knowledge limitations

Do not let a character know facts they have never learned.

## History

### Childhood / family

### Education / training

### Important relationships

### Previous work

### Major events

### Secrets

Separate:
- secrets the character keeps;
- facts the character does not know;
- facts the reader does not yet know.

## Relationships

Use relationship IDs or exact character filenames where possible.

| Character | Relationship | Their view of this character | This character's view of them | Current state |
|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD |

## Social network

### People they know directly

### People they know by reputation

### Organisations they interact with

### People who know of them but whom they do not know

This section is useful for maintaining six-degrees-style connections.

## Current state

Update after every appearance.

- Current date:
- Current location:
- Employment:
- Financial state:
- Physical state:
- Emotional state:
- Relationship changes:
- Current goal:
- Current problem:
- What they know now that they did not know before:
- Outstanding obligations:
- Objects currently carried / owned that matter:

## Story participation

| Story | Role | Starting state | Key action | Ending state |
|---|---|---|---|---|
| Story 1 | POV / support / etc. | TBD | TBD | TBD |

## Arc

### Book-level starting state

### Important turning points

### Current trajectory

### Possible future direction
This is planning, not canon until written.

## Canonical details that must not drift

- TBD

## Flexible details

Details an author may choose or change without contradicting canon.

- TBD

## Forbidden assumptions

List things a model must **not** infer.

Examples:
- Do not assume they are wealthy because they have a prestigious job.
- Do not assume they are romantically interested in their closest friend.
- Do not assume they know Character X merely because both know Character Y.
- Do not assume their cultural background determines their political views.

## Open questions

- TBD
```

---

# How much detail is enough?

The goal is behavioural consistency, not bureaucracy.

A main POV character may need several pages.

A recurring shopkeeper may need:

```markdown
# Len Corra

- Narrative role: background continuity
- Owns the South Gate bakery.
- Mid-50s at first appearance.
- Missing the final joint of his left little finger.
- Dry, impatient humour.
- Remembers customers' orders but frequently forgets their names.
- Knows Mara because she buys breakfast there.
- Knows Tomas only as "the courier who blocks the doorway".
- Does NOT know Mara and Tomas know one another.
- First appears: Story 1.
```

That is enough if nothing else matters.

---

# Example only — fully developed character fragment

> **NON-CANONICAL EXAMPLE.**
> This demonstrates useful depth. It should not be imported into the actual world unless explicitly adopted.

```markdown
# Mara Vale

## Metadata
- Character ID: CH-MARA-001
- Status: alive
- Narrative role: anchor
- First appearance: Story 1
- Latest appearance: Story 1
- POV character: yes
- Home: East Ward, capital city
- Occupation: municipal ward inspector
- Affiliations: Civic Works Office

## Identity
- Age at first appearance: 29
- Pronouns: she/her
- Social status: skilled municipal worker; respectable employment, little savings

## Appearance
- Compact build.
- Dark hair usually cut herself and never quite even.
- Left eyebrow has a thin white scar.
- Uniform is well maintained but older than most colleagues' uniforms.
- Carries chalk, measuring cord, seals and inspection tags in a battered leather case.

## First impression
Efficient, mildly irritated, difficult to impress.

## Personality

### Core traits
- observant;
- practical;
- private;
- morally serious without wanting to appear idealistic.

### Contradictions
- dislikes bureaucracy but believes public systems matter;
- claims not to care what people think but hates being considered unreliable;
- generous with labour, guarded with money.

### Under pressure
- fear makes her more precise, not louder;
- anger makes her formal;
- shame makes her avoid the person involved;
- attraction produces excessive practical helpfulness.

## Voice / speech
- Short sentences.
- Rarely uses elaborate metaphors.
- Asks specific questions.
- Swears only after the situation is already very bad.
- When angry, uses a person's full name.

### Example lines
- "That isn't repaired. It's been painted."
- "You can dislike the rule after you stop the roof falling on them."
- "No. Explain the part you skipped."
- "If this works, I was never here."

## Skills and limitations
- Excellent at identifying structural ward failures.
- Competent with basic repair magic.
- Poor horse rider.
- Can read technical Old Imperial inscriptions but cannot speak the language.
- Knows municipal regulations extremely well.
- Does not understand aristocratic etiquette.

## Current state
- Location: East Ward.
- Financial state: two months of expenses saved.
- Current goal: licence renewal.
- Outstanding obligation: younger brother's training fees.
- New secret: falsified one inspection record.

## Canonical details that must not drift
- Scar is on LEFT eyebrow.
- She has one younger brother.
- She does not own a horse.
- She is not a combat mage.
- At the end of Story 1, she has falsified exactly one official inspection record.
```

---

# Character writing rules

When generating prose:

1. Read the POV character's full file.
2. Read files for characters physically present in the scene.
3. Read relevant relationship entries.
4. Read the latest timeline state.
5. Never give a character knowledge merely because the reader knows it.
6. Never restore an old relationship state because an earlier story described it.
7. Distinguish private thought from objective canon.
8. Allow characters to be mistaken.
9. Avoid reducing a character to their trauma, sexuality, occupation, species, magic, or one personality trait.
10. Update `Current state` after every meaningful appearance.
