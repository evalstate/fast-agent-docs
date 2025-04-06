## Providers

### Anthropic

### OpenAI

fast-agent supports OpenAI gpt-4o and o1/o3 series models.

### DeepSeek

### Generic OpenAI LLM

!!! warning

    Use the Generic Provider to connect to OpenAI compatible models (including Ollama).
    Tool Calling and other modalities for generic models are not included in the e2e test suite, and should be used at your own risk.

Models prefixed with `generic` will use a generic OpenAI endpoint, with the defaults configured to work with Ollama. For example, to run with Llama 3.2 latest you can specify `generic.llama3.2:latest`. As with other models `base_url` can be overridden. The associated API key environment variable is `GENERIC_API_KEY`, with `ollama` used as the default.
