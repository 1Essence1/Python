import json

def find_diffs(obj1, obj2, path=""):
    diffs = []
    
    all_keys = set()
    if isinstance(obj1, dict): all_keys.update(obj1.keys())
    if isinstance(obj2, dict): all_keys.update(obj2.keys())
    
    for key in sorted(all_keys):
        new_path = f"{path}.{key}" if path else key
        
        val1 = obj1.get(key, "<missing>") if isinstance(obj1, dict) else "<missing>"
        val2 = obj2.get(key, "<missing>") if isinstance(obj2, dict) else "<missing>"

        if val1 == "<missing>" or val2 == "<missing>":
            diffs.append(format_diff(new_path, val1, val2))
            
        elif isinstance(val1, dict) and isinstance(val2, dict):
            diffs.extend(find_diffs(val1, val2, new_path))
            
        elif val1 != val2:
            diffs.append(format_diff(new_path, val1, val2))
            
    return diffs

def format_diff(path, v1, v2):
    s1 = "<missing>" if v1 == "<missing>" else json.dumps(v1, separators=(',', ':'), sort_keys=True)
    s2 = "<missing>" if v2 == "<missing>" else json.dumps(v2, separators=(',', ':'), sort_keys=True)
    return f"{path} : {s1} -> {s2}"

json1 = json.loads(input())
json2 = json.loads(input())

results = find_diffs(json1, json2)

if not results:
    print("No differences")
else:
    for line in sorted(results):
        print(line)
