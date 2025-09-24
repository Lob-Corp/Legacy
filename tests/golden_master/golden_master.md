# Golden Master Testing

## Overview

This file documents all testing scenarios used to establish the golden master records for this project. The golden master testing approach captures the exact behavior of the legacy application to ensure that during the development and refactoring process, no existing functionality is broken or altered unintentionally.

### Purpose

Golden master testing works by:
1. **Recording** the current behavior of the legacy application through comprehensive test scenarios
2. **Storing** the exact output (HTML snapshots) as "golden master" records
3. **Comparing** new implementations against these recorded behaviors to detect any regressions

### Workflow

Each test scenario in this document:
- Navigates through specific user interactions in the web interface
- Captures the resulting HTML output after form submissions
- Saves these outputs as reference files for future comparison
- Ensures that any changes to the application behavior are intentional and properly reviewed

This systematic approach allows to refactor and modernize the codebase while maintaining behavioral compatibility with the original legacy application.

## Test Scenarios

### Add Family (`add_family`)

| Scenario Name | Purpose | Typical Inputs | Main Steps (Actions) | Key Checks / Expected Result |
|---------------|---------|----------------|----------------------|------------------------------|
| `scenario_add_family_one_parent` | Add a family with a single parent | Parent info (name, birth, occupation) | Fill parent fields, submit | Family created with one parent |
| `scenario_add_family_parent_already_exists` | Add a parent that already exists | Same parent info entered twice | Add parent, submit, try to add it again | No duplicate parent created |
| `scenario_add_family_two_parents` | Add a family with two parents | Two parents' info | Fill both parent fields, submit | Family created with two parents |
| `scenario_add_family_same_sex_parents` | Add two parents of the same sex | Two parents, same sex | Fill both parent fields, submit | Family accepted, no validation error |
| `scenario_add_family_dead_parents` | Add parents with death dates | Parents with birth and death dates | Fill birth/death fields, submit | Death info saved, family created |
| `scenario_add_family_link_parent` | Link to an existing parent | Select existing parent, new parent info | Select/link parent, fill other fields, submit | Parent linked, not duplicated |
| `scenario_add_family_marriage_event` | Add a marriage event to the family | Parents, marriage event (date, place, witnesses)| Fill parent/event fields, add witnesses, submit | Marriage event and witnesses saved |
| `scenario_add_family_custom_event` | Add a custom event to the family | Parents, custom event (name, date, place, notes)| Fill parent/event fields, submit | Custom event saved with family |
| `scenario_add_family_multiple_events` | Add multiple events to the family | Parents, several events | Fill parent fields, add multiple events, submit | All events saved with family |
| `scenario_add_family_comment` | Add a comment to the family | Parents, comment text | Fill parent fields, add comment, submit | Comment saved with family |
| `scenario_add_family_one_child` | Add a single child to the family | Parents, one child info | Fill parent/child fields, submit | Family created with one child |
| `scenario_add_family_link_child` | Link an existing child to a new family | Parents, select existing child | Add child, link to another family, submit | Child linked to new family |
| `scenario_add_family_multiple_children` | Add multiple children to the family | Parents, multiple children info | Fill parent/children fields, submit | All children saved with family |
| `scenario_add_family_sources` | Add sources to the family | Parents, source info | Fill parent fields, add source, submit | Source saved with family |
| `scenario_add_family_empty` | Submit the form with no data | None | Submit empty form | Error shown, no family created |

## Questions

This section summarizes all the questions that need to be answered in order to fully understand the application and its interface, so that testing can be as relevant and comprehensive as possible.

    - Why booleans on add widgets ?
    - Why is the checkbox after familly sources used for ?
    - Why events have different calendars and not birth/death date ?
    - Why there is a number field in witness info ?
    - Why month selection is textual at start but when changing the calendar type never falls back to textual ?
