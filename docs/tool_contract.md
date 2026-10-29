# Lookup Offering Tool Contract

## Purpose
Retrieve one offering from the local synthetic catalog using its ID.

## Tool Name
`lookup_offering`

## Input
- `offering_id`: required string.
- Allowed characters: uppercase letters, lowercase letters,
  digits, underscores, and hyphens.
- Length: 1 to 64 characters.
- Extra arguments are not allowed.

## Successful Lookup
Returns:
- `status`: "found"
- `offering`: the matching catalog record.

The record contains:
- id
- destination
- service_type
- duration_days
- status
- indicative_note

## Missing Offering
Returns:
- `status`: "not_found"
- `offering`: null

## Validation Errors
Reject missing arguments, invalid argument types, malformed IDs,
unexpected fields, and unapproved tool names.

The API returns HTTP 400 for tool-level validation errors.

## Security Boundaries
- Read only the fixed local data/catalog.json file.
- Never accept arbitrary filesystem paths from the model.
- Never fetch arbitrary URLs.
- Never execute shell commands.
- Never modify or delete catalog records.
- Never invent missing offering information.

## Limitations
The catalog contains synthetic demonstration records.
This tool does not verify actual prices or availability, make bookings,
contact customers, or authorize business commitments.


