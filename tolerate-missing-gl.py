#!/usr/bin/env python3
"""tolerate-missing-gl.py — make leonkasovan/gl v3.2/gles2 loader tolerant.

iOS EAGL tops out at GLES 3.0, so every 3.1/3.2 core entry point resolves
to NULL and Init() aborts on the first one (glActiveShaderProgram). The
engine never CALLS any of them (verified: no 3.1+ gl.* references in
Ikemen-GO src outside dormant shadow paths), so dropping the eager
nil-checks is safe: missing functions stay nil, called ones resolve.

Idempotent. Run from the repo root.
"""
import re
from pathlib import Path

P = Path("v3.2/gles2/package.go")
text = P.read_text()
pat = re.compile(r'\n\tif gp\w+ == nil \{\n\t\treturn errors\.New\("gl\w+"\)\n\t\}')
text, n = pat.subn("", text)
print(f"removed {n} nil-checks")
if "errors." not in text:
    text = text.replace('\t"errors"\n', "")
    print("dropped now-unused errors import")
P.write_text(text)
print("OK")
