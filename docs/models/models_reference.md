---
title: Models Reference
---

# Models Reference

This page lists models that expose structured output, reasoning, text
verbosity, tokenization modality support, and built-in Anthropic web tools
(`web_search` / `web_fetch`) where available. Model names prefer aliases where
available; otherwise the table shows the minimal model string (including
provider prefix when required). The provider column reflects the default
provider used by fast-agent (models may become available with multiple
providers in the future).

Anthropic-on-Vertex is exposed as a separate provider using model strings such
as `anthropic-vertex.claude-sonnet-4-6`. With `google.vertex_ai.enabled`, the
native Google provider can also pass Vertex partner model ids such as
`google.claude-sonnet-4-6` through unchanged. The table below still shows the
default provider for each base model id; Vertex-specific routes are documented
on [LLM Providers](llm_providers.md#anthropic-on-vertex-ai).

--8<-- "_generated/models_reference.md"
