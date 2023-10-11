from glob import glob
files = glob("nas/mint-bench/data/outputs/**/theoremqa/results.jsonl", recursive=True)
import json
for file in files:
    json_strs = open(file).readlines()
    good_jsons = []
    for json_str in json_strs:
        json_obj = json.loads(json_str)
        possible_solutions = [i['content'].split('<solution>')[-1].split('</solution>')[0].strip() for i in json_obj['state']['history']]
        possible_solutions = [i for i in possible_solutions if i in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']]
        if len(possible_solutions) == 0:
            good_jsons.append(json_str)
    # dump back
    with open(file, 'w') as f:
        for json_str in good_jsons:
            f.write(json_str)
