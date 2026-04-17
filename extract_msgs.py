import os
import re
import json

trans_re = re.compile(r'{%\s*trans\s+(?P<quote>[\'"`])(?P<text>.*?)(?P=quote)\s*%}')
msgs = set()

for root, _, files in os.walk("."):
    if ".venv" in root or "locale" in root: continue
    for f in files:
        if f.endswith(".html"):
            with open(os.path.join(root, f), "r", encoding="utf-8") as file:
                for match in trans_re.finditer(file.read()):
                    msgs.add(match.group('text'))

with open("found_msgs.json", "w", encoding="utf-8") as f:
    json.dump(list(msgs), f, indent=4, ensure_ascii=False)

try:
    import polib
    print("polib mapped")
    po = polib.pofile("locale/fr/LC_MESSAGES/django.po")
    existing_fr = {e.msgid for e in po}
    print(f"Missing from FR: {len(msgs - existing_fr)}")
except Exception as e:
    print(f"Error checking PO: {e}")
