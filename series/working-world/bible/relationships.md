# Relationships

This file tracks **relationship state and relationship change**.

A character file records what an individual thinks.

This file records the canonical history between people.

Relationships are directional.

Character A's feelings about Character B may be completely different from Character B's feelings about Character A.

---

## Relationship ID format

Recommended:

```text
REL-character-a--character-b
```

Example:

```text
REL-mara-vale--tomas-enn
```

The ordering is only for identification.

---

## Relationship entry

```markdown
## Character A ↔ Character B

### Metadata
- Relationship ID:
- Characters:
- First shared appearance:
- Current status:

### Objective connection
How do they actually know one another?

### A's view of B

### B's view of A

### What A knows about B

### What B knows about A

### What A misunderstands about B

### What B misunderstands about A

### Power balance
Money, status, age, law, employment, magic, emotional dependence, reputation, etc.

### History

### Current tensions

### Affection / loyalty

### Boundaries

### Secrets between them

### Important changes

| Story / date | Event | State before | State after |
| --- | --- | --- | --- |
| TBD | TBD | TBD | TBD |

### Current relationship state

### Possible future direction
Planning only; not canon until written.
```

---

## Relationship types to track

Do not track only romance.

Useful relationship categories:

- family;
- friendship;
- former friendship;
- romantic;
- sexual;
- ex-partners;
- professional;
- employer/employee;
- client/provider;
- neighbours;
- rivals;
- political;
- religious;
- mentor/student;
- debt;
- criminal;
- adversarial;
- one-sided admiration;
- reputation only;
- indirect connection.

---

## Network rules

### Direct acquaintance

Both characters have met.

### One-way recognition

A knows who B is.

B does not know A.

### Reputation link

A knows stories about B but has never met B.

### Indirect link

A knows C, who knows B.

Do **not** treat this as A knowing B.

### Institutional link

Both interact with the same organisation without knowing one another.

### Event link

Both were affected by the same event.

They may never meet.

This distinction is essential for maintaining the "six degrees" structure.

---

## Connection matrix

Use this table for quick reference.

| Character A | Character B | Connection | Have met? | Strength | Last changed |
| --- | --- | --- | ---: | --- | --- |
| TBD | TBD | friend / sibling / indirect / reputation / etc. | yes/no | weak / moderate / strong | Story X |

---

## Example only — relationship

> **NON-CANONICAL EXAMPLE.**

## Mara Vale ↔ Len Corra

### Objective connection

Mara buys breakfast at Len's bakery several mornings each week.

They have known one another casually for approximately three years.

They have never socialised privately.

### Mara's view of Len

Reliable.

Nosy.

Better informed about the neighbourhood than he pretends to be.

She likes him but would not describe him as a friend.

### Len's view of Mara

Competent municipal worker.

Too serious.

Someone he trusts not to ignore a genuinely dangerous building problem.

### What Mara knows about Len

- owns the bakery;
- has an adult daughter;
- hates the city licensing office.

### What Len knows about Mara

- works in Civic Works;
- has a younger brother;
- usually pays in exact coin.

### What neither knows

Len's daughter works with a courier who will become important to another story.

This does not make Mara and that courier acquaintances.

### Current relationship state

Familiar local acquaintances with low emotional intimacy and moderate practical trust.

### Important changes

| Story / date | Event | State before | State after |
| --- | --- | --- | --- |
| Story 1 | Len lies to an inspector to give Mara time | ordinary familiarity | Mara now owes him a small personal favour |

---

## Example only — indirect six-degrees chain

```text
Mara Vale
  -> regularly buys from Len Corra
Len Corra
  -> father of Sera Corra
Sera Corra
  -> works with Tomas Enn
Tomas Enn
  -> delivers sealed documents for the Registry
Registry
  -> investigates forged permits used by Ilyan Ves
Ilyan Ves
  -> has never met Mara
```

Mara and Ilyan are connected.

They do not know one another.

Neither needs to discover the chain.
