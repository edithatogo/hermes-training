FROM pytorch/pytorch:2.7.1-cuda12.6-cudnn9-runtime

ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    LM_EVAL_TIMEOUT_S=21600 \
    LM_EVAL_OUTPUT_DIR=/results/lm-eval-output \
    LM_EVAL_RESULT_JSON=/results/summary.json

WORKDIR /opt/hermes-scorecard

RUN python -m pip install --no-cache-dir --upgrade \
    "lm_eval[hf]" \
    "transformers>=4.56,<5" \
    peft \
    bitsandbytes \
    safetensors \
    accelerate \
    huggingface_hub

COPY scripts/hf_jobs_peft_lm_eval_selected.py /opt/hermes-scorecard/run_scorecard.py

RUN mkdir -p /results

CMD ["python", "/opt/hermes-scorecard/run_scorecard.py"]
