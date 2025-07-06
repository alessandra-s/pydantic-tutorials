# Pydantic Deep Learning Project

## Overview
This repository documents my deep dive into Pydantic, focusing on understanding the library intimately through hands-on experimentation, testing theories, and connecting concepts to existing knowledge.

## Learning Philosophy
I'm not just working through tutorials - I'm testing theories, connecting to past learning, and adjusting my thinking when wrong to understand Pydantic intimately.

## Project Structure

```
Pydantic Tutorials/
├── tutorial.md              # Main tutorial guide
├── examples/                # All runnable code examples
│   ├── example1_basic.py
│   └── union_explanation.py
├── learning_journal/        # Deep learning reflections
│   ├── learning_journal.md  # Main learning journal
│   └── union_typing_reflection.md
├── requirements.txt         # Dependencies
└── README.md               # This file
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

### Running Examples
Navigate to the examples directory and run any example:
```bash
cd examples
python example1_basic.py
python union_explanation.py
```

## Learning Approach

### 1. Systematic Tutorial Progress
- Follow `tutorial.md` as the main guide
- Create examples for each concept
- Test understanding with hands-on code

### 2. Deep Learning Through Testing
- Start with assumptions and test them
- Document misconceptions and corrections
- Connect new concepts to existing knowledge
- Identify similarities and differences

### 3. Cross-Domain Connections
- Relate Python concepts to set theory, SQL, etc.
- Identify similarities and differences
- Use analogies carefully
- Document misconceptions, corrections within self-learning and key insights

## Key Insights Documented

### Union Type Confusion
- **Misconception**: Union combines values like set theory
- **Reality**: Union specifies allowed types for a field
- **Key Insight**: `Union[str, None]` means "accept string OR None"

See `learning_journal/union_typing_reflection.md` for detailed analysis.

## Contributing
This is a personal learning project, but suggestions and corrections are welcome!

## License
MIT License - feel free to use this for your own learning journey. 