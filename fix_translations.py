import os
import json
import polib
import time
import re
from deep_translator import GoogleTranslator

working_dir = "c:/Users/Nathan Kinda/OneDrive/Desktop/officeease"
with open(os.path.join(working_dir, "found_msgs.json"), "r", encoding="utf-8") as f:
    all_msgs = set(json.load(f))

langs = ["fr", "hi", "my"]

for lang in langs:
    po_path = os.path.join(working_dir, f"locale/{lang}/LC_MESSAGES/django.po")
    if not os.path.exists(po_path): continue
    
    print(f"Loading {po_path}...")
    po = polib.pofile(po_path, encoding='utf-8')
    po.metadata['Content-Type'] = 'text/plain; charset=UTF-8'
    
    translator = GoogleTranslator(source='en', target=lang)
    
    existing_entries = {e.msgid: e for e in po}
    
    # Identify which need translation
    to_translate = []
    for msg in all_msgs:
        entry = existing_entries.get(msg)
        needs_translation = False
        if not entry or not entry.msgstr:
            needs_translation = True
        elif '' in entry.msgstr or 'Ã' in entry.msgstr:
            needs_translation = True
            
        if needs_translation:
            to_translate.append(msg)
            
    print(f"[{lang}] Found {len(to_translate)} strings needing translation out of {len(all_msgs)} total.")
    
    for i, msg in enumerate(to_translate):
        try:
            # Simple HTML protection before sending to Google Translate
            clean_msg = msg.replace('<br>', '\n').replace('<br/>', '\n')
            
            translated = translator.translate(clean_msg)
            
            if translated:
                # Restore HTML protection
                translated = translated.replace('\n', '<br/>')
                
                entry = existing_entries.get(msg)
                if not entry:
                    entry = polib.POEntry(msgid=msg, msgstr=translated, occurrences=[('template', 'auto')])
                    po.append(entry)
                    existing_entries[msg] = entry
                else:
                    entry.msgstr = translated
            print(f"[{lang}] {i+1}/{len(to_translate)} Translated: '{msg[:20]}...' -> '{translated[:20]}...'")
        except Exception as e:
            print(f"[{lang}] Error on {msg}: {e}")
        
    po.save(po_path)
    po.save_as_mofile(po_path.replace('.po', '.mo'))
    print(f"[{lang}] Complete! Saved to disk.")
