# Mutable Defaults in Pydantic: Understanding the Pitfalls and Solutions

## What are “basic defaults” in Pydantic?
A “basic default” is when you assign a default value to a field directly in the class definition:

```python
class DefaultsModel(BaseModel):
    first_name: str = "Cynthia"
    middle_name: list = []  # ⚠️ Problem!
    last_name: str = "Frong"
```
- For `first_name` and `last_name`, the default is a string (an immutable type).
- For `middle_name`, the default is an empty list (a mutable type).

---

## Why is using a mutable default (like `[]`) a problem?
When you use a mutable object (like a list or dict) as a default value in a class, **that same object is shared across all instances** of the class. This means if you modify it in one instance, the change appears in all other instances!

**Example:**
```python
a = DefaultsModel()
b = DefaultsModel()
a.middle_name.append("Marie")
print(b.middle_name)  # ['Marie']  <-- Oops! Changed in both!
```
- This does NOT happen with immutable types like strings or numbers. Each instance gets its own copy.

---

## What does “shared between all instances” mean?
It means that every time you create a new instance of the class, if you don’t provide a value for `middle_name`, it will use the same list object as every other instance. So, changes to the list in one instance affect all others.

---

## What about `first_name` and `last_name`?
Strings are immutable in Python. When you assign a default string, each instance gets its own value. Changing the string in one instance does NOT affect others.

---

## How do you fix the mutable default problem?
Use `Field(default_factory=list)` (or `dict`, etc.) for mutable types. This tells Pydantic to create a new list for each instance.

```python
class DefaultsModel_Field(BaseModel):
    first_name: str = "Cynthia"
    middle_name: list = Field(default_factory=list)
    last_name: str = "Frong"
```

---

## Do I only use Field for empty objects?
You use `Field(default_factory=...)` for any mutable default (empty or not). If you want a default list with some items, you could use a lambda:
```python
middle_name: list = Field(default_factory=lambda: ["Marie"])
```
You can use `Field` for other purposes too (validation, metadata, etc.), but `default_factory` is specifically for creating new mutable objects per instance.

---

## Is this the validation aspect of Pydantic?
Not directly. This is about **object creation and Python’s behavior with mutable defaults**. Pydantic’s validation will still check types, but `Field(default_factory=...)` is about making sure each instance gets its own object.

---

## Test Examples
Here are some tests you can run to see the difference:

```python
from pydantic import BaseModel, Field

class DefaultsModel(BaseModel):
    first_name: str = "Cynthia"
    middle_name: list = []
    last_name: str = "Frong"

class DefaultsModel_Field(BaseModel):
    first_name: str = "Cynthia"
    middle_name: list = Field(default_factory=list)
    last_name: str = "Frong"

print("=== Mutable Default Problem ===")
a = DefaultsModel()
b = DefaultsModel()
a.middle_name.append("Marie")
print("a.middle_name:", a.middle_name)  # ['Marie']
print("b.middle_name:", b.middle_name)  # ['Marie']  <-- Problem: shared!

print("\n=== Using Field (No Sharing) ===")
x = DefaultsModel_Field()
y = DefaultsModel_Field()
x.middle_name.append("Marie")
print("x.middle_name:", x.middle_name)  # ['Marie']
print("y.middle_name:", y.middle_name)  # []  <-- Correct: not shared!
```

---

## Summary Table

| Field Type      | Default Assignment         | Shared? | Use Field?         |
|-----------------|---------------------------|---------|--------------------|
| Immutable (str) | `first_name: str = "A"`   | No      | Not needed         |
| Mutable (list)  | `middle_name: list = []`  | Yes     | Use default_factory|

---

**In short:**
- Use `Field(default_factory=...)` for mutable defaults to avoid shared state.
- This is a Python quirk, not a Pydantic-specific feature, but Pydantic makes it easy to do the right thing. 