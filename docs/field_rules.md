# Travel Inquiry Extractor — Field Rules

## General Principles

- Extract only information supported by the client's message.
- Use `None` when a field cannot be determined.
- Never invent missing information or silently choose between conflicting values.
- Set `needs_review=True` when information is contradictory, invalid, ambiguous, or requires clarification under the rules below.
- Missing optional information alone does not require review.
- Preserve valid extracted fields even when another field needs review.

## Decision Table

| Field | Provided | Absent | Contradictory | Invalid or unusable |
|---|---|---|---|---|
| `travelers` | Extract a clear positive integer. | `None`; no review by itself. | `None`; set `needs_review=True`. | `None`; set `needs_review=True`. |
| `dates` | Extract an exact, unambiguous date. | `None`; no review by itself. | `None`; set `needs_review=True`. | `None`; set `needs_review=True` for vague, incomplete, or invalid dates. |
| `location` | Extract a clearly stated destination. | `None`; no review by itself. | `None`; set `needs_review=True`. | `None`; set `needs_review=True` if clarification is needed. |
| `origin_country` | Extract the explicitly stated departure country, not passport nationality. | `None`; no review by itself. | `None`; set `needs_review=True`. | `None`; set `needs_review=True` if the departure country is unusable or unclear. |
| `duration` | Extract a clear positive duration in days. | `None`; no review by itself. | `None`; set `needs_review=True`. | `None`; set `needs_review=True` for zero, negative, or vague durations. |
| `price` | Extract a clear numeric budget or price. | `None`; no review by itself. | `None`; set `needs_review=True`. | `None`; set `needs_review=True` if the amount is unclear or unusable. |
| `contact_details` | Extract clearly provided contact information. | `None`; no review by itself. | `None`; set `needs_review=True`. | `None`; set `needs_review=True` if malformed or unusable. |

## 1. Travelers

- **Provided:** Extract a clear positive integer.
- **Absent:** Set `travelers=None`. Do not guess the number.
- **Contradictory:** If traveler counts conflict and cannot be resolved, set `travelers=None` and `needs_review=True`.
- **Invalid:** If the stated count is zero, negative, or otherwise invalid, set `travelers=None` and `needs_review=True`.

## 2. Dates

- **Provided:** Extract an exact, unambiguous date.
- **Absent:** Set `dates=None`. If no other issue requires review, keep `needs_review=False`.
- **Vague or incomplete:** If only a month, season, or vague time period is provided and an exact travel date is required, set `dates=None` and `needs_review=True`.
- **Contradictory:** If conflicting dates cannot be resolved, set `dates=None` and `needs_review=True`.
- **Invalid:** If the stated date is invalid or unusable, set `dates=None` and `needs_review=True`.
- Never invent a day for a month-only date.

## 3. Destination (`location`)

- **Provided:** Extract the clearly stated destination.
- **Absent:** Set `location=None`.
- **Contradictory:** If multiple conflicting destinations cannot be resolved, set `location=None` and `needs_review=True`.
- **Invalid or unclear:** Set `location=None` and `needs_review=True` if clarification is necessary.

## 4. Origin Country

- **Provided:** Extract the explicitly stated departure country.
- **Absent:** Set `origin_country=None`.
- **Nationality only:** If the client states a passport nationality but not the departure country, set `origin_country=None`. Do not assume nationality identifies the departure country.
- **Contradictory:** If the departure country is unclear because of conflicting information, set `origin_country=None` and `needs_review=True`.

## 5. Duration

- **Provided:** Extract a clear positive trip duration in days.
- **Absent:** Set `duration=None`.
- **Contradictory:** If conflicting durations cannot be resolved, set `duration=None` and `needs_review=True`.
- **Invalid or vague:** If the duration is zero, negative, or too vague to determine, set `duration=None` and `needs_review=True`.

## 6. Price

- **Provided:** Extract a clearly stated numeric budget or price.
- **Absent:** Set `price=None`.
- **Contradictory:** If conflicting prices cannot be resolved, set `price=None` and `needs_review=True`.
- **Invalid or unclear:** Set `price=None` and `needs_review=True` if the amount is unusable.
- Preserve the numeric amount. For example, `$2,000` becomes `2000.0`. Do not confuse the amount with a travel date or duration.

## 7. Contact Details

- **Provided:** Extract clearly provided contact information.
- **Absent:** Set `contact_details=None`.
- **Contradictory:** If contact information conflicts and cannot be resolved, set `contact_details=None` and `needs_review=True`.
- **Invalid:** If contact information is malformed or unusable, set `contact_details=None` and `needs_review=True`.

## 8. Review Flag

- Set `needs_review=True` when any field has unresolved contradictory, invalid, or clarification-required information.
- Set `needs_review=False` when the available information is clear and no review-worthy issue exists.
- Missing optional fields alone do not require review.
- Treat an inquiry as materially incomplete and set `needs_review=True` when a missing fact prevents the business from replying confidently or taking the next appropriate action.
- If multiple fields are affected, preserve every valid field and flag the overall lead for review.
