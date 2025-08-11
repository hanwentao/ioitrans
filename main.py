"""
Translate IOI tasks using Ollama.
"""

import argparse
import pathlib
import pprint
import sys
import tomllib

import ollama
import tqdm


def parse_args():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task", nargs="*", help="task name")
    parser.add_argument(
        "-c",
        "--config",
        type=argparse.FileType("rb"),
        default="config.toml",
        help="configuration file",
    )
    parser.add_argument(
        "-m",
        "--model",
        help="model name",
    )
    parser.add_argument(
        "-t",
        "--think",
        action=argparse.BooleanOptionalAction,
        help="thinking mode",
    )
    parser.add_argument(
        "-s",
        "--seed",
        type=int,
        help="random seed",
    )
    parser.add_argument(
        "-p",
        "--path",
        type=pathlib.Path,
        help="path to tasks",
    )
    parser.add_argument(
        "-d",
        "--dump",
        action="store_true",
        help="dump the effective configuration",
    )
    args = parser.parse_args()
    return args


def load_config():
    """
    Load configuration from file, and override with command-line arguments.
    """
    args = parse_args()
    config = tomllib.load(args.config)
    if args.model is not None:
        config["model"] = args.model
    if args.think is not None:
        config["think"] = args.think
    if args.seed is not None:
        config["seed"] = args.seed
    if args.path is not None:
        config["path"] = args.path
    if args.task is not None:
        config["tasks"] = args.task
    config["dump"] = args.dump
    return config


def translate(config):
    """
    Translate text using the specified model and configuration.
    """
    model = config.get("model", "qwen3")
    think = config.get("think", False)
    seed = config.get("seed", None)  # None for random seed
    path = config.get("path", ".")
    if isinstance(path, str):
        path = pathlib.Path(path)
    prompt_template = config.get(
        "prompt_template", "将以下文本从英语翻译成中文：\n{text}"
    )
    global_prompt = config.get("global_prompt", [])
    global_prompt = "；".join(global_prompt)

    for task in config.get("tasks", [None]):
        if task is not None:
            print(f"Translating task {task}...", file=sys.stderr, flush=True)

        task_prompt = config.get("task_prompt", {}).get(task, [])
        task_prompt = "；".join(task_prompt)

        if task is None:
            text = sys.stdin.read()
        else:
            text = open(path / f"{task}-ISC.md").read()

        prompt = prompt_template.format(
            global_prompt=global_prompt,
            task_prompt=task_prompt,
            text=text,
        )

        stream = ollama.generate(
            model=model,
            think=think,
            options={"seed": seed},
            prompt=prompt,
            stream=True,
        )

        if task is None:
            out = sys.stdout
        else:
            out = open(path / f"{task}-CHN.md", "w")

        for chunk in tqdm.tqdm(stream):
            out.write(chunk.response)


def main():
    """
    Main entry point.
    """
    config = load_config()
    if config["dump"]:
        pprint.pprint(config)
        return
    translate(config)


if __name__ == "__main__":
    sys.exit(main())
