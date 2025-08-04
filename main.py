import json
import sys

import ollama
import tqdm

task = sys.argv[1] if len(sys.argv) > 1 else None

config = json.load(open('config.json'))
model = config.get('model', 'qwen3')
think = config.get('think', False)
seed = config.get('seed', None)  # None for random seed
prompt_template = config.get('prompt_template', '将以下文本从英语翻译成中文：\n{text}')
global_prompt = config.get('global_prompt', [])
task_prompt = config.get('task_prompt', {}).get(task, [])

global_prompt = '；'.join(global_prompt)
task_prompt = '；'.join(task_prompt)

if task is None:
    text = sys.stdin.read()
else:
    text = open(f'{task}-ISC.md').read()

prompt = prompt_template.format(
    global_prompt=global_prompt,
    task_prompt=task_prompt,
    text=text,
)

stream = ollama.generate(
    model=model,
    think=think,
    options={'seed': seed},
    prompt=prompt,
    stream=True,
)

if task is None:
    out = sys.stdout
else:
    out = open(f'{task}-CHN.md', 'w')

for chunk in tqdm.tqdm(stream):
    out.write(chunk.response)
