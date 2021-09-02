import json
from tqdm import tqdm
import os

directory = os.fsencode("./prep")
output_file_name = "crawled_output.json"
output_dict = dict()
count = 0

for file in tqdm(os.listdir(directory)):
    filename = os.fsdecode(file)
    with open(f"./prep/{filename}", "r") as f:
        for line in f:
            if line.strip():
                json_dict = json.loads(line)
                with open(output_file_name, "a") as f:
                    f.write(json.dumps(json_dict) + "\n")

