# OpenAI Text-to-Speech (TTS) Guide

Convert text to natural-sounding speech using OpenAI's TTS API.

## Features

- Multiple voice options (6 voices: male, female, neutral)
- High-quality audio output
- Support for long texts (automatic chunking)
- Multiple audio formats (MP3, Opus, AAC, FLAC)
- Two quality levels (standard and HD)

## Files Included

1. **`text_to_speech.py`** - Convert text directly from command line
2. **`text_to_speech_file.py`** - Convert text from a file (handles long texts)
3. **`sample_text.txt`** - Example text file for testing

## Quick Start

### Convert Simple Text

```bash
python text_to_speech.py "Hello, world!"
```

This creates `speech.mp3` in the current directory.

### Convert Text from File

```bash
python text_to_speech_file.py sample_text.txt
```

This creates `speech_output.mp3` from the file content.

## Available Voices

OpenAI TTS offers 6 different voices:

| Voice | Description | Best For |
|-------|-------------|----------|
| **alloy** | Neutral | General purpose |
| **echo** | Male | Professional content |
| **fable** | Neutral | Storytelling |
| **onyx** | Male, deep | Narration |
| **nova** | Female | Clear, friendly |
| **shimmer** | Female, soft | Gentle content |

Try different voices to find the one that fits your use case!

## Usage Examples

### Basic Usage

```bash
# Simple text with default settings
python text_to_speech.py "Hello, this is a test"

# Custom output filename
python text_to_speech.py "Hello!" greeting.mp3

# Choose a specific voice
python text_to_speech.py "Hello!" greeting.mp3 nova

# Use HD quality model
python text_to_speech.py "Hello!" greeting.mp3 nova tts-1-hd
```

### Converting Files

```bash
# Convert a text file
python text_to_speech_file.py article.txt

# Custom output and voice
python text_to_speech_file.py article.txt audiobook.mp3 onyx

# HD quality for best audio
python text_to_speech_file.py article.txt audiobook.mp3 nova tts-1-hd
```

### Compare Voices

Create samples of each voice:

```bash
python text_to_speech.py "This is the alloy voice" alloy_sample.mp3 alloy
python text_to_speech.py "This is the echo voice" echo_sample.mp3 echo
python text_to_speech.py "This is the fable voice" fable_sample.mp3 fable
python text_to_speech.py "This is the onyx voice" onyx_sample.mp3 onyx
python text_to_speech.py "This is the nova voice" nova_sample.mp3 nova
python text_to_speech.py "This is the shimmer voice" shimmer_sample.mp3 shimmer
```

## Playing Audio Files

After generating audio, play it using:

**macOS:**
```bash
afplay speech.mp3
```

**Linux:**
```bash
mpg123 speech.mp3
# or
mpv speech.mp3
```

**Windows:**
```bash
start speech.mp3
```

## Models

### tts-1 (Standard)
- Faster processing
- Lower latency
- Good quality
- **Cost:** ~$0.015 per 1K characters

### tts-1-hd (High Definition)
- Higher quality audio
- Slightly slower
- Better for professional use
- **Cost:** ~$0.030 per 1K characters

## Audio Formats

Supported output formats:
- **MP3** (default) - Most compatible
- **Opus** - Best for streaming
- **AAC** - Apple devices
- **FLAC** - Lossless quality

```bash
# Generate different formats
python text_to_speech.py "Test" output.mp3
python text_to_speech.py "Test" output.opus
python text_to_speech.py "Test" output.aac
python text_to_speech.py "Test" output.flac
```

## Limitations

- **Character limit:** 4096 characters per request
  - `text_to_speech_file.py` automatically handles this by splitting text
- **Language support:** Works best with English, but supports multiple languages
- **Real-time factor:** Generates faster than real-time playback

## Use Cases

### 1. Audiobook Creation
```bash
python text_to_speech_file.py chapter1.txt chapter1.mp3 onyx tts-1-hd
```

### 2. Accessibility
Convert articles or documents for visually impaired users:
```bash
python text_to_speech_file.py article.txt article_audio.mp3 nova
```

### 3. Language Learning
Create pronunciation guides:
```bash
python text_to_speech.py "How do you pronounce this?" pronunciation.mp3
```

### 4. Podcasts & Videos
Generate narration for content:
```bash
python text_to_speech_file.py script.txt narration.mp3 echo tts-1-hd
```

### 5. Voice Notifications
Create audio alerts:
```bash
python text_to_speech.py "Your build is complete" notification.mp3 alloy
```

## Tips for Best Results

### 1. Text Formatting
- Use proper punctuation for natural pauses
- Add commas for breathing room
- Use periods for clear sentence breaks

### 2. Numbers and Dates
- Write numbers as words: "twenty-five" instead of "25"
- Spell out dates: "January first" instead of "1/1"

### 3. Acronyms
- Add periods: "N.A.S.A." instead of "NASA"
- Or spell out: "National Aeronautics and Space Administration"

### 4. Emphasis
- Use punctuation: "This is amazing!" vs "This is amazing."
- Capitalize for acronyms but not for emphasis

### 5. Long Texts
- Use the file converter for texts over 1000 characters
- Break very long content into chapters/sections
- The file converter automatically handles chunking

## Cost Estimation

TTS costs are based on character count:

| Model | Cost per 1K chars | 1 minute of audio (~150 words) |
|-------|-------------------|--------------------------------|
| tts-1 | $0.015 | ~$0.015 |
| tts-1-hd | $0.030 | ~$0.030 |

**Example costs:**
- Short message (100 chars): < $0.01
- Article (2000 chars): $0.03 - $0.06
- Audiobook chapter (20,000 chars): $0.30 - $0.60

Check current pricing: https://openai.com/pricing

## Troubleshooting

### Audio Quality Issues
- Use `tts-1-hd` for better quality
- Try different voices
- Check your source text formatting

### File Size Large
- MP3 files are typically 1-2 MB per minute
- Use Opus format for smaller files
- Use AAC for a good balance

### Pronunciation Problems
- Spell out problematic words phonetically
- Add commas for pauses
- Use periods to separate ideas

### Long Text Not Working
- Use `text_to_speech_file.py` instead of `text_to_speech.py`
- The file version automatically chunks long texts
- Max 4096 characters per API call

## Advanced Examples

### Create an Audiobook from Multiple Chapters

```bash
#!/bin/bash
# Convert multiple chapters
for i in {1..10}; do
    python text_to_speech_file.py "chapter$i.txt" "chapter$i.mp3" onyx tts-1-hd
done

# Combine with ffmpeg (if installed)
# ffmpeg -i "concat:chapter1.mp3|chapter2.mp3|..." output.mp3
```

### Batch Process Multiple Files

```bash
#!/bin/bash
# Convert all .txt files in a directory
for file in *.txt; do
    output="${file%.txt}.mp3"
    python text_to_speech_file.py "$file" "$output" nova
done
```

## Integration with Other Tools

### Use in Python Scripts

```python
from openai import OpenAI

client = OpenAI(api_key="your-key")

response = client.audio.speech.create(
    model="tts-1",
    voice="nova",
    input="Your text here"
)

response.stream_to_file("output.mp3")
```

### Combine with Chat Completion

Generate text with GPT, then convert to speech:

```bash
# Generate story with GPT (chat_gpt.py output)
# Then convert to speech
python text_to_speech.py "$(python chat_gpt.py)" story.mp3 fable
```

## Additional Resources

- [OpenAI TTS Documentation](https://platform.openai.com/docs/guides/text-to-speech)
- [API Reference](https://platform.openai.com/docs/api-reference/audio)
- [Pricing](https://openai.com/pricing)

## Legal & Ethical Considerations

- **Voice cloning:** Don't use TTS to impersonate real people
- **Copyright:** Ensure you have rights to convert the text
- **Disclosure:** Consider disclosing AI-generated audio to listeners
- **Accessibility:** Great for making content more accessible

## Quality Comparison

| Aspect | tts-1 | tts-1-hd |
|--------|-------|----------|
| Speed | ⚡⚡⚡ Fast | ⚡⚡ Slower |
| Quality | ⭐⭐⭐ Good | ⭐⭐⭐⭐ Excellent |
| Cost | 💰 Lower | 💰💰 Higher |
| Use Case | Drafts, testing | Final production |

