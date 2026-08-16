import json

with open(r"C:\Users\nihar\.gemini\antigravity\brain\e36329fd-eee3-482b-ad15-fc583f746f17\.system_generated\logs\transcript.jsonl", 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line)
        if obj.get('source') == 'USER_EXPLICIT':
            content = obj.get('content', '')
            if 'http' in content or 'pinterest' in content:
                print(f"Step {obj.get('step_index')}: {content}")
