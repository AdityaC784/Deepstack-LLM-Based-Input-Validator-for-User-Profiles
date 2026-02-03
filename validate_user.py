import json
import sys
import os
import re
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv
load_dotenv()

try:
    from groq import Groq
except ImportError:
    print("Error: groq library not installed. Run: pip install groq")
    sys.exit(1)

from prompts import get_validation_prompt


class UserValidator:
   
    def __init__(self):
        self.client = Groq()
        self.model = os.getenv("GROQ_MODEL")
        
    def validate(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        prompt = get_validation_prompt(user_data)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                max_completion_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            response_text = response.choices[0].message.content
            print("DEBUG: \n" + response_text)
            result = self._parse_llm_response(response_text)

            if not self._validate_schema(result):
                return {
                    "is_valid": False,
                    "errors": ["Invalid response schema from validator"],
                    "warnings": []
                }
            return result

        except json.JSONDecodeError as e:
            return {
                "is_valid": False,
                "errors": [f"Failed to parse validator response: {str(e)}"],
                "warnings": []
            }
        except Exception as e:
            return {
                "is_valid": False,
                "errors": [f"Validation error: {str(e)}"],
                "warnings": []
            }

    def _parse_llm_response(self, response_text: str) -> Dict[str, Any]:
       
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL)
        if json_match:
            response_text = json_match.group(1)
        
        
        try:
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}')
            
            if start_idx != -1 and end_idx != -1:
                json_str = response_text[start_idx:end_idx + 1]
                return json.loads(json_str)
        except (json.JSONDecodeError, ValueError):
            pass

        raise json.JSONDecodeError(
            "Could not find valid JSON in response",
            response_text,
            0
        )

    def _validate_schema(self, result: Dict[str, Any]) -> bool:
       
        required_keys = {"is_valid", "errors", "warnings"}
        
        if not isinstance(result, dict):
            return False
        
        if set(result.keys()) != required_keys:
            return False
        
        if not isinstance(result.get("is_valid"), bool):
            return False
        
        if not isinstance(result.get("errors"), list):
            return False
        
        if not isinstance(result.get("warnings"), list):
            return False
        
     
        for item in result.get("errors", []):
            if not isinstance(item, str):
                return False
        
        for item in result.get("warnings", []):
            if not isinstance(item, str):
                return False
        
        return True

                                            
def load_json_file(file_path: str) -> Dict[str, Any]:
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Input file not found: {file_path}")
    
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"Invalid JSON in {file_path}",
            e.doc,
            e.pos
        )


def main():
    
    if len(sys.argv) < 2:
        print("Usage: python validate_user.py <input_file.json>")
        print("\nExample: python validate_user.py examples/input1.json")
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        user_data = load_json_file(input_file)
        validator = UserValidator()
        result = validator.validate(user_data)
        
        print(json.dumps(result, indent=2))
        sys.exit(0 if result.get("is_valid") else 1)

    except FileNotFoundError as e:
        error_result = {
            "is_valid": False,
            "errors": [str(e)],
            "warnings": []
        }
        print(json.dumps(error_result, indent=2))
        sys.exit(1)

    except json.JSONDecodeError as e:
        error_result = {
            "is_valid": False,
            "errors": [f"JSON parsing error: {str(e)}"],
            "warnings": []
        }
        print(json.dumps(error_result, indent=2))
        sys.exit(1)

    except Exception as e:
        error_result = {
            "is_valid": False,
            "errors": [f"Unexpected error: {str(e)}"],
            "warnings": []
        }
        print(json.dumps(error_result, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
