# AGENTS.md

## Project overview
This is a beginner-friendly Python project that converts images of handwritten notes into 1 Markdown file.

Main workflow:
1. Read image files from `uploads/`
2. Extract text from each image using OCR
3. Convert extracted text into simple Markdown
4. Save output into one `.md` file in `output/`
5. Keep the code easy to understand and easy to explain

## Goals
- Prefer simple, readable Python over clever code
- Keep functions small
- Add comments for beginner understanding when useful
- Make minimal, safe changes
- Preserve working code unless a change is necessary

## Tech expectations
- Language: Python
- Use `pathlib` for file paths where possible
- Use `.env` for secrets
- Never hardcode API keys or secrets
- Assume secrets are loaded from environment variables
- Keep dependencies minimal unless there is a clear reason to add one

## File expectations
Important folders:
- `uploads/` = input images
- `output/` = generated markdown files
- `src/` = Python source code

Preferred structure:
- `src/main.py` as the entry point
- Split logic into small functions or helper modules only when it improves clarity

## Coding style
- Write beginner-friendly code
- Use straightforward loops and conditionals
- Avoid unnecessary abstraction
- Avoid large refactors unless requested
- Keep naming explicit and simple
- Explain non-obvious logic in comments

## When making changes
- First understand the current code before editing
- Make the smallest change that solves the task
- Do not rewrite unrelated parts of the project
- Do not add frameworks unless requested
- Do not add deployment/config complexity unless requested

## OCR and markdown behavior
- Handwriting OCR may be imperfect, so prefer robust and simple output
- Output Markdown should be clean and basic:
  - headings
  - paragraphs
- Do not invent content that is not visible in the image
- If text is unclear, preserve uncertainty rather than guessing aggressively

## Environment and secrets
- Load secrets from `.env`
- Never print secrets
- Never commit `.env`
- Never replace environment-variable usage with hardcoded values

Expected environment variables may include:
- `OPENAI_API_KEY`


## Testing and validation
After changes:
- Run the smallest relevant check possible
- If the project has no tests yet, at least run the main script when relevant
- Report clearly what was changed
- Report clearly what was run to verify the change
- Mention any assumptions or limitations

## Git safety
- Do not modify git history
- Do not create commits unless explicitly asked
- Do not push to GitHub unless explicitly asked
- Never commit secrets or generated sensitive files

## Communication style
- Be concise and practical
- Explain changes in simple terms
- When writing code, optimize for readability and learning
- If there are multiple valid options, choose the simplest one first

## For this project specifically
When asked to implement a feature, prefer this order:
1. Make it work locally
2. Keep it understandable
3. Keep it safe for secrets
4. Improve structure only if needed
5. Consider deployment later

If adding OCR:
- Start with one image
- Then support multiple images from `uploads/`
- Then generate one `.md` file

If adding hosting later:
- Keep core OCR logic separate from any web framework
- Prefer a plain Python implementation first
- Only introduce FastAPI or another framework when explicitly requested