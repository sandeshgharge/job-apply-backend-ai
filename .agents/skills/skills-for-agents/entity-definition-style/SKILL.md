---
name: entity-definition-style
description: Enforce a standard Pydantic entity pattern for backend models and scan for missing patterns when adding new entities.
---

# Entity Definition Style (Backend)

When defining new Pydantic entity models in this backend project follow the exact pattern below and only create or modify entities when a new entity is required.

## Required pattern

At the top of the entity file define the shared camel case config:

camel_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

Then set the model configuration on every `BaseModel` subclass:

class JobDetails(BaseModel):
    model_config = camel_config

This ensures JSON keys use camelCase aliases while allowing population by field name.

## When to apply this skill
- Use this guidance only when creating a new entity model file or adding a new `BaseModel` subclass that represents a persisted/transported entity.
- Do not apply it to transient DTOs or internal helper classes unless they are used across the API boundary.

## Automatic checks the agent should perform
When this skill is active the agent should scan the backend codebase (at minimum the `entities/` folder) and report any `BaseModel` subclasses that are missing either:

- the `camel_config` definition at file top (a `ConfigDict` using `to_camel`), or
- the `model_config = camel_config` assignment on the `BaseModel` subclass.

Report matches with file paths and line ranges and do not add or modify files unless the task explicitly requests creation of a new entity.

## Implementation notes
- If instructed to create a new entity, add the `camel_config` line once at top of the file (importing `ConfigDict` and `to_camel` where needed), then set `model_config = camel_config` on the class.
- If a file already imports `to_camel`/`ConfigDict`, reuse the existing import statements.
- Keep all existing field validators and other model logic intact.

## Examples

Correct file header snippet:

from pydantic import BaseModel, ConfigDict, field_validator
from pydantic.alias_generators import to_camel

camel_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

class MyEntity(BaseModel):
    model_config = camel_config
    id: Optional[str] = None

## Goal
Ensure a consistent, camelCase JSON surface for backend entities and provide a fast audit report of entity files when asked.
