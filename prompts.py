import json
from typing import Dict, Any


def get_validation_prompt(user_data: Dict[str, Any]) -> str:
   
   prompt = f"""You are a strict data validator. Validate the following user profile data and return ONLY a valid JSON response with no additional text.

User Profile Data:
{json.dumps(user_data, indent=2)}

Validation Instructions:
You must validate this data against the following constraints:

ERRORS (Critical issues - field is invalid):
1. The 'name' field is mandatory. If missing or empty, this is an error.
2. If 'email' is provided, it must be a valid email address format (must contain @ and a domain).
3. If 'age' is provided, it must be a positive number (greater than 0). Negative numbers or zero are errors.
4. If 'country' is provided, it must be a valid ISO-2 country code format (exactly 2 uppercase letters, like US, IN, GB, etc.). Common country codes include: US, IN, GB, CA, AU, DE, FR, JP, BR, MX, etc.
5. The 'phone' field is mandatory. If present, it must follow the E.164 international format (starts with + and contains only digits, typically +[country code][number], like +919876543210 for India).

WARNINGS (Non-critical issues - field is present but suboptimal):
1. If 'age' is provided and less than 18, issue a warning.
2. If 'name' is provided but contains fewer than 3 characters, issue a warning.
3. If 'email' is provided and uses a known disposable/temporary email domain (like akixpres.com, tempmail.com, guerrillamail.com, etc.), issue a warning.
4. If both 'phone' and 'country' are provided, check if the country code in the phone number (the digits immediately after the + sign) aligns with the country code. For example, phone +919876543210 starts with +91 (India), so country should be IN. If they don't match, issue a warning.

Important Rules:
- Only report fields that are present in the input. Ignore missing/null fields.
- Be strict with errors - if a field violates an error rule, report it.
- Be thoughtful with warnings - report actual issues, not false positives.
- All validation messages must reference the actual values from the input.
- If multiple rules apply to a field, report all of them.

Return ONLY this JSON structure, with no additional text before or after:
{{
  "is_valid": boolean (true only if errors list is empty),
  "errors": [list of error messages],
  "warnings": [list of warning messages]
}}

Example response format:
{{
  "is_valid": false,
  "errors": ["name is required", "email is not a valid email address"],
  "warnings": ["age is below recommended minimum"]
}}

Now validate the provided user profile data. Return only the JSON response:"""

   return prompt


