from pydantic import BaseModel

class MyFirstModel(BaseModel):
    first_name: str
    last_name: str

# Test the basic example
print("=== Example 1: Basic Model ===")
try:
    validating = MyFirstModel(first_name="marc", last_name="nealer")
    print(f"✅ Valid data: {validating}")
    print(f"   First name: {validating.first_name}")
    print(f"   Last name: {validating.last_name}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n--- Testing invalid data ---")
try:
    invalid = MyFirstModel(first_name=123, last_name="nealer")  # first_name should be string
    print(f"✅ This should not print: {invalid}")
except Exception as e:
    print(f"❌ Expected error: {e}") 