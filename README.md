# OpenAI API Scripts

Collection of Python scripts for working with OpenAI APIs:
- **Chat completion** - Simple GPT chat interface
- **Fine-tuning** - Create and manage custom fine-tuned models

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set your OpenAI API key:**
   
   You need an OpenAI API key. Get one from [OpenAI's platform](https://platform.openai.com/api-keys).
   
   Then set it as an environment variable:
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```
   
   Or for a permanent solution, add it to your `~/.zshrc` or `~/.bashrc`:
   ```bash
   echo 'export OPENAI_API_KEY="your-api-key-here"' >> ~/.zshrc
   source ~/.zshrc
   ```

## Usage

### Chat Completion

Run the basic chat script:
```bash
python chat_gpt.py
```

### Fine-Tuning

For detailed fine-tuning instructions, see [FINE_TUNING_README.md](FINE_TUNING_README.md)

Quick start:
```bash
# 1. Prepare your training data in training_data.jsonl
# 2. Start fine-tuning job
python fine_tune.py

# 3. Check status
python check_fine_tune_status.py <job_id>

# 4. Use your fine-tuned model
python use_fine_tuned_model.py <model_name> "Your question"
```

## Troubleshooting

### Error 429 - Insufficient Quota

If you see this error:
```
openai.RateLimitError: Error code: 429 - insufficient_quota
```

**This means your OpenAI account needs credits:**
1. Go to https://platform.openai.com/account/billing
2. Add a payment method
3. Purchase credits or check if you have free trial credits available
4. New accounts sometimes get $5 free credits for 3 months

### Other Common Issues

- **Authentication Error**: Your API key is invalid or expired. Get a new one from the OpenAI dashboard.
- **API Key Not Set**: Make sure you've exported the `OPENAI_API_KEY` environment variable.

## Customization

You can modify the script to:
- Change the prompt by editing the `user_message` variable
- Use different models (e.g., `gpt-4`, `gpt-4-turbo`)
- Adjust `max_tokens` and `temperature` parameters
- Add more conversation context by adding more messages to the `messages` array

