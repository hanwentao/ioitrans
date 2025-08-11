# ioitrans

本程序使用大语言模型帮助翻译 IOI 题目。

## 依赖

- [Ollama](https://ollama.com/)
- [Python](https://www.python.org/)
- [uv](https://docs.astral.sh/uv/)

## 运行

```bash
git clone https://github.com/hanwentao/ioitrans.git
cd ioitrans
cp config.example.toml config.toml
# Edit config.toml accordingly
uv run main.py <task-name>
```
