# Travel Lead Extraction Requirements

## User / Client

The client is an automated workflow, such as an n8n Telegram bot, that
forwards a traveler's free-form message to this API. The API is an extraction
service for downstream travel-agent workflows; it is not the travel agent and
does not communicate directly with travelers.

## Input

The client sends raw text using the `ExtractRequest` schema:

```json
{
  "text": "Planning a trip for two travelers from Canada to Portugal in June."
}
```

The `text` value must contain between 10 and 1,000 characters.

## Extracted Fields

Each extracted lead contains the following nullable fields:

- `travelers`: Positive integer number of travelers.
- `dates`: A precise date when one can be established reliably; otherwise
  `null`.
- `location`: Destination or travel location.
- `duration`: Positive integer duration, such as a number of days.
- `origin_country`: Traveler's country of origin.
- `price`: Positive numeric price when explicitly provided.
- `needs_review`: Boolean indicating whether human review is needed.

Missing information must be represented as `null`. The system must not replace
missing values with plausible guesses or defaults.

## Non-goals and Boundaries

This system will not:

- Book flights, hotels, tours, or other travel services.
- Process credit cards, payments, refunds, or financial transactions.
- Contact airlines, hotels, travel agencies, or other suppliers.
- Guarantee availability, pricing, visas, or travel eligibility.
- Infer personal information that was not present in the input.
- Convert an extraction into a confirmed itinerary or reservation.

## Constraints

- Reject empty text and text longer than 1,000 characters.
- Reject text shorter than 10 characters.
- Preserve missing fields as `null`; do not invent plausible values.
- Never infer a precise date from month-only text. For example, `June` must
  not become an arbitrary day in June.
- Only populate constrained numeric fields when the value is explicitly
  supported and greater than zero.
- Return structured validation errors using the standard FastAPI/Pydantic error
  shape.

## Acceptance Gate

This feature is production-ready only when all of the following are true:

- Valid raw text produces an `ExtractionResponse` with the documented fields.
- Missing values are returned as `null`, not guessed or defaulted.
- Empty, too-short, and overlong input is rejected with a validation error.
- Invalid constrained values, such as zero or negative travelers, duration, or
  price, are rejected with a validation error.
- Month-only dates remain unresolved rather than being converted to a precise
  date.
- The response and error shapes are documented and covered by automated tests.
- The focused test suite, type checks, and lint checks pass with no unresolved
  errors.