# SLM User Modeling Research
This project aims to understand how Small Language Models (SLMs) can implicitly 
model user attributes (such as gender) from their writing style, without explicit
cues. We used the [**Gemma-3-270m**](https://huggingface.co/google/gemma-3-270m) model and the [**Blog Authorship Corpus**](https://huggingface.co/datasets/barilan/blog_authorship_corpus)
(~612K posts with gender labels).

## Structure
This project goes through diffrent steps/phases (all available in the `notebook/` folder):
- Phase 0 : Dataset analysis
- Phase 1 : Dataset preparation
- Phase 2 : Linear probing
- Phase 3 : Token analysis and importance
- Phase 4 : Activation steering

## Results

### Phase 0: Exploratory Data Analysis (EDA)

The dataset analysis revealed:
- ~680K blog posts with author metadata
- Balanced distribution between male and female authors
- After cleaning (removing missing values, too short/long texts, special characters): **612,203 samples**

### Phase 1: Data Preparation

We created a "hard" dataset by filtering out texts containing trivial gender markers:
- Removal of explicit pronouns (I am a man/woman, my husband/wife...)
- Removal of gendered first names
- Result: a dataset where gender cannot be guessed from obvious lexical cues

### Phase 2: Linear Probing

**Method**: Training linear classifiers (Logistic Regression) on the hidden states of each model layer to predict the author's gender.

**Key Results**:
| Layer | Accuracy |
|-------|----------|
| Layer 0 (embeddings) | ~70% |
| Middle layers (1-5) | **50-80%** |
| Middle layers (6-18) | **40-60%** |
| Best layer | **~80%** |

> **Conclusion**: The model encodes gender-correlated information across its layers, with accuracy significantly above chance (50%), but remains subtle (~50-60%).

### Phase 3: Token Analysis

**Methods used**:
1. **Integrated Gradients**: Measures the importance of each input token for the prediction
2. **Attention Rollout**: Aggregates attention weights across layers

**Results**:
- **No specific token** is systematically used by the LLM to interpret gender
- The most influential tokens vary considerably between samples
- The gender signal appears to be **distributed** rather than concentrated on specific keywords

### Phase 4: Activation Steering

**Objective**: Verify whether the identified gender representations are causally relevant by intervening on the model's activations.

**Method**:
1. Compute the "gender direction vector": $`\vec{d}_{gender} = \vec{\mu}_{male} - \vec{\mu}_{female}`$
2. Inject this vector during generation (steering)
3. Measure the effect on pronoun usage

**Quantitative Results (female pronoun ratio)**:

| Condition | Male pronouns | Female pronouns | Female ratio |
|-----------|---------------|-----------------|--------------|
| Baseline | - | - | ~50% |
| Male steering (+3) | &uarr; | &darr; | **&darr;** (expected ✓) |
| Female steering (-3) | &darr; | &uarr; | **&uarr;** (expected ✓) |
| Female steering (-6) | &darr;&darr; | ↑↑ | **&uarr;&uarr;** (expected ✓) |
| Male steering (+6) | - | - | Reversed effects (out of distribution) |

**Key Observations**:
- Moderate steering (±3) works in the expected direction
- Strong steering (+6) produces reversed effects, suggesting activations are pushed outside the training distribution
- Asymmetry: female-direction steering works at all intensities

### General Conclusions

| Aspect | Conclusion |
|--------|------------|
| **Gender encoding** |  The model implicitly encodes gender information (accuracy ~65-67%) |
| **Signal nature** | Subtle and distributed - no specific "revealing" tokens |
| **Causality** |  The identified representations causally influence generation |
| **Intervention** | Activation steering can modify behavior, but requires fine calibration |

**Implications**:
- **Privacy**: LLMs can reveal demographic attributes from writing style
- **Fairness**: Implicit gender modeling could lead to differential treatment
- **Mitigation**: Steering techniques offer a potential approach to reduce these biases at inference time


## Setup
Make sure to create/have a python environment with the requirements inside `requirements.txt`:
```bash
pip install -r requirements.txt
```

And also dont forget to download the data. A CSV file will be created in the `data/` folder:
```bash
./download_data.sh
```

## Env variable
At the root of the project, make sure you have a `.env` that follows the `.env.example` 
file format. This file only contain an Hugging Face Toekn to allow us to see the
model weights. 

To setup this token, go to [Hugging Face](https://huggingface.co/). Then go to your
Profile `Settings > Access Tokens`. From there create a `Read` access token and
store the value of your token inside the `.env` file.
