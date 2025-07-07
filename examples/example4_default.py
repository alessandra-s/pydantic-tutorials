from pydantic import BaseModel, Field

# This example demonstrates the difference between basic defaults and proper handling of mutable defaults in Pydantic.

# --- Basic Defaults (with a mutable default problem) ---
class DefaultsModel(BaseModel):
    first_name: str = "Cynthia"  # Immutable default (safe)
    middle_name: list = []        # ⚠️ Mutable default (problem: shared between all instances)
    last_name: str = "Frong"     # Immutable default (safe)

# The 'middle_name' list is created once and shared by all instances of DefaultsModel.
# This means if you modify 'middle_name' in one instance, it affects all others!
# 'first_name' and 'last_name' are strings (immutable), so each instance gets its own value.

# --- Example: Demonstrate the problem ---
print("=== Mutable Default Problem ===")
a = DefaultsModel()
b = DefaultsModel()
a.middle_name.append("Marie")  # Modifies the shared list
print("a.middle_name:", a.middle_name)  # ['Marie']
print("b.middle_name:", b.middle_name)  # ['Marie']  <-- Problem: shared!
# Now, both a.middle_name and b.middle_name will show ['Marie']

# --- Proper Defaults with Field (solves the problem) ---
class DefaultsModel_Field(BaseModel):
    first_name: str = "Cynthia"  # Immutable default (safe)
    middle_name: list = Field(default_factory=list)  # ✅ Each instance gets its own list
    last_name: str = "Frong"     # Immutable default (safe)

# Using Field with default_factory ensures a new list is created for each instance.
# Modifying one instance's 'middle_name' does NOT affect others.

# --- Example: Demonstrate the correct behavior ---
print("\n=== Using Field (No Sharing) ===")
x = DefaultsModel_Field()
y = DefaultsModel_Field()
x.middle_name.append("Holden")  # Only x is affected
print("x.middle_name:", x.middle_name)  # ['Holden']
print("y.middle_name:", y.middle_name)  # []  <-- Correct: not shared!
# x.middle_name is ['Holden'], y.middle_name is []

# --- Summary ---
# Use Field(default_factory=list) for mutable defaults to avoid shared state between instances.
# This is a common Python pitfall, not just a Pydantic issue, but Pydantic makes it easy to do the right thing. 