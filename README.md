# LLM-Based Input Validator

A production-ready Python project that validates user profile data using prompt engineering with Large Language Models (LLMs). Built for the DeepStack AI/ML Internship Assignment.

## 🎯 Project Overview

This project implements a **strict input validator** that:
- Takes user profile JSON data as input
- Uses Claude (or compatible LLM) to validate based on high-level constraints
- Returns structured JSON output with validation results
- Includes comprehensive automated test suite using Promptfoo

### Key Design Principles

1. **LLM-Only Validation**: All validation logic delegated to the LLM via prompt engineering
2. **High-Level Constraints**: Rules expressed at a standard level (e.g., "E.164 format" instead of detailed regex patterns)
3. **Strict Schema Compliance**: Output always matches the required JSON schema
4. **No Hardcoded Rules**: The validator learns rules from prompts, not hardcoded checks

## 📋 Validation Rules

### Errors (Critical Issues)
- **Name**: Required and non-empty
- **Email**: Must be valid email format (if provided)
- **Age**: Must be positive number (if provided)
- **Country**: Must be ISO-2 country code like US, IN, GB (if provided)
- **Phone**: Required and must follow E.164 format (+[country code][number])

### Warnings (Non-Critical Issues)
- **Age**: Below 18 years old
- **Name**: Shorter than 3 characters
- **Email**: Uses disposable/temporary email domain
- **Phone-Country**: Mismatch between country code and phone number

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd llm-input-validator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Keys

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your GROQ API key
GROQ_API_KEY=your_actual_api_key_here
GROQ_MODEL="MODELNAME"
```



### 3. Run the Validator

```bash
# Validate a user profile
python validate_user.py examples/input1.json

# Example with valid input
python validate_user.py examples/input2.json

# Your own file
python validate_user.py path/to/your/input.json
```

### 4. Run Automated Evals

```bash
# Install promptfoo (if not already installed)
npm install -g promptfoo

#npm 
npm install 

# Run the test suite
promptfoo eval -c promptfoo.yaml

# View the HTML report
promptfoo view
```

## 📁 Project Structure

```
llm-input-validator/
├── validate_user.py          # Main validation script
├── prompts.py                # Prompt engineering templates
├── config.py                 # Configuration and constants
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── .env                     # Your actual environment variables (create from .env.example)
├── promptfoo.yaml           # Promptfoo test configuration
├── README.md                # This file
│
├── examples/                # Example input files
│   ├── input1.json         # Invalid input example
│   ├── input2.json         # Valid input example
│
└── tests/                   # Unit tests
    └── test_validator.py   # Test cases
```

## 💡 Usage Examples

### Example 1: Valid Input

```bash
python validate_user.py examples/input2.json
```

**Input** (`examples/input2.json`):
```json
{
  "name": "Aarav Patel",
  "email": "aarav.patel@gmail.com",
  "age": 24,
  "country": "IN",
  "phone": "+919876543210"
}
```

**Output**:
```json
{
  "is_valid": true,
  "errors": [],
  "warnings": []
}
```

### Example 2: Invalid Input

```bash
python validate_user.py examples/input1.json
```

**Input** (`examples/input1.json`):
```json
{
  "name": "",
  "email": "user@gmail",
  "age": 16,
  "country": "India",
  "phone": "99999"
}
```

**Output**:
```json
{
  "is_valid": false,
  "errors": [
    "name is required",
    "email is not a valid email address",
    "country must be a valid ISO-2 country code",
    "phone number is not in E.164 format"
  ],
  "warnings": [
    "age is below recommended minimum"
  ]
}
```

## 🧪 Testing with Promptfoo

### View Test Results

```bash
# Run evaluation with detailed output
promptfoo eval -c promptfoo.yaml --verbose

# Open HTML report
promptfoo view
```

### Test Coverage

The `promptfoo.yaml` includes 14 comprehensive test cases:

| Test Case | Description | Expected |
|-----------|-------------|----------|
| 1 | Valid user profile | `is_valid: true` |
| 2 | Multiple errors | `is_valid: false` with errors |
| 3 | Missing name | Error about name |
| 4 | Missing phone | Error about phone |
| 5 | Invalid email | Error about email format |
| 6 | Invalid phone format | Error about E.164 |
| 7 | Invalid country code | Error about country |
| 8 | Negative age | Error about age |
| 9 | Age below 18 | Warning triggered |
| 10 | Short name | Warning triggered |
| 11 | Disposable email | Warning triggered |
| 12 | Country-phone mismatch | Warning triggered |
| 13 | Null fields ignored | Properly handled |
| 14 | Minimal valid input | Success with minimal fields |

## 🔧 Technical Architecture

### Component Design

#### `validate_user.py`
- **UserValidator class**: Main validation engine
- **LLM Integration**: Calls Claude API with structured prompts
- **JSON Parsing**: Extracts JSON from markdown code blocks
- **Schema Validation**: Ensures output matches expected structure
- **Error Handling**: Graceful handling of malformed responses

#### `prompts.py`
- **High-Level Constraints**: Uses standard terminology (E.164, ISO-2)
- **No Rule Enumeration**: Avoids listing every validation detail
- **Context-Aware**: Includes examples and explanations
- **Flexible**: Can be adapted for different validation needs

#### `config.py`
- **API Configuration**: Centralized LLM settings
- **Constants**: Validation schemas and rules
- **ISO-2 Country Codes**: Sample list for reference
- **Disposable Email Domains**: Sample list for warnings

### How It Works

```
Input JSON
    ↓
prompts.py: Generate validation prompt with high-level rules
    ↓
GROQ.GROQ: Call Claude API
    ↓
LLM: Understands rules and validates data
    ↓
validate_user.py: Parse JSON response
    ↓
Validate schema and format
    ↓
Output structured JSON result
```

## 🎓 Prompt Engineering Strategy

### Key Principles Applied

1. **Standard Terminology**: Use recognized standards (E.164, ISO-2, etc.)
   ```
   Good: "Phone must be in E.164 format"
   Bad: "Phone must be +[digits only], no dashes"
   ```

2. **Context Over Rules**: Provide context rather than exhaustive lists
   ```
   Good: "Country code from phone should match the country field"
   Bad: "If phone is +91 and country is US, flag warning"
   ```

3. **Example-Driven**: Use examples to clarify expectations
   ```
   Good: "E.164 format example: +919876543210"
   Bad: "Exactly 10 digits after +"
   ```

4. **High-Level Constraints**: Let LLM infer details
   ```
   Good: "E.164 international phone format"
   Bad: "Must start with +, contain country code 1-3 digits, etc"
   ```

## 🔐 Security Considerations

- **No External APIs**: Only uses GROQ API for validation
- **No Data Storage**: All validation is stateless
- **Environment Variables**: API keys stored in `.env`, not in code
- **Input Validation**: Schema checked before processing
- **Output Sanitization**: JSON parsing with error handling

## 📊 Evaluation Criteria

Based on assignment requirements:

- ✅ **Output Quality**: Strict JSON schema compliance
- ✅ **Schema Discipline**: Validated at each step
- ✅ **Prompt Clarity**: High-level, standard-based rules
- ✅ **Eval Quality**: 14 comprehensive test cases
- ✅ **Ease of Use**: Single command to run everything
- ✅ **Communication**: Clear code and documentation

## 🚨 Troubleshooting

### "Invalid JSON in response"
- The LLM response doesn't contain valid JSON
- Try: Rerun the validator (LLM might have had a parsing issue)
- Check: Ensure API key is valid

### "Missing GROQ_API_KEY"
- Environment variable not set
- Solution: Create `.env` file from `.env.example` and add your key

### "HTTPError 401"
- Invalid or expired API key
- Solution: Update `GROQ_API_KEY` in `.env`

### Promptfoo not found
- Installation issue
- Solution: `npm install -g @promptfoo/promptfoo`

## 📈 Future Improvements

- [ ] Support for additional LLM providers (OpenAI, Cohere)
- [ ] Batch validation for multiple users
- [ ] Custom validation rule sets
- [ ] Performance benchmarking
- [ ] Extended ISO-2 country code list
- [ ] Extended disposable email domain list
- [ ] Caching for common validations
- [ ] Web API wrapper (Flask/FastAPI)

## 📝 License

MIT License - Feel free to use and modify



## 📞 Support

For questions or issues:
1. Check the README
2. Review the test cases in `promptfoo.yaml`
3. Check LLM response with verbose mode

---

**Created for**: DeepStack AI/ML 
**Last Updated**: January 2026


