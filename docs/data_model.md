# Clarivo data model

## Core relationship

```text
User
└── PracticeSession
    ├── Exercise
    ├── Prompt
    ├── Attempt 1
    │   ├── Audio reference
    │   ├── Transcript
    │   ├── Analysis
    │   └── Feedback
    └── Attempt 2
        ├── Audio reference
        ├── Transcript
        ├── Analysis
        └── Feedback
```

Retries belong to the same practice session so attempts can be compared.

## Initial entities

### User

Identity and profile of a learner. Authentication can follow the first vertical
slice.

### Exercise

Reusable practice format containing type, difficulty, preparation duration, and
speaking duration.

### Prompt

Question or speaking task associated with an exercise. Target skills are stored
as structured metadata.

### PracticeSession

One user's practice of one prompt. A session owns one or more attempts.

### Attempt

One recording within a session. Audio is stored in object storage; the database
stores its URL, duration, and MIME type.

### Transcript

ASR output for an attempt, including raw and normalized text, segments, words,
provider metadata, and processing time. Raw disfluencies must be preserved.

### Analysis

Versioned delivery and content metrics for an attempt. Versioning makes old
results traceable as analyzers evolve.

### Feedback

Versioned coaching generated from an analysis. It is separate because detected
signals and the advice selected for a user are different concerns.

## First database increment

The first model implementation should introduce only `Exercise` and `Prompt`.
`PracticeSession` and `Attempt` follow in the next increment.
