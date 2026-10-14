import io
import re
import tokenize

def clean_question(text):
    match = re.search(
        r"^Question:\s*\n(.*?)(?=^Original buggy code:|^Solution explanation:|\Z)",
        text,
        re.S | re.M,
    )
    return (match.group(1) if match else text).strip()

def strip_comments(code):
    tokens = [
        token
        for token in tokenize.generate_tokens(io.StringIO(code).readline)
        if token.type != tokenize.COMMENT
    ]
    cleaned = tokenize.untokenize(tokens)
    return "\n".join(
        line.rstrip() for line in cleaned.splitlines() if line.strip() or not line
    ) + "\n"

def extract_code(reply):
    match = re.search(r"```(?:python)?\s*\n(.*?)```", reply, re.S | re.I)
    return (match.group(1) if match else reply).strip() + "\n"
