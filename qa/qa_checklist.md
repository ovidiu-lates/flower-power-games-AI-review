# QA Checklist

## Scope

Validate that review text can be analysed consistently for sentiment, perceived difficulty, themes/aspects, and complaints. The validation cases are stored in `qa/validation_reviews.json`.

## Test data coverage

- [ ] Positive review: VR-001, VR-002, or VR-006
- [ ] Neutral review: VR-003
- [ ] Negative review: VR-004, VR-008, or VR-010
- [ ] Easy review: VR-001, VR-003, or VR-009
- [ ] Hard review: VR-005 or VR-006
- [ ] Theme/aspect extraction: VR-007 or VR-008
- [ ] Complaint extraction: VR-004, VR-008, or VR-012
- [ ] Negation handling: VR-009
- [ ] Ambiguous outcome: VR-011
- [ ] Mixed outcome: VR-005 or VR-012

## Environment and smoke checks

- [ ] `.env` exists locally and is not committed.
- [ ] SQL Server container is running on `localhost,1434`.
- [ ] Database `FlowerPowerGames` exists.
- [ ] Latest Alembic migrations are applied with `uv run alembic upgrade head`.
- [ ] `uv run pytest` completes without failures.
- [ ] `uv run ruff check .` completes without errors.
- [ ] FastAPI starts with `uv run uvicorn smart_review_ai.main:app --reload --app-dir src`.
- [ ] `GET /health` returns HTTP 200 and `{"status":"ok"}`.
- [ ] `/docs` loads successfully.

## Validation procedure

For every case in `qa/validation_reviews.json`:

1. Submit the `review_text` through the analysis function or API endpoint.
2. Record the actual sentiment, difficulty, themes, and complaints.
3. Compare the result with `expected_outcome`.
4. Mark the case **Pass** only when the main labels are correct and no important complaint or theme is missed.
5. Record deviations, timestamps, and the application version or Git commit.

## Expected-result rules

- [ ] Sentiment reflects the overall review, not one isolated positive or negative phrase.
- [ ] Negations are respected; for example, “not difficult” should not be classified as hard.
- [ ] Difficulty is based on learning/strategic complexity, not whether the reviewer liked the game.
- [ ] Themes are concise concepts supported by the review text.
- [ ] Complaints contain only actual problems or criticisms.
- [ ] Empty complaint lists are returned when no complaint is present.
- [ ] Mixed or ambiguous language is not forced into an unjustifiably strong label.
- [ ] The response remains valid when the review contains multiple aspects.

## Edge and error cases

- [ ] Empty review text is rejected clearly or returns a documented validation response.
- [ ] Whitespace-only text is handled consistently.
- [ ] Very short text does not cause an unhandled exception.
- [ ] Long text does not cause an unhandled exception.
- [ ] Special characters and punctuation are accepted.
- [ ] Duplicate submissions produce consistent results where deterministic output is expected.
- [ ] Database/API failures return a useful error without exposing credentials.

## Results

| Case | Actual result | Pass/Fail | Notes |
|---|---|---|---|
| VR-001 |  |  |  |
| VR-002 |  |  |  |
| VR-003 |  |  |  |
| VR-004 |  |  |  |
| VR-005 |  |  |  |
| VR-006 |  |  |  |
| VR-007 |  |  |  |
| VR-008 |  |  |  |
| VR-009 |  |  |  |
| VR-010 |  |  |  |
| VR-011 |  |  |  |
| VR-012 |  |  |  |

## Exit criteria

- [ ] All 12 validation cases have recorded actual results.
- [ ] No critical or high-severity defects remain open.
- [ ] At least one case from every required acceptance category passes.
- [ ] Any expected-vs-actual differences are documented and agreed with the team.
