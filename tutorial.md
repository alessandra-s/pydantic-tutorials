# Pydantic Tutorial Guide

## What is Pydantic?

Pydantic is Python Dataclasses with validation, serialization and data transformation functions. You can use Pydantic to:
- Check your data is valid
- Transform data into the shapes you need
- Serialize the results so they can be moved on to other applications

## Basic Example

Let's say you have a function that expects a first and last name. You need to ensure both are there and that they are strings.

```python
from pydantic import BaseModel

class MyFirstModel(BaseModel):
    first_name: str
    last_name: str

validating = MyFirstModel(first_name="marc", last_name="nealer")
```

**Key Points:**
- Pydantic classes look almost the same as Python dataclasses
- Unlike a dataclass, Pydantic will check the values are strings and issue validation errors if they are not
- Validating by the type given is known as **default validation**

## More Complex Example - Optional Parameters

When it comes to optional parameters, Pydantic handles them with no problem, but the typing might not be what you expect:

```python
from pydantic import BaseModel
from typing import Union, Optional

class MySecondModel(BaseModel):
    first_name: str
    middle_name: Union[str, None]  # Parameter doesn't have to be sent
    title: Optional[str]           # Parameter should be sent, but can be None
    last_name: str
```

**Important Distinction:**
- `Union[str, None]` - Parameter is optional (doesn't have to be sent)
- `Optional[str]` - Parameter should be sent, even if it's None

## Working with Collections and Complex Types

You can use all the objects from the typing library and Pydantic will validate against them:

```python
from pydantic import BaseModel
from typing import Union, List, Dict
from datetime import datetime

class MyThirdModel(BaseModel):
    name: Dict[str, str]
    skills: List[str]
    holidays: List[Union[str, datetime]]
```

## Default Values

### Basic Defaults

```python
from pydantic import BaseModel

class DefaultsModel(BaseModel):
    first_name: str = "jane"
    middle_names: list = []  # ⚠️ PROBLEM: Shared between all instances
    last_name: str = "doe"
```

### Proper Defaults with Field

There's a problem with the list definition above - only one list object is created and shared between all instances. To resolve this, use the `Field` object:

```python
from pydantic import BaseModel, Field

class DefaultsModel(BaseModel):
    first_name: str = "jane"
    middle_names: list = Field(default_factory=list)  # ✅ Correct way
    last_name: str = "doe"
```

**Important:** A class or function is passed to `default_factory`, not an instance. This creates a new instance for all model instances.

## Nesting Models

Nesting models is really simple:

```python
from pydantic import BaseModel

class NameModel(BaseModel):
    first_name: str
    last_name: str
    
class UserModel(BaseModel):
    username: str
    name: NameModel
```

## Custom Validation

### Before and After Validation

- **Field validation:** Before/After refers to the default type validation
- **Model validation:** Before = before object initialization, After = after object initialization and other validation

### Field Validation with Annotated Validators

Preferred approach using `Annotated` validators (clean and easy to understand):

```python
from pydantic import BaseModel, BeforeValidator, ValidationError
import datetime
from typing import Annotated

def stamp2date(value):
    if not isinstance(value, float):
        raise ValidationError("incoming date must be a timestamp")
    try:
        res = datetime.datetime.fromtimestamp(value)
    except ValueError:
        raise ValidationError("Time stamp appears to be invalid")
    return res

class DateModel(BaseModel):
    dob: Annotated[datetime.datetime, BeforeValidator(stamp2date)]
```

### Multiple Validators

You can apply multiple validators:

```python
from pydantic import BaseModel, BeforeValidator, AfterValidator, ValidationError
import datetime
from typing import Annotated

def one_year(value):
    if value < datetime.datetime.today() - datetime.timedelta(days=365):
        raise ValidationError("the date must be less than a year old")
    return value

def stamp2date(value):
    if not isinstance(value, float):
        raise ValidationError("incoming date must be a timestamp")
    try:
        res = datetime.datetime.fromtimestamp(value)
    except ValueError:
        raise ValidationError("Time stamp appears to be invalid")
    return res

class DateModel(BaseModel):
    dob: Annotated[datetime.datetime, BeforeValidator(stamp2date), AfterValidator(one_year)]
```

### Optional Fields with Validation

```python
from pydantic import BaseModel, BeforeValidator, ValidationError, Field
import datetime
from typing import Annotated

def stamp2date(value):
    if not isinstance(value, float):
        raise ValidationError("incoming date must be a timestamp")
    try:
        res = datetime.datetime.fromtimestamp(value)
    except ValueError:
        raise ValidationError("Time stamp appears to be invalid")
    return res

class DateModel(BaseModel):
    dob: Annotated[Annotated[datetime.datetime, BeforeValidator(stamp2date)] | None, Field(default=None)]
```

## Model Validation

For validation that requires checking multiple fields together (e.g., at least one of several optional fields must be provided):

### After Validation

```python
from pydantic import BaseModel, model_validator, ValidationError
from typing import Union

class AllOptionalAfterModel(BaseModel):
    param1: Union[str, None] = None
    param2: Union[str, None] = None
    param3: Union[str, None] = None
    
    @model_validator(mode="after")
    def there_must_be_one(self):
        if not (self.param1 or self.param2 or self.param3):
            raise ValidationError("One parameter must be specified")
        return self
```

### Before Validation

```python
from pydantic import BaseModel, model_validator, ValidationError
from typing import Union, Any

class AllOptionalBeforeModel(BaseModel):
    param1: Union[str, None] = None
    param2: Union[str, None] = None
    param3: Union[str, None] = None
    
    @model_validator(mode="before")
    @classmethod  # ⚠️ IMPORTANT: Must specify both decorators in this order
    def there_must_be_one(cls, data: Any):
        if not (data["param1"] or data["param2"] or data["param3"]):
            raise ValidationError("One parameter must be specified")
        return data
```

**Important Notes:**
- Before validation: Use `@classmethod` decorator in addition to `@model_validator`
- Order of decorators matters!
- Before validation receives raw data (usually a dictionary)
- Must return the data object

## Aliases

Aliases help when dealing with incoming data that has different field names than your model.

### Basic Alias Configuration

```python
from pydantic import AliasGenerator, BaseModel, ConfigDict

class Tree(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=lambda field_name: field_name.upper(),
            serialization_alias=lambda field_name: field_name.title(),
        )
    )

    age: int
    height: float
    kind: str

t = Tree.model_validate({'AGE': 12, 'HEIGHT': 1.2, 'KIND': 'oak'})
print(t.model_dump(by_alias=True))  # {'Age': 12, 'Height': 1.2, 'Kind': 'oak'}
```

**Note:** To serialize using serialization aliases, use `by_alias=True`

### AliasChoices - Multiple Possible Field Names

For data where the same field might have different names:

```python
from pydantic import BaseModel, ConfigDict, AliasGenerator, AliasChoices

aliases = {
    "first_name": AliasChoices("fname", "surname", "forename", "first_name"),
    "last_name": AliasChoices("lname", "family_name", "last_name")
}

class FirstNameChoices(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=lambda field_name: aliases.get(field_name, None)
        )
    )
    title: str
    first_name: str
    last_name: str
```

**Tip:** Include the actual field name in the `AliasChoices` list for round-trip compatibility.

### AliasPath - Nested Data Access

For accessing values in nested dictionaries:

```python
from pydantic import BaseModel, ConfigDict, AliasGenerator, AliasPath

aliases = {
    "first_name": AliasPath("name", "first_name"),
    "last_name": AliasPath("name", "last_name")
}

class FirstNameChoices(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=lambda field_name: aliases.get(field_name, None)
        )
    )
    title: str
    first_name: str
    last_name: str

obj = FirstNameChoices(**{
    "name": {"first_name": "marc", "last_name": "Nealer"},
    "title": "Master Of All"
})
```

### Combining AliasPath and AliasChoices

You can use both together for maximum flexibility:

```python
from pydantic import BaseModel, ConfigDict, AliasGenerator, AliasPath, AliasChoices

aliases = {
    "first_name": AliasChoices("first_name", AliasPath("name", "first_name")),
    "last_name": AliasChoices("last_name", AliasPath("name", "last_name"))
}

class FirstNameChoices(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=lambda field_name: aliases.get(field_name, None)
        )
    )
    title: str
    first_name: str
    last_name: str

obj = FirstNameChoices(**{
    "name": {"first_name": "marc", "last_name": "Nealer"},
    "title": "Master Of All"
})
```

## Key Takeaways

1. **Pydantic is powerful but has many ways to do the same thing** - stick to consistent patterns
2. **Use `Annotated` validators over `Field()` for cleaner code**
3. **Be careful with mutable defaults** - use `Field(default_factory=...)` for lists/dicts
4. **Model validation is great for cross-field validation**
5. **Aliases are essential for real-world data transformation**

## Warning About AI Assistance

⚠️ **Important:** ChatGPT, Gemini, etc. give erratic answers about Pydantic. They often mix up Pydantic V1 and V2 syntax or claim Pydantic "can't do" things it actually can. Best to avoid them when learning this library and stick to official documentation and tested examples like these.

---

*This guide covers the essential patterns you'll need for most Pydantic use cases. Keep it handy as a reference while coding!*