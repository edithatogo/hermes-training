#!/usr/bin/env node
import fs from "node:fs";
import process from "node:process";
import { pathToFileURL } from "node:url";

function parseArgs(argv) {
  const args = {};
  for (let index = 2; index < argv.length; index += 1) {
    const item = argv[index];
    if (!item.startsWith("--")) {
      throw new Error(`Unexpected positional argument: ${item}`);
    }
    const key = item.slice(2).replaceAll("-", "_");
    const next = argv[index + 1];
    if (next === undefined || next.startsWith("--")) {
      args[key] = true;
    } else {
      args[key] = next;
      index += 1;
    }
  }
  return args;
}

function required(args, key) {
  if (!args[key]) {
    throw new Error(`Missing --${key.replaceAll("_", "-")}`);
  }
  return args[key];
}

function buildPrompt(query, doc, instruction) {
  const systemPrompt =
    "Judge whether the Document meets the requirements based on the Query and the Instruct provided. " +
    'Note that the answer can only be "yes" or "no".';
  return (
    `<|im_start|>system\n${systemPrompt}<|im_end|>\n` +
    `<|im_start|>user\n<Instruct>: ${instruction}\n\n<Query>: ${query}\n\n<Document>: ${doc}<|im_end|>\n` +
    "<|im_start|>assistant\n<think>\n\n</think>\n"
  );
}

function softmaxYes(yesLogit, noLogit) {
  const maxLogit = Math.max(yesLogit, noLogit);
  const yesScore = Math.exp(yesLogit - maxLogit);
  const noScore = Math.exp(noLogit - maxLogit);
  return yesScore / (yesScore + noScore);
}

async function main() {
  const args = parseArgs(process.argv);
  const modulePath = process.env.HERMES_TRANSFORMERSJS_MODULE;
  const transformers = modulePath
    ? await import(pathToFileURL(modulePath).href)
    : await import("@huggingface/transformers");
  const { AutoModelForCausalLM, AutoTokenizer, env } = transformers;
  const suitePath = required(args, "suite");
  const modelId = args.model_id || "onnx-community/Qwen3-Reranker-0.6B-ONNX";
  const dtype = args.dtype || "q4";
  const device = args.device || "wasm";
  const maxLength = Number.parseInt(args.max_length || "8192", 10);
  const limitCases = Number.parseInt(args.limit_cases || "1", 10);
  const instruction = args.instruction || "Retrieve relevant memory";
  const cacheDir = args.cache_dir || process.env.TRANSFORMERS_CACHE || process.env.HF_HOME;

  if (cacheDir) {
    env.cacheDir = cacheDir;
  }

  const suite = JSON.parse(fs.readFileSync(suitePath, "utf8"));
  if (!Array.isArray(suite) || suite.length === 0) {
    throw new Error(`${suitePath}: expected non-empty JSON array`);
  }
  const cases = suite.slice(0, Math.max(1, limitCases));

  const startedAt = Date.now();
  const tokenizer = await AutoTokenizer.from_pretrained(modelId);
  const model = await AutoModelForCausalLM.from_pretrained(modelId, {
    dtype,
    device,
  });
  const tokenYes = tokenizer.convert_tokens_to_ids("yes");
  const tokenNo = tokenizer.convert_tokens_to_ids("no");
  if (!Number.isInteger(tokenYes) || !Number.isInteger(tokenNo) || tokenYes < 0 || tokenNo < 0) {
    throw new Error(`${modelId}: tokenizer does not expose yes/no tokens`);
  }

  const rows = [];
  for (const testCase of cases) {
    const candidates = [];
    for (const candidate of testCase.candidates) {
      const prompt = buildPrompt(testCase.query, candidate.text, instruction);
      const inputs = tokenizer(prompt, { truncation: true, max_length: maxLength });
      const output = await model(inputs);
      const seqLen = output.logits.dims[1];
      const vocabSize = output.logits.dims[2];
      const offset = (seqLen - 1) * vocabSize;
      const yesLogit = Number(output.logits.data[offset + tokenYes]);
      const noLogit = Number(output.logits.data[offset + tokenNo]);
      candidates.push({
        id: candidate.id,
        relevant: Boolean(candidate.relevant),
        base_score: Number(candidate.score || 0),
        rerank_score: softmaxYes(yesLogit, noLogit),
      });
    }
    candidates.sort((left, right) => right.rerank_score - left.rerank_score);
    rows.push({
      id: testCase.id,
      category: testCase.category,
      query: testCase.query,
      top_candidate_id: candidates[0].id,
      top1_pass: Boolean(candidates[0].relevant),
      ranked_candidates: candidates,
    });
  }

  if (typeof model.dispose === "function") {
    await model.dispose();
  }

  console.log(
    JSON.stringify(
      {
        ok: true,
        model_id: modelId,
        dtype,
        device,
        max_length: maxLength,
        instruction,
        cache_dir: cacheDir || "",
        token_yes: tokenYes,
        token_no: tokenNo,
        load_and_score_latency_s: (Date.now() - startedAt) / 1000,
        cases: rows,
      },
      null,
      2,
    ),
  );
}

main().catch((error) => {
  console.error(error && error.stack ? error.stack : String(error));
  process.exit(1);
});
