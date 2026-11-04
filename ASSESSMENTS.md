# Knowledge Checks

Each section has a `quiz.yaml` question bank, and each of the six newest modules has a module bank (10 questions), and each of the six newest modules has a module bank (10 questions), listed in `astrona.yaml` as a `type: quiz` entry with `pass_score: 70` after the section capstone. A final domain quiz, `sections/final-domain-quiz.yaml`, closes the course. The banks use `schema_version: 1` and `kind: question_bank`, with single-choice questions, one correct option, per-option feedback, a measurable learning objective and the reading path in `source_readings` for author traceability. All banks have `status: draft`.

The banks contain answer keys and are public learning material, so they are not a secure examination bank. Do not treat scores as an official CAPA result.

| Bank | Path | Questions |
| --- | --- | --- |
| ats062-010 | sections/section-010/quiz.yaml | 18 |
| ats062-020 | sections/section-020/quiz.yaml | 18 |
| ats062-030 | sections/section-030/quiz.yaml | 17 |
| ats062-010-m03 | sections/section-010/module-03/quiz.yaml | 10 |
| ats062-010-m04 | sections/section-010/module-04/quiz.yaml | 10 |
| ats062-010-m05 | sections/section-010/module-05/quiz.yaml | 10 |
| ats062-020-m03 | sections/section-020/module-03/quiz.yaml | 10 |
| ats062-030-m03 | sections/section-030/module-03/quiz.yaml | 10 |
| ats062-030-m04 | sections/section-030/module-04/quiz.yaml | 10 |
| ats062-final | sections/final-domain-quiz.yaml | 42 |

The final bank reuses 12 older and 18 newer questions from the section banks, and 12 questions from the module banks, under new IDs.
