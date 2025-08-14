# Empathetic Code Reviewer

**Tagline:** Transforming Critical Feedback into Constructive Growth

## Overview

This program takes raw, critical code review comments and transforms them into empathetic, educational feedback using AI. It acts as a bridge between direct critique and supportive mentorship, helping teams maintain positive communication while preserving the technical value of code reviews.

## Features

- **Empathetic Rephrasing**: Converts harsh feedback into supportive guidance
- **Educational Context**: Explains the "why" behind each suggestion
- **Concrete Examples**: Provides improved code snippets
- **Contextual Awareness**: Adapts tone based on feedback severity
- **Resource Links**: Includes relevant documentation and best practices
- **Holistic Summary**: Provides encouraging overall assessment

## Installation

1. Clone this repository
2. Create virual env:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up your Groq API key:
   ```bash
   export GROQ_API_KEY="your-api-key-here"
   ```

## Usage

### Command Line
```bash
python empathetic_reviewer.py input.json
```

### Python API
```python
from empathetic_reviewer import EmpathethicCodeReviewer

reviewer = EmpathethicCodeReviewer()
result = reviewer.review_code(code_snippet, review_comments)
print(result)
```

## Input Format

The program expects a JSON object with two keys:

```json
{
  "code_snippet": "def get_active_users(users):\n    results = []\n    for u in users:\n        if u.is_active == True and u.profile_complete == True:\n            results.append(u)\n    return results",
  "review_comments": [
    "This is inefficient. Don't loop twice conceptually.",
    "Variable 'u' is a bad name.",
    "Boolean comparison '== True' is redundant."
  ]
}
```

## Output

The program generates a well-formatted Markdown report with:
- Positive rephrasing of each comment
- Technical explanation of the underlying principle
- Concrete code improvement suggestions
- Links to relevant documentation
- Encouraging summary

## Technical Approach

The solution uses advanced prompt engineering to:
1. Analyze the severity and context of each comment
2. Generate empathetic rephrasing while preserving technical accuracy
3. Provide educational context with software engineering principles
4. Suggest concrete improvements with working code examples
5. Link to authoritative resources for further learning