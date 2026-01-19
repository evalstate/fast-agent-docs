# Getting Started

## Install or upgrade

```bash
uv tool install -U fast-agent-mcp
```

If you have multiple Python versions installed, pin the one required by fast-agent:

```bash
uv tool install -U fast-agent-mcp --python 3.13.5
```

## Run

```bash
fast-agent go
```

## Instruction file

```bash
fast-agent go -i prompt.md
fast-agent go -i https://gist.github.com/....
```

## Model override

```bash
fast-agent go --model sonnet
```
