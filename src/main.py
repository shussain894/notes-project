from __future__ import annotations

import base64
import io
import mimetypes
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from openai import APIConnectionError, APIStatusError, BadRequestError, AuthenticationError
from pillow_heif import read_heif, register_heif_opener


UPLOADS_DIR = Path("uploads")
OUTPUT_DIR = Path("output")
SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
HEIC_EXTENSIONS = {".heic", ".heif"}
MODEL_NAME = "gpt-4.1"
PROMPT = """Convert this image into clean Markdown.

Requirements:
- Preserve the document structure as faithfully as possible.
- Use Markdown headings, lists, tables, and emphasis when appropriate.
- If text is unclear, make the best reasonable guess and keep going.
- Return only the Markdown content with no code fences or commentary.
"""

register_heif_opener()


def encode_bytes_as_data_url(image_bytes: bytes, mime_type: str) -> str:
    encoded = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"


def load_image_bytes(image_path: Path) -> tuple[bytes, str]:
    if image_path.suffix.lower() in HEIC_EXTENSIONS:
        heif_file = read_heif(image_path)
        converted = heif_file.to_pillow().convert("RGB")
        buffer = io.BytesIO()
        converted.save(buffer, format="PNG")
        return buffer.getvalue(), "image/png"

    mime_type, _ = mimetypes.guess_type(image_path.name)
    if not mime_type:
        raise ValueError(f"Could not determine MIME type for {image_path}")

    return image_path.read_bytes(), mime_type


def find_images(directory: Path) -> list[Path]:
    return sorted(
        path
        for path in directory.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS.union(HEIC_EXTENSIONS)
    )


def image_to_markdown(client: OpenAI, image_path: Path) -> str:
    image_bytes, mime_type = load_image_bytes(image_path)
    image_data_url = encode_bytes_as_data_url(image_bytes, mime_type)

    response = client.responses.create(
        model=MODEL_NAME,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": PROMPT},
                    {"type": "input_image", "image_url": image_data_url},
                ],
            }
        ],
    )
    return response.output_text.strip()


def main() -> None:
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is missing from .env")

    if not UPLOADS_DIR.exists():
        raise RuntimeError(f"Missing uploads directory: {UPLOADS_DIR}")

    images = find_images(UPLOADS_DIR)
    if not images:
        print("No supported image files found in uploads/")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    client = OpenAI(api_key=api_key)

    for image_path in images:
        try:
            print(f"Processing {image_path.name}...")
            markdown = image_to_markdown(client, image_path)
            output_path = OUTPUT_DIR / f"{image_path.stem}.md"
            output_path.write_text(markdown + "\n", encoding="utf-8")
            print(f"Saved {output_path}")

        except AuthenticationError as e:
            print(f"AUTH ERROR for {image_path.name}: {e}")
        except BadRequestError as e:
            print(f"BAD REQUEST for {image_path.name}: {e}")
        except APIConnectionError as e:
            print(f"CONNECTION ERROR for {image_path.name}: {e}")
        except APIStatusError as e:
            print(f"API STATUS ERROR for {image_path.name}: status={e.status_code}, response={e.response}")
        except Exception as e:
            print(f"UNEXPECTED ERROR for {image_path.name}: {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()