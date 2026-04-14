# Data Summary — TT_Mr_Nghi.ipynb

## Overview
Training data generator for the Vinmec function-call rail.
Goal: produce a dataset of noisy Vietnamese appointment queries paired with
structured `<functioncall>` labels, to fine-tune a slot-extraction SLM.

## Extracted Variables (12 fields)

| # | Field | Type | Notes |
|---|---|---|---|
| 1 | `customer_name` | string | Full name of caller/patient |
| 2 | `customer_phone` | string | Vietnamese mobile number |
| 3 | `medical_department` | string | Clinical dept in Vietnamese |
| 4 | `hospital_name` | string | Vinmec branch / city |
| 5 | `appointment_date` | string | Free-form date expression |
| 6 | `appointment_time` | string | Free-form time expression |
| 7 | `symptoms` | string | Presenting complaint |
| 8 | `customer_dob` | string | Date of birth |
| 9 | `customer_place` | string | Province or address |
| 10 | `relationship` | string | Caller-patient relationship |
| 11 | `cancel_num` | integer | Number of appointments to cancel |
| 12 | `is_yes` | boolean | Explicit yes/no confirmation |

## Data Generation Approach

1. **Seed generation (Gemini API)** — `gemini-pro` prompted to produce realistic Vietnamese
   appointment booking dialogues with ground-truth argument dicts.
2. **Noise injection** — multiple noise types applied to user utterances:
   - Diacritic stripping (plain ASCII Vietnamese)
   - Telex / VNI input method encoding artifacts
   - Character-level swaps and typos
   - Mixed-language (partial English) tokens
3. **Quality filter** — rows containing Chinese characters removed
   (artifacts from LLM outputs), leaving a clean subset.

## Sample Sizes

| Stage | Count |
|---|---|
| Raw generated pairs | 14,643 |
| After Chinese-char filter | 14,471 |
| Removed | 172 |

## Label Format
Each assistant turn uses the Vinmec function-call template:
```
<functioncall> {'name': 'information_extraction', 'arguments': {<field>: <value>, ...}}
```
Absent fields are omitted from the arguments dict (not set to null).

## Purpose
Fine-tune a slot-extraction model (vigpt / Qwen2.5-0.5B-Instruct) to be
**robust against noisy input**, since real call-centre transcripts contain
heavy ASR errors and informal Vietnamese spelling variants.
