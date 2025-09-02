# remove-secrets.py
def replace_line(line):
    # Replace Hugging Face token line with a placeholder
    if b"HUGGING_FACE_TOKEN =" in line:
        return b'HUGGING_FACE_TOKEN = "REDACTED"\n'
    return line

import sys
for filename in sys.argv[1:]:
    with open(filename, "rb") as f:
        lines = f.readlines()
    with open(filename, "wb") as f:
        for line in lines:
            f.write(replace_line(line))
