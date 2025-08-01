import sys

import ollama
import tqdm

text = sys.stdin.read()
prompt = f'将以下文本从英语翻译成中文：\n{text}'
stream = ollama.generate(
    model='qwen3',
    think=False,
    stream=True,
    prompt=prompt,
)
for chunk in tqdm.tqdm(stream):
    sys.stdout.write(chunk.response)
