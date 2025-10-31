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

### How to run

Use `python record.py` to launch the recording on the legacy project.

## Test Scenarios

### Add Family (`add_family`)

| Scenario Name | Purpose | Typical Inputs | Main Steps (Actions) | Key Checks / Expected Result | Implemented |
|---------------|---------|----------------|----------------------|------------------------------|-------------|
| `scenario_add_family_one_parent` | Add a family with a single parent | Parent info (name, birth, occupation) | Fill parent fields, submit | Family created with one parent | ✅ |
| `scenario_add_family_parent_already_exists` | Add a parent that already exists | Same parent info entered twice | Add parent, submit, try to add it again | No duplicate parent created | ✅ |
| `scenario_add_family_two_parents` | Add a family with two parents | Two parents' info | Fill both parent fields, submit | Family created with two parents | ✅ |
| `scenario_add_family_same_sex_parents` | Add two parents of the same sex | Two parents, same sex | Fill both parent fields, submit | Family accepted, no validation error | ✅ |
| `scenario_add_family_dead_parents` | Add parents with death dates | Parents with birth and death dates | Fill birth/death fields, submit | Death info saved, family created | ✅ |
| `scenario_add_family_link_parent` | Link to an existing parent | Select existing parent, new parent info | Select/link parent, fill other fields, submit | Parent linked, not duplicated | ✅ |
| `scenario_add_family_marriage_event` | Add a marriage event to the family | Parents, marriage event (date, place, witnesses)| Fill parent/event fields, add witnesses, submit | Marriage event and witnesses saved | ✅ |
| `scenario_add_family_custom_event` | Add a custom event to the family | Parents, custom event (name, date, place, notes)| Fill parent/event fields, submit | Custom event saved with family | ✅ |
| `scenario_add_family_multiple_events` | Add multiple events to the family | Parents, several events | Fill parent fields, add multiple events, submit | All events saved with family | ✅ |
| `scenario_add_family_comment` | Add a comment to the family | Parents, comment text | Fill parent fields, add comment, submit | Comment saved with family | ✅ |
| `scenario_add_family_one_child` | Add a single child to the family | Parents, one child info | Fill parent/child fields, submit | Family created with one child | ✅ |
| `scenario_add_family_link_child` | Link an existing child to a new family | Parents, select existing child | Add child, link to another family, submit | Child linked to new family | ✅ |
| `scenario_add_family_multiple_children` | Add multiple children to the family | Parents, multiple children info | Fill parent/children fields, submit | All children saved with family | ✅ |
| `scenario_add_family_sources` | Add sources to the family | Parents, source info | Fill parent fields, add source, submit | Source saved with family | ✅ |
| `scenario_add_family_empty` | Submit the form with no data | None | Submit empty form | Error shown, no family created | ✅ |

### Details (`details`)

| Scenario Name | Purpose | Typical Inputs | Main Steps (Actions) | Key Checks / Expected Result | Implemented |
|---------------|---------|----------------|----------------------|------------------------------|-------------|
| `scenario_details_by_id` | View person details by ID | person id (i) | GET /gwd/<base>/details?i=<id> | Full person page rendered with family, events, sources and timeline | ❌ |
| `scenario_details_by_name` | View person details by name | p (first name), n (surname) | GET /gwd/<base>/details?p=John&n=Doe | Person found by name and details shown; 404 page if not found | ❌ |
| `scenario_details_missing_params` | Missing id and name | none | GET /gwd/<base>/details | Bad request page rendered | ❌ |

### Modify Individual (`modify_individual` / `MOD_IND`)

| Scenario Name | Purpose | Typical Inputs | Main Steps (Actions) | Key Checks / Expected Result | Implemented |
|---------------|---------|----------------|----------------------|------------------------------|-------------|
| `scenario_mod_ind_get` | Load edit form for an individual | base, id, lang | GET /gwd/<base>/modify_individual?id=<id>&lang=en | Returns edit form populated with person data and digest | ❌ |
| `scenario_mod_ind_post_update` | Submit edits to update person | form fields (first_name, surname, dates, events...) | POST form to same endpoint | DB updated, redirect to detail or JSON ok when requested | ❌ |
| `scenario_mod_ind_post_delete` | Delete a person via form | delete flag or action=delete | POST with delete in form | Person removed; JSON or plain confirmation returned | ❌ |

### Search (`search`)

| Scenario Name | Purpose | Typical Inputs | Main Steps (Actions) | Key Checks / Expected Result | Implemented |
|---------------|---------|----------------|----------------------|------------------------------|-------------|
| `scenario_search_surname` | List persons by surname | surname parameter | GET /gwd/<base>/search?surname=Smith | Renders surname listing (search_surname) with persons and counts | ❌ |
| `scenario_search_firstname` | List persons by first name | firstname parameter | GET /gwd/<base>/search?firstname=John | Renders firstname listing (search_firstname) | ❌ |
| `scenario_search_alpha` | Alphabetical listing | sort=alpha&on=surname | GET /gwd/<base>/search?sort=alpha&on=surname | Returns grouped alpha page with letters and person lists | ❌ |

### Homepage (`gwd/<base>`)

| Scenario Name | Purpose | Typical Inputs | Main Steps (Actions) | Key Checks / Expected Result | Implemented |
|---------------|---------|----------------|----------------------|------------------------------|-------------|
| `scenario_homepage_basic` | Render base homepage | base, optional lang | GET /gwd/<base>?lang=en | Renders `gwd/homepage.html` with total_persons count | ❌ |

### Images (`/images/<path>`)

| Scenario Name | Purpose | Typical Inputs | Main Steps (Actions) | Key Checks / Expected Result | Implemented |
|---------------|---------|----------------|----------------------|------------------------------|-------------|
| `scenario_images_serve_ok` | Serve existing image file | filename path | GET /images/person/123.png | File served with cache headers (max_age=3600) | ❌ |
| `scenario_images_bad_path` | Reject invalid path | absolute or ../ in path | GET /images/../etc/passwd | 400 returned (bad request) | ❌ |
| `scenario_images_not_found` | Missing file | unknown filename | GET /images/missing.png | 404 returned | ❌ |

### Titles (`titles`)

| Scenario Name | Purpose | Typical Inputs | Main Steps (Actions) | Key Checks / Expected Result | Implemented |
|---------------|---------|----------------|----------------------|------------------------------|-------------|
| `scenario_titles_search` | Search titles or fiefs | title or fief param | GET /gwd/<base>/titles?title=Lord | If single match, redirect/render title_detail with persons holding title | ❌ |
| `scenario_titles_list` | List all titles | none | GET /gwd/<base>/titles | Render `titles_all.html` grouped by initial | ❌ |

### Fiefs (`fiefs`)

| Scenario Name | Purpose | Typical Inputs | Main Steps (Actions) | Key Checks / Expected Result | Implemented |
|---------------|---------|----------------|----------------------|------------------------------|-------------|
| `scenario_fiefs_list` | List fiefs/titles with counts | none | GET /gwd/<base>/fiefs | Render `fiefs_all.html` with titles and counts | ❌ |

### GWSetup (`/gwsetup/*`)

| Scenario Name | Purpose | Typical Inputs | Main Steps (Actions) | Key Checks / Expected Result | Implemented |
|---------------|---------|----------------|----------------------|------------------------------|-------------|
| `scenario_gwsetup_welcome` | Render setup welcome page | lang | GET /gwsetup/welcome/en | Template `welcome.htm` rendered via TemplateService | ❌ |
| `scenario_gwsetup_generic` | Render other setup pages | path and lang | GET /gwsetup/<page>/<lang> | Corresponding template returned or NotImplemented for some endpoints | ❌ |

### GWD Root (`/gwd` root)

| Scenario Name | Purpose | Typical Inputs | Main Steps (Actions) | Key Checks / Expected Result | Implemented |
|---------------|---------|----------------|----------------------|------------------------------|-------------|
| `scenario_gwd_root` | Show available bases | optional lang query | GET /gwd | Renders index with list of available bases and links (lang preserved) | ❌ |
