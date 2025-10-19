# OpenAI Fine-Tuning Guide

This guide explains how to fine-tune GPT models using the OpenAI API.

## What is Fine-Tuning?

Fine-tuning lets you customize OpenAI models to better fit your specific use case by training them on your own examples. This can improve:
- Response quality for domain-specific tasks
- Consistency in tone and style
- Following specific formats or instructions
- Performance on specialized knowledge

## Files Included

1. **`fine_tune.py`** - Creates and starts a fine-tuning job
2. **`check_fine_tune_status.py`** - Monitors fine-tuning job progress
3. **`use_fine_tuned_model.py`** - Uses your fine-tuned model
4. **`training_data.jsonl`** - Example training data (customize this!)

## Prerequisites

1. OpenAI API key with billing enabled
2. Training data in JSONL format
3. Sufficient credits (fine-tuning costs vary by model and data size)

## Training Data Format

Your training data must be in JSONL format (JSON Lines), with each line containing a conversation:

```json
{"messages": [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}
{"messages": [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}
```

### Best Practices for Training Data:

- **Minimum examples**: At least 10 examples (50-100+ recommended)
- **Quality over quantity**: High-quality examples are more important than many poor ones
- **Consistency**: Keep system messages and formatting consistent
- **Diversity**: Cover different variations of similar queries
- **Balance**: Include various types of questions/responses

## Step-by-Step Guide

### Step 1: Prepare Your Training Data

Edit `training_data.jsonl` with your own examples:

```bash
# Each line should be valid JSON with a "messages" array
{"messages": [{"role": "system", "content": "You are X"}, {"role": "user", "content": "Y"}, {"role": "assistant", "content": "Z"}]}
```

### Step 2: Start Fine-Tuning Job

```bash
python fine_tune.py
```

This will:
1. Upload your training file
2. Wait for file processing
3. Create and start the fine-tuning job
4. Display the job ID

**Output example:**
```
[1/3] Uploading training file: training_data.jsonl
✓ File uploaded successfully!
  File ID: file-abc123

[2/3] Waiting for file to be processed...
✓ File processed successfully!

[3/3] Creating fine-tuning job...
✓ Fine-tuning job created successfully!

Job ID: ftjob-xyz789
Model: gpt-3.5-turbo
Status: queued
```

### Step 3: Monitor Progress

Check your job status:

```bash
# Check specific job
python check_fine_tune_status.py ftjob-xyz789

# List all jobs
python check_fine_tune_status.py --list
```

Fine-tuning typically takes:
- **GPT-3.5-turbo**: 10-30 minutes for small datasets
- **GPT-4**: Longer, depending on data size

### Step 4: Use Your Fine-Tuned Model

Once the job is complete, you'll get a model name like:
```
ft:gpt-3.5-turbo-0125:my-org:custom-model:9ABcDEf
```

Use it:

```bash
python use_fine_tuned_model.py "ft:gpt-3.5-turbo-0125:my-org:custom-model:9ABcDEf" "Your question here"
```

Or integrate it into your code:

```python
response = client.chat.completions.create(
    model="ft:gpt-3.5-turbo-0125:my-org:custom-model:9ABcDEf",
    messages=[
        {"role": "user", "content": "Your question"}
    ]
)
```

## Available Models for Fine-Tuning

- **gpt-3.5-turbo** (recommended for most use cases)
- **gpt-4o-mini-2024-07-18** (faster, cheaper)
- **gpt-4** series (more capable, more expensive)

## Costs

Fine-tuning costs include:
1. **Training cost**: Based on number of tokens in training data × epochs
2. **Usage cost**: Using the fine-tuned model (typically higher than base models)

Example pricing (as of 2024):
- GPT-3.5-turbo training: ~$0.008 per 1K tokens
- GPT-3.5-turbo usage: ~$0.012 per 1K input tokens

Check current pricing: https://openai.com/pricing

## Tips for Success

1. **Start small**: Test with 10-20 examples first
2. **Validate quality**: Review your training examples carefully
3. **Iterate**: Compare fine-tuned vs base model performance
4. **Monitor costs**: Track your spending in the OpenAI dashboard
5. **Use validation data**: Include a validation set to prevent overfitting

## Troubleshooting

### "Training data validation failed"
- Check JSONL format (each line must be valid JSON)
- Ensure all required fields are present
- Verify message roles are correct (system, user, assistant)

### Job failed during training
- Check job events: `python check_fine_tune_status.py <job_id>`
- Review error messages in the OpenAI dashboard
- Ensure sufficient credits

### Poor model performance
- Add more diverse training examples
- Increase training epochs (default is 3)
- Check for data quality issues

## Additional Resources

- [OpenAI Fine-Tuning Guide](https://platform.openai.com/docs/guides/fine-tuning)
- [Fine-Tuning Dashboard](https://platform.openai.com/finetune)
- [API Reference](https://platform.openai.com/docs/api-reference/fine-tuning)

## Customizing Hyperparameters

Edit `fine_tune.py` to adjust training parameters:

```python
fine_tuning_job = client.fine_tuning.jobs.create(
    training_file=training_file.id,
    model="gpt-3.5-turbo",
    hyperparameters={
        "n_epochs": 3,  # Increase for more training
        # Add other hyperparameters as needed
    }
)
```

Common adjustments:
- **n_epochs**: Number of training passes (1-50, default auto)
- More epochs = more training, but risk of overfitting

