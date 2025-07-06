from pydantic import BaseModel
from typing import Union, Optional

class NameModel(BaseModel):
    first_name: str
    middle_name: Union[str, None] = None  # Can be string OR None, defaults to None
    last_name: str

print("=== Understanding Union[str, None] ===")

print("\n--- Test 1: With middle name ---")
name1 = NameModel(
    first_name="John",
    middle_name="Michael",  # String value
    last_name="Doe"
)
print(f"✅ Result: {name1}")
print(f"   First: {name1.first_name}")
print(f"   Middle: {name1.middle_name}")
print(f"   Last: {name1.last_name}")

print("\n--- Test 2: Without middle name ---")
name2 = NameModel(
    first_name="Jane",
    # middle_name not provided - becomes None
    last_name="Smith"
)
print(f"✅ Result: {name2}")
print(f"   First: {name2.first_name}")
print(f"   Middle: {name2.middle_name}")  # This will be None
print(f"   Last: {name2.last_name}")

print("\n--- Test 3: Explicitly None ---")
name3 = NameModel(
    first_name="Bob",
    middle_name=None,  # Explicitly None
    last_name="Johnson"
)
print(f"✅ Result: {name3}")
print(f"   Middle: {name3.middle_name}")

print("\n--- What Union[str, None] means ---")
print("• The field can accept a string value")
print("• The field can accept None")
print("• The field can be omitted entirely (becomes None)")
print("• It does NOT combine or merge names")
print("• It does NOT make last_name optional")
print("• It's just type validation: 'accept string or None'") 