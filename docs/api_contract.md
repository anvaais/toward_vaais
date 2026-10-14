# API Contract

## ExtractRequest

The extraction endpoint accepts raw travel-planning text. The request body
contains one required `text` field. The text must be between 10 and 1,000
characters.

### 1. Fully detailed lead

```json
{
  "text": "We are 2 travelers from Canada looking for a 10-day trip to Portugal from 2027-06-05 to 2027-06-14. Our budget is 3500 USD and we would like help planning hotels and activities."
}
```

### 2. Lead with several missing fields

```json
{
  "text": "Please find a trip to Kyoto for one person. I have not decided on the dates, duration, or budget yet."
}
```

The missing dates, duration, origin country, and price must remain `null`
rather than being replaced with guessed values.

### 3. Month-only date

```json
{
  "text": "A family of four would like to visit Greece in September. We are flexible about the exact dates and would like suggestions for a two-week holiday."
}
```

The month must not be converted into an arbitrary precise date. The extracted
`dates` value must remain `null` unless the client supplies a specific date.

### 4. Nationality versus origin country

```json
{
  "text": "I am a British national currently living in Singapore and planning a trip for two people to Japan. We would depart from Singapore in 2027-04-12."
}
```

Nationality and origin country are different concepts. The extraction must
use the traveler's departure or residence context for `origin_country` when
that is what the text provides; it must not automatically convert a
nationality into an origin country.

### 5. Specific budget and duration

```json
{
  "text": "Three travelers want a 7-day trip to Iceland starting on 2027-02-18, with a maximum budget of 4800 EUR for the whole trip."
}
```

The explicit duration and budget should be extracted as positive values. No
additional values should be inferred when the request does not provide them.
