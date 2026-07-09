# Package 3.1.0 - Account Management

## Purpose

Begin the first true administration subsystem for ACE Management Dashboard by turning account discovery into a read-only Account Management module.

## Scope

- Account list
- Search
- Sorting
- Filtering
- Pagination
- Account summary metrics
- Linked character navigation through existing detail routes
- Read-only safety preservation

## Non-scope

- Account create/edit/delete
- Ban/unban actions
- Password reset actions
- SQL migrations
- Character semantic decoding, which belongs to Phase 3.2

## Notes

The ACE database exposes many values as raw schema fields. This package intentionally avoids building a guessed semantic property dictionary into account pages. Future phases should add a centralized dictionary and decoder service before showing friendly character attributes such as race, sex, title, heritage, vitae, skills, and inventory.
