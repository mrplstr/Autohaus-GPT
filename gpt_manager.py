import json
import os

GPT_FILE = "data/gpts.json"

def load_gpts():
    if not os.path.exists(GPT_FILE):
        return []
    with open(GPT_FILE, "r") as f:
        return json.load(f)

def save_gpts(gpts):
    with open(GPT_FILE, "w") as f:
        json.dump(gpts, f, indent=2)

def add_gpt(name, system_prompt, temperature, max_tokens):
    gpts = load_gpts()
    new_id = max([g["id"] for g in gpts], default=0) + 1
    gpts.append({
        "id": new_id,
        "name": name,
        "system_prompt": system_prompt,
        "temperature": temperature,
        "max_tokens": max_tokens
    })
    save_gpts(gpts)

def delete_gpt(gpt_id):
    gpts = load_gpts()
    gpts = [g for g in gpts if g["id"] != gpt_id]
    save_gpts(gpts)
