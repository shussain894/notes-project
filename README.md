# Image To Markdown

This project reads image files from `uploads/`, sends each one to `gpt-4.1` using the OpenAI API key in `.env`, and writes a Markdown file into `output/`.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Add your API key to `.env`:

```env
OPENAI_API_KEY=your_key_here
```

## Usage

1. Put images in `uploads/`.
2. Run:

```bash
python3 src/main.py
```

Each supported image (`.png`, `.jpg`, `.jpeg`, `.webp`, `.gif`, `.heic`, `.heif`) becomes a matching `.md` file in `output/`.

HEIC and HEIF images are converted to PNG in memory before being sent to the API.
