# Go Local, Go Trustworthy: Local LLM Demos

This project provides a series of demonstrations showcasing the power, performance, and versatility of running Large Language Models (LLMs) locally. By keeping data on-premise, we can build powerful, trustworthy, and private AI applications.

The demos use a local `llama.cpp` server to run various quantized models and compare their capabilities on different tasks.

### Demo 1: Knowledge Graph Extraction & Performance Benchmark

This demo compares the performance of three different models on a structured data extraction task. Each model is prompted to analyze a block of text and generate a knowledge graph from it in a structured JSON format.

* **Task**: Text-to-Knowledge Graph
* **Metric**: Performance (tokens/second) and qualitative analysis of the generated graph.
* **Models**:
  * `Mistral Small 3.1` (24B, Q4 quantized)
  * `Gemma3` (27B, Q4 quantized)
  * `Qwen3` (32B, Q4 quantized)

### Demo 2: Performance Boost with Speculative Decoding

This demo repeats the knowledge graph extraction task from Demo 1 but enables speculative decoding to showcase the significant performance improvements possible with this technique. A smaller "draft" model is used to generate text drafts, which are then validated by the larger model.

* **Task**: Text-to-Knowledge Graph (with enhanced performance)
* **Metric**: Comparison of tokens/second with and without speculative decoding.
* **Models**:
  * `Mistral Small 3.1` (24B, Q4) with a **0.5B draft model**.
  * `Qwen3` (32B, Q4) with a **0.6B draft model**.
  * `Gemma3` (27B, Q4) with a **1B draft model**.

### Demo 3: Multimodal OCR to Structured Markdown

This demo showcases the multimodal capabilities of local LLMs by performing an Optical Character Recognition (OCR) task. A model analyzes an image and transcribes its content into clean, structured Markdown.

* **Task**: Image-to-Structured Text (OCR)
* **Model**:
  * `Mistral Small 3.2` (24B, Q6)