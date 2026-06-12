# Harmonic Hermes Current Release Scan

This scan adds the Harmonic reasoning backbone and agentic fine-tune family to
the Hermes local-runtime radar:

- `DJLougen/Harmonic-9B`
- `DJLougen/Harmonic-Hermes-9B-GGUF`
- `mradermacher/Harmonic-Hermes-9B-i1-GGUF`

## What Changed

- Harmonic-9B is the reasoning backbone and the direct base for the agentic
  fine-tune.
- Harmonic-Hermes-9B is the Stage 2 tool-calling / agent model built on top of
  that backbone.
- The GGUF paths make the model usable in Ollama, LM Studio, and llama.cpp
  workflows.

## Practical Reading

- Treat Harmonic-9B as the base teacher/backbone.
- Treat Harmonic-Hermes-9B-GGUF as the easiest local runtime validation lane.
- Treat Harmonic-Hermes-9B-i1-GGUF as the alternate Mac runtime comparison lane.

## Evidence Notes

Verified from current Hugging Face model pages:

- [Harmonic-9B](https://huggingface.co/DJLougen/Harmonic-9B)
- [Harmonic-Hermes-9B-GGUF](https://huggingface.co/DJLougen/Harmonic-Hermes-9B-GGUF)
- [Harmonic-Hermes-9B-i1-GGUF](https://huggingface.co/mradermacher/Harmonic-Hermes-9B-i1-GGUF)

## Result

The radar now includes a new Hermes-style local runtime lane built from an
open reasoning backbone plus a direct agentic fine-tune.
