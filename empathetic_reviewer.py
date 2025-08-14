#!/usr/bin/env python3
"""
Empathetic Code Reviewer
Transforms critical code review comments into constructive, educational feedback.
"""

import json
import argparse
import os
import sys
from typing import List, Dict, Any
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class EmpathethicCodeReviewer:
    """
    AI-powered code review comment transformer that converts harsh feedback
    into empathetic, educational guidance.
    """
    
    def __init__(self, api_key: str = None):
        """Initialize the reviewer with Groq API key."""
        self.client = Groq(
            api_key=api_key or os.getenv("GROQ_API_KEY"),
        )
    
    def _analyze_comment_severity(self, comment: str) -> str:
        """Analyze the severity/tone of a review comment."""
        harsh_indicators = ['bad', 'wrong', 'terrible', 'awful', 'stupid', 'inefficient', 'don\'t']
        neutral_indicators = ['could', 'might', 'consider', 'suggest']
        
        comment_lower = comment.lower()
        
        if any(indicator in comment_lower for indicator in harsh_indicators):
            return "harsh"
        elif any(indicator in comment_lower for indicator in neutral_indicators):
            return "neutral"
        else:
            return "constructive"
    
    def _get_language_from_code(self, code_snippet: str) -> str:
        """Detect programming language from code snippet."""
        if 'def ' in code_snippet and ':' in code_snippet:
            return "Python"
        elif 'function' in code_snippet and '{' in code_snippet:
            return "JavaScript"
        elif 'public class' in code_snippet or 'private ' in code_snippet:
            return "Java"
        else:
            return "Python"  # Default assumption
    
    def _create_empathetic_prompt(self, code_snippet: str, comments: List[str]) -> str:
        """Create a sophisticated prompt for empathetic code review transformation."""
        
        language = self._get_language_from_code(code_snippet)
        severity_analysis = [self._analyze_comment_severity(comment) for comment in comments]
        
        prompt = f"""You are an exceptional senior software engineer and mentor known for your ability to provide constructive, empathetic feedback that helps developers grow. Your mission is to transform direct, potentially harsh code review comments into supportive, educational guidance.

**Context:**
- Programming Language: {language}
- Number of comments to transform: {len(comments)}
- Comment severity levels detected: {', '.join(set(severity_analysis))}

**Code Under Review:**
```{language.lower()}
{code_snippet}
```

**Original Review Comments:**
{chr(10).join(f"{i+1}. {comment}" for i, comment in enumerate(comments))}

**Your Task:**
Transform each comment into a well-structured analysis following this exact format for each comment:

---
### Analysis of Comment: "[Original Comment]"

**Positive Rephrasing:** [Rewrite the feedback to be encouraging and supportive while maintaining technical accuracy. Start with something positive about the code, then gently introduce the improvement opportunity.]

**The 'Why':** [Explain the underlying software engineering principle, performance consideration, or best practice. Make it educational and help the developer understand the deeper reasoning.]

**Suggested Improvement:**
```{language.lower()}
[Provide a concrete, working code example that demonstrates the recommended fix. Ensure the code is syntactically correct and represents a meaningful improvement.]
```

**Learn More:** [Provide a relevant link to official documentation, style guides, or authoritative resources that support this recommendation.]

---

**Instructions for tone adaptation:**
- For harsh comments: Be extra gentle and encouraging, acknowledge what's working first
- For neutral comments: Maintain supportive tone while being direct about improvements  
- For constructive comments: Enhance the existing positive tone with more detail

**After analyzing all comments, add:**

## Overall Assessment

[Provide a holistic, encouraging summary that:
1. Acknowledges the developer's effort and what they did well
2. Frames the suggestions as growth opportunities
3. Encourages continued learning and improvement
4. Maintains an optimistic, supportive tone]

**Quality Standards:**
- Be specific and actionable, not generic
- Ensure all code examples are syntactically correct and runnable
- Provide genuine technical insights, not just politeness
- Make explanations clear for developers at different skill levels
- Include relevant links to authoritative sources when possible"""

        return prompt
    
    def review_code(self, code_snippet: str, review_comments: List[str]) -> str:
        """
        Transform review comments into empathetic feedback.
        
        Args:
            code_snippet: The code being reviewed
            review_comments: List of original review comments
            
        Returns:
            Markdown-formatted empathetic review
        """
        try:
            prompt = self._create_empathetic_prompt(code_snippet, review_comments)
            
            response = self.client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an senior software engineer and mentor specializing in empathetic, educational code reviews. You excel at transforming harsh feedback into constructive guidance while maintaining technical accuracy."
                    },
                    {"role": "user", "content": prompt}
                ],
                stream=False,
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error generating empathetic review: {str(e)}"
    
    def process_json_input(self, json_data: Dict[str, Any]) -> str:
        """Process JSON input and return empathetic review."""
        if 'code_snippet' not in json_data or 'review_comments' not in json_data:
            raise ValueError("JSON must contain 'code_snippet' and 'review_comments' keys")
        
        return self.review_code(
            json_data['code_snippet'], 
            json_data['review_comments']
        )

def main():
    """Command line interface for the Empathetic Code Reviewer."""
    parser = argparse.ArgumentParser(
        description="Transform critical code review comments into empathetic, educational feedback"
    )
    parser.add_argument(
        'input_file', 
        help='JSON file containing code_snippet and review_comments'
    )
    parser.add_argument(
        '-o', '--output', 
        help='Output file for the empathetic review (default: stdout)'
    )
    
    args = parser.parse_args()
    
    try:
        # Load input JSON
        with open(args.input_file, 'r') as f:
            input_data = json.load(f)
        
        # Create reviewer and process
        reviewer = EmpathethicCodeReviewer()
        result = reviewer.process_json_input(input_data)
        
        # Output result
        if args.output:
            with open(args.output, 'w') as f:
                f.write(result)
            print(f"Empathetic review written to {args.output}")
        else:
            print(result)
            
    except FileNotFoundError:
        print(f"Error: Input file '{args.input_file}' not found", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in '{args.input_file}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()