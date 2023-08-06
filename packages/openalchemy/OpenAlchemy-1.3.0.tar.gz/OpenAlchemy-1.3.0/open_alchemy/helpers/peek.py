"""Assemble the final schema and return its type."""

import typing

from open_alchemy import exceptions
from open_alchemy import facades
from open_alchemy import types

from . import ref


def type_(*, schema: types.Schema, schemas: types.Schemas) -> str:
    """
    Get the type of the schema.

    Raises TypeMissingError if the final schema does not have a type or the value is
    not a string.

    Args:
        schema: The schema for which to get the type.
        schemas: The schemas for $ref lookup.

    Returns:
        The type of the schema.

    """
    value = peek_key(schema=schema, schemas=schemas, key="type")
    if value is None:
        raise exceptions.TypeMissingError("Every property requires a type.")
    if not isinstance(value, str):
        raise exceptions.TypeMissingError(
            "A type property value must be of type string."
        )
    return value


def nullable(*, schema: types.Schema, schemas: types.Schemas) -> typing.Optional[bool]:
    """
    Retrieve the nullable property from a property schema.

    Raises MalformedSchemaError if the nullable value is not a boolean.

    Args:
        schema: The schema to get the nullable from.
        schemas: The schemas for $ref lookup.

    Returns:
        The nullable value.

    """
    value = peek_key(schema=schema, schemas=schemas, key="nullable")
    if value is None:
        return None
    if not isinstance(value, bool):
        raise exceptions.MalformedSchemaError(
            "A nullable value must be of type boolean."
        )
    return value


def format_(*, schema: types.Schema, schemas: types.Schemas) -> typing.Optional[str]:
    """
    Retrieve the format property from a property schema.

    Raises MalformedSchemaError if the format value is not a string.

    Args:
        schema: The schema to get the format from.
        schemas: The schemas for $ref lookup.

    Returns:
        The format value or None if it was not found.

    """
    value = peek_key(schema=schema, schemas=schemas, key="format")
    if value is None:
        return None
    if not isinstance(value, str):
        raise exceptions.MalformedSchemaError("A format value must be of type string.")
    return value


def max_length(*, schema: types.Schema, schemas: types.Schemas) -> typing.Optional[int]:
    """
    Retrieve the maxLength property from a property schema.

    Raises MalformedSchemaError if the maxLength value is not an integer.

    Args:
        schema: The schema to get the maxLength from.
        schemas: The schemas for $ref lookup.

    Returns:
        The maxLength value or None if it was not found.

    """
    value = peek_key(schema=schema, schemas=schemas, key="maxLength")
    if value is None:
        return None
    if not isinstance(value, int):
        raise exceptions.MalformedSchemaError(
            "A maxLength value must be of type integer."
        )
    return value


def read_only(*, schema: types.Schema, schemas: types.Schemas) -> typing.Optional[bool]:
    """
    Determine whether schema is readOnly.

    Raises MalformedSchemaError if the readOnly value is not a boolean.

    Args:
        schema: The schema to get readOnly from.
        schemas: The schemas for $ref lookup.

    Returns:
        Whether the schema is readOnly.

    """
    value = peek_key(schema=schema, schemas=schemas, key="readOnly")
    if value is None:
        return None
    if not isinstance(value, bool):
        raise exceptions.MalformedSchemaError(
            "A readOnly property must be of type boolean."
        )
    return value


def write_only(
    *, schema: types.Schema, schemas: types.Schemas
) -> typing.Optional[bool]:
    """
    Determine whether schema is writeOnly.

    Raises MalformedSchemaError if the writeOnly value is not a boolean.

    Args:
        schema: The schema to get writeOnly from.
        schemas: The schemas for $ref lookup.

    Returns:
        Whether the schema is writeOnly.

    """
    value = peek_key(schema=schema, schemas=schemas, key="writeOnly")
    if value is None:
        return None
    if not isinstance(value, bool):
        raise exceptions.MalformedSchemaError(
            "A writeOnly property must be of type boolean."
        )
    return value


def description(
    *, schema: types.Schema, schemas: types.Schemas
) -> typing.Optional[str]:
    """
    Retrieve the description property from a property schema.

    Raises MalformedSchemaError if the description value is not a string.

    Args:
        schema: The schema to get the description from.
        schemas: The schemas for $ref lookup.

    Returns:
        The description value or None if it was not found.

    """
    value = peek_key(schema=schema, schemas=schemas, key="description")
    if value is None:
        return None
    if not isinstance(value, str):
        raise exceptions.MalformedSchemaError(
            "A description value must be of type string."
        )
    return value


def primary_key(*, schema: types.Schema, schemas: types.Schemas) -> bool:
    """
    Determine whether property schema is for a primary key.

    Raises MalformedSchemaError if the x-primary-key value is not a boolean.

    Args:
        schema: The schema to get x-primary-key from.
        schemas: The schemas for $ref lookup.

    Returns:
        Whether the schema is for a primary key property.

    """
    value = peek_key(schema=schema, schemas=schemas, key="x-primary-key")
    if value is None:
        return False
    if not isinstance(value, bool):
        raise exceptions.MalformedSchemaError(
            "The x-primary-key property must be of type boolean."
        )
    return value


def tablename(*, schema: types.Schema, schemas: types.Schemas) -> typing.Optional[str]:
    """
    Retrieve the tablename of the schema.

    Raises MalformedSchemaError if the tablename value is not a string.

    Args:
        schema: The schema to get tablename from.
        schemas: The schemas for $ref lookup.

    Returns:
        The tablename or None.

    """
    value = peek_key(schema=schema, schemas=schemas, key="x-tablename")
    if value is None:
        return None
    if not isinstance(value, str):
        raise exceptions.MalformedSchemaError(
            "The x-tablename property must be of type string."
        )
    return value


def inherits(
    *, schema: types.Schema, schemas: types.Schemas
) -> typing.Optional[typing.Union[str, bool]]:
    """
    Retrieve the value of the x-inherits extension property of the schema.

    Raises MalformedSchemaError if the value is not a string nor a boolean.

    Args:
        schema: The schema to get x-inherits from.
        schemas: The schemas for $ref lookup.

    Returns:
        The inherits or None.

    """
    value = peek_key(schema=schema, schemas=schemas, key="x-inherits")
    if value is None:
        return None
    if not isinstance(value, (str, bool)):
        raise exceptions.MalformedSchemaError(
            "The x-inherits property must be of type string or boolean."
        )
    return value


def json(*, schema: types.Schema, schemas: types.Schemas) -> typing.Optional[bool]:
    """
    Retrieve the value of the x-json extension property of the schema.

    Raises MalformedSchemaError if the value is not a boolean.

    Args:
        schema: The schema to get x-json from.
        schemas: The schemas for $ref lookup.

    Returns:
        The x-json value or None if the schema does not have the key.

    """
    value = peek_key(schema=schema, schemas=schemas, key="x-json")
    if value is None:
        return None
    if not isinstance(value, bool):
        raise exceptions.MalformedSchemaError(
            "The x-json property must be of type boolean."
        )
    return value


def default(*, schema: types.Schema, schemas: types.Schemas) -> types.TColumnDefault:
    """
    Retrieve the default value and check it against the schema.

    Args:
        schema: The schema to retrieve the default value from.

    """
    # Retrieve value
    value = peek_key(schema=schema, schemas=schemas, key="default")
    if value is None:
        return None
    # Assemble schema
    resolved_schema: types.ColumnSchema = {
        "type": type_(schema=schema, schemas=schemas)
    }
    format_value = format_(schema=schema, schemas=schemas)
    max_length_value = max_length(schema=schema, schemas=schemas)
    if format_value is not None:
        resolved_schema["format"] = format_value
    if max_length_value is not None:
        resolved_schema["maxLength"] = max_length_value
    try:
        facades.jsonschema.validate(value, resolved_schema)
    except facades.jsonschema.ValidationError:
        raise exceptions.MalformedSchemaError(
            f"The default value does not conform to the schema. The value is: {value}"
        )
    return value


def peek_key(*, schema: types.Schema, schemas: types.Schemas, key: str) -> typing.Any:
    """
    Recursive type lookup.

    Raise MalformedSchemaError of a $ref value is seen again.

    Args:
        schema: The schema to look up the key in.
        schemas: All the schemas to resolve any $ref.
        key: The key to check for.
        seen_refs: All the $ref that have already been seen.

    Returns:
        The key value (if found) or None.

    """
    return _peek_key(schema, schemas, key, set())


def _peek_key(
    schema: types.Schema, schemas: types.Schemas, key: str, seen_refs: typing.Set[str]
) -> typing.Any:
    """Implement peek_key."""
    # Base case, look for type key
    value = schema.get(key)
    if value is not None:
        return value

    # Recursive case, look for $ref
    ref_value = schema.get("$ref")
    if ref_value is not None:
        # Check for circular $ref
        if ref_value in seen_refs:
            raise exceptions.MalformedSchemaError("Circular reference detected.")
        seen_refs.add(ref_value)

        _, ref_schema = ref.get_ref(ref=ref_value, schemas=schemas)
        return _peek_key(ref_schema, schemas, key, seen_refs)

    # Recursive case, look for allOf
    all_of = schema.get("allOf")
    if all_of is not None:
        for sub_schema in all_of:
            value = _peek_key(sub_schema, schemas, key, seen_refs)
            if value is not None:
                return value

    # Base case, type or ref not found or no type in allOf
    return None
