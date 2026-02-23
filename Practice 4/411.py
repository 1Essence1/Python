import json

def apply_patch(source, patch):
    if not isinstance(patch, dict):
        return patch
    
    if not isinstance(source, dict):
        source = {}

    for key, value in patch.items():
        if value is None:
            if key in source:
                del source[key]
        elif isinstance(value, dict) and key in source and isinstance(source[key], dict):
            source[key] = apply_patch(source[key], value)
        else:
            source[key] = value
            
    return source

source_json = json.loads(input())
patch_json = json.loads(input())

result = apply_patch(source_json, patch_json)

print(json.dumps(result, sort_keys=True, separators=(',', ':')))