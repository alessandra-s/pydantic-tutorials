# Pydantic Deep Learning Project

## Overview
This repository documents my deep dive into Pydantic, focusing on understanding the library intimately through hands-on experimentation, testing theories, and connecting concepts to existing knowledge.

## Learning Philosophy
I'm not just working through tutorials - I'm testing theories, connecting to past learning, and adjusting my thinking when wrong to understand Pydantic intimately.

## Project Structure

```
Pydantic Tutorials/
├── tutorial.md # Main tutorial guide
├── examples/ # All runnable code examples
│ ├── example1_basic.py
│ ├── example2_optional_parameters.py
│ ├── example2_union_explanation.py
│ └── example3_collections_complex_types.py
├── learning_journal/ # Deep learning reflections
│ └── learning_journal.md
├── requirements.txt # Dependencies
├── README.md # This file
└── .gitignore # Git ignore rules
```

## Getting Started

### Prerequisites
- Python 3.9+
- pip

### Setup
1. Clone the repository
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```


## Examples

### Example 1: Basic Model
- Shows simple Pydantic model validation for required string fields.

### Example 2: Optional Parameters & Union Types
- `example2_optional_parameters.py`: Demonstrates how to use `Optional` and `Union` for fields that may be omitted or set to `None`.
- `example2_union_explanation.py`: Explores how `Union` works in Pydantic and clarifies common misconceptions.

### Example 3: Collections & Complex Types
- `example3_collections_complex_types.py`: Demonstrates validation for nested types, lists, dictionaries, unions, and serialization/deserialization.

## Learning Journal
See `learning_journal/learning_journal.md` for a detailed record of challenges, insights, and connections to prior knowledge.

## Getting Started

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run examples:
   ```bash
   cd examples
   python example1_basic.py
   python example2_optional_parameters.py
   python example2_union_explanation.py
   python example3_collections_complex_types.py
   ```

## Contributing
This is a personal learning project, but suggestions and corrections are welcome!
