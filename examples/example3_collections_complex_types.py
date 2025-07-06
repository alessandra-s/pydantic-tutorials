from pydantic import BaseModel
from typing import Union, List, Dict
from datetime import datetime
import json

#using multiple objects from typing library to show how Pydanitc can handle dynamic validation
class MyThirdModel(BaseModel):
    name: Dict[str,str]
    skills: List[str]
    holidays: List[Union[str, datetime]] 

print("Testing Pydantic Dynamic Type Handling & Validation")




# Test # 1: Valid data

print("=== Example 3: Multi-type Model (Valid Data) ===")
try:
    valid_data = MyThirdModel(
        name={"first": "Collapsing", "last": "Willpower"},
        skills=["Python", "JavaScript", "Docker"],
        holidays=["Christmas", datetime(2024,12,25)]
    )
    print("✅ SUCCESS:", valid_data)
    print("     Type of holidays[1]:", type(valid_data.holidays[1]))
except Exception as e:
    print("❌ FAILED:", e)




# Test 2: Dict Validaiton - wrong value type

print("=== Test 1: Dict Validaiton - wrong value type) ===")
try: 
    invalid_dict = MyThirdModel(
        name= {"first": "Ava", "last": 524}, #last should be str, not int
        skills=["Flying"],
        holidays= ["Valentines Day", datetime(2025,2,14)]
    )
    print("✅ SUCCESS:", invalid_dict)
except Exception as e:
    print("❌ FAILED (Expected):", e)




# Test 3: Dict validation - Wrong key type

print("=== Test 2:Dict Validaiton - wrong key type) ===")
try:
    invalid_key = MyThirdModel(
        name={1: "John", "last": "Doe"},  # key should be str, not int
        skills=["Python"],
        holidays=["Christmas"]
    )
    print("✅ SUCCESS:", invalid_key)
except Exception as e:
    print("❌ FAILED (Expected):", e)




# Test 4: List validation - Wrong item type

print("=== Test 4: List Validation - Wrong Item Type ===")
try:
    invalid_list = MyThirdModel(
        name={"first": "Death", "last": "Grips"},
        skills=["Chronically Online", 123, "Docker"],  # 123 should be str
        holidays=["Every Damn Day of My Life"]
    )
    print("✅ SUCCESS:", invalid_list)
except Exception as e:
    print("❌ FAILED (Expected):", e)




# Test 5: Union type flexibility - Mixed types in holidays

print("=== Test 5: Union Type Flexibility - Mixed Types ===")
try:
    mixed_union = MyThirdModel(
        name={"first": "Alice", "last": "Climbs"},
        skills=["React", "Node.js"],
        holidays=[
            "Christmas",                    # str
            datetime(2024, 7, 4),          # datetime
            "Easter",                      # str
            datetime(2024, 12, 31, 23, 59) # datetime with time
        ]
    )
    print("✅ SUCCESS:", mixed_union)
    print("   Holiday types:", [type(h).__name__ for h in mixed_union.holidays])
except Exception as e:
    print("❌ FAILED:", e)



# Test 6: Union validation failure - Invalid type

print("=== Test 6: Union Validation - Invalid Type ===")
try:
    invalid_union = MyThirdModel(
        name={"first": "Bob", "last": "Johnson"},
        skills=["Vue.js"],
        holidays=["Christmas", 12345]  # int not allowed in Union[str, datetime]
    )
    print("✅ SUCCESS:", invalid_union)
except Exception as e:
    print("❌ FAILED (Expected):", e)




# Test 7: Automatic type coercion

print("=== Test 7: Automatic Type Coercion ===")
try:
    # Pydantic will try to convert compatible types
    coercion_test = MyThirdModel(
        name={"first": "Charlie", "last": "Brown"},
        skills=["AWS", "GCP"],  # These are already strings
        holidays=["2024-12-25"]  # String that could be converted to datetime
    )
    print("✅ SUCCESS:", coercion_test)
    print("   Holiday types:", [type(h).__name__ for h in coercion_test.holidays])
except Exception as e:
    print("❌ FAILED:", e)




# Test 8: Empty collections

print("=== Test 8: Empty Collections ===")
try:
    empty_collections = MyThirdModel(
        name={},  # Empty dict
        skills=[],  # Empty list
        holidays=[]  # Empty list
    )
    print("✅ SUCCESS:", empty_collections)
except Exception as e:
    print("❌ FAILED:", e)




# Test 9: Nested complexity

print("=== Test 9: Nested Complexity ===")
try:
    complex_data = MyThirdModel(
        name={
            "first": "David",
            "middle": "Michael",
            "last": "Wilson",
            "suffix": "Jr."
        },
        skills=[
            "Python", "JavaScript", "TypeScript", "Go", "Rust",
            "Docker", "Kubernetes", "AWS", "GCP", "Azure"
        ],
        holidays=[
            "Christmas", "New Year", "Easter", "Thanksgiving",
            datetime(2024, 1, 1), datetime(2024, 12, 25),
            datetime(2024, 7, 4, 12, 0, 0)
        ]
    )
    print("✅ SUCCESS:", complex_data)
    print("   Name keys:", list(complex_data.name.keys()))
    print("   Skills count:", len(complex_data.skills))
    print("   Holiday mix:", [type(h).__name__ for h in complex_data.holidays])
except Exception as e:
    print("❌ FAILED:", e)



##Bonus: introduce serialization
# Test 10: JSON serialization and deserialization

print("=== Test 10: JSON Serialization/Deserialization ===")
try:
    original = MyThirdModel(
        name={"first": "Eve", "last": "Anderson"},
        skills=["Machine Learning", "Data Science"],
        holidays=["Memorial Day", datetime(2024, 5, 27)]
    )
    
    # Serialize to JSON
    json_str = original.model_dump_json()
    print("✅ JSON Serialization:", json_str[:100] + "...")
    
    # Deserialize from JSON
    json_data = json.loads(json_str)
    recreated = MyThirdModel(**json_data)
    print("✅ JSON Deserialization:", recreated)
    
except Exception as e:
    print("❌ FAILED:", e)




# Test 11: Model validation with dict input

print("=== Test 11: Dict Input Validation ===")
try:
    dict_input = {
        "name": {"first": "Frank", "last": "Miller"},
        "skills": ["Photography", "Videography"],
        "holidays": ["Labor Day", "2024-09-02"]
    }
    
    from_dict = MyThirdModel(**dict_input)
    print("✅ Dict Input SUCCESS:", from_dict)
    
    # Using model_validate (more explicit)
    from_validate = MyThirdModel.model_validate(dict_input)
    print("✅ model_validate SUCCESS:", from_validate)
    
except Exception as e:
    print("❌ FAILED:", e)




# Test 12: Edge cases and boundary conditions

print("=== Test 12: Edge Cases ===")
try:
    edge_cases = MyThirdModel(
        name={"": ""},  # Empty string keys and values (valid for Dict[str, str])
        skills=[""],  # Empty string in list (valid for List[str])
        holidays=[datetime.min, datetime.max]  # Extreme datetime values
    )
    print("✅ Edge Cases SUCCESS:", edge_cases)
except Exception as e:
    print("❌ FAILED:", e)


print("\n" + "=" * 60)
print("Observations:")
print("• Dict[str, str] validates both key AND value types")
print("• List[str] validates each item in the list")
print("• Union[str, datetime] accepts either type for each item")
print("• Pydantic provides detailed error messages for validation failures")
print("• Type coercion happens automatically when possible")
print("• Empty collections are valid unless specifically constrained")
print("• JSON serialization handles datetime conversion automatically")