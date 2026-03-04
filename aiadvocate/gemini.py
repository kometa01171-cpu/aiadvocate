# pip install google-genai

import os
from google import genai
from google.genai import types

# API KEY ni ENV orqali berish xavfsizroq
os.environ["GOOGLE_API_KEY"] = "AIzaSyAcnhCmq5MJVL8bDgRJ7eADjDBUCsn7QEY"

client = genai.Client()

model = "gemini-2.5-flash-lite"

# =========================+
# SYSTEM INSTRUCTION
# =========================
system_instruction = types.Content(
    role="system",
    parts=[
        types.Part.from_text(
            text="You are a professional AI assistant. "
                 "Always give clear, short and structured answers. "
                 "If system uploads a file, analyze it carefully before answering."
        )
    ],
)

while True:
    user_input = input("Birnima: ")

    # =========================
    # FILE UPLOAD (optional)
    # =========================
    file_path = input("File yo'li (bo'sh qoldirsangiz skip): ")

    file_part = None
    if file_path.strip() != "":
        uploaded_file = client.files.upload(file=file_path)
        file_part = types.Part.from_uri(
            file_uri=uploaded_file.uri,
            mime_type=uploaded_file.mime_type,
        )

    # =========================
    # USER CONTENT
    # =========================
    parts = [types.Part.from_text(text=user_input)]

    if file_part:
        parts.append(file_part)

    user_content = types.Content(
        role="user",
        parts=parts,
    )

    # =========================
    # TOOLS
    # =========================
    tools = [
        types.Tool(
            googleSearch=types.GoogleSearch()
        ),
    ]

    # =========================
    # CONFIG
    # =========================
    generate_content_config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        tools=tools,
    )

    # =========================
    # STREAM RESPONSE
    # =========================
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=[user_content],
        config=generate_content_config,
    ):
        print(chunk.text, end="")

    print("\n")