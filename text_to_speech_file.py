#!/usr/bin/env python3
"""
Script to convert text from a file to speech using OpenAI's TTS API.
Useful for converting long texts, articles, or documents to audio.
"""

import os
import sys
from pathlib import Path
from openai import OpenAI, RateLimitError, AuthenticationError, APIError

def split_text(text, max_length=4096):
    """
    Split text into chunks that fit within the API's character limit.
    OpenAI TTS has a 4096 character limit per request.
    """
    sentences = text.replace('\n', ' ').split('. ')
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        # Add period back if it's not the last sentence
        sentence = sentence.strip()
        if sentence and not sentence.endswith('.'):
            sentence += '.'
        
        if len(current_chunk) + len(sentence) + 1 <= max_length:
            current_chunk += sentence + " "
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def main():
    # Check if API key is set
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY environment variable not set!")
        print("Please set it with: export OPENAI_API_KEY='your-api-key-here'")
        sys.exit(1)
    
    # Initialize the OpenAI client
    client = OpenAI(api_key=api_key)
    
    # Get input file
    if len(sys.argv) < 2:
        print("Usage: python text_to_speech_file.py <input_file> [output_file] [voice] [model]")
        print("\nExamples:")
        print("  python text_to_speech_file.py article.txt")
        print("  python text_to_speech_file.py article.txt output.mp3 nova tts-1-hd")
        print("\nAvailable voices:")
        print("  - alloy (neutral)")
        print("  - echo (male)")
        print("  - fable (neutral)")
        print("  - onyx (male)")
        print("  - nova (female)")
        print("  - shimmer (female)")
        print("\nAvailable models:")
        print("  - tts-1 (faster, standard quality)")
        print("  - tts-1-hd (slower, higher quality)")
        sys.exit(1)
    
    # Parse arguments
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "speech_output.mp3"
    voice = sys.argv[3] if len(sys.argv) > 3 else "alloy"
    model = sys.argv[4] if len(sys.argv) > 4 else "tts-1"
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"ERROR: Input file '{input_file}' not found!")
        sys.exit(1)
    
    # Validate voice
    valid_voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
    if voice not in valid_voices:
        print(f"ERROR: Invalid voice '{voice}'")
        print(f"Valid voices: {', '.join(valid_voices)}")
        sys.exit(1)
    
    # Validate model
    valid_models = ["tts-1", "tts-1-hd"]
    if model not in valid_models:
        print(f"ERROR: Invalid model '{model}'")
        print(f"Valid models: {', '.join(valid_models)}")
        sys.exit(1)
    
    # Ensure output file has correct extension
    if not output_file.endswith(('.mp3', '.opus', '.aac', '.flac')):
        output_file += '.mp3'
    
    try:
        print("=" * 60)
        print("OpenAI Text-to-Speech File Converter")
        print("=" * 60)
        
        # Read input file
        print(f"\nReading file: {input_file}")
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read().strip()
        
        if not text:
            print("ERROR: Input file is empty!")
            sys.exit(1)
        
        print(f"Text length: {len(text)} characters")
        
        # Split text if needed
        chunks = split_text(text)
        num_chunks = len(chunks)
        
        if num_chunks > 1:
            print(f"Text split into {num_chunks} chunks (API limit: 4096 chars/request)")
        
        print(f"Voice: {voice}")
        print(f"Model: {model}")
        print(f"Output: {output_file}")
        print("\nGenerating speech...")
        
        # Generate audio for each chunk
        audio_data = bytearray()
        
        for i, chunk in enumerate(chunks, 1):
            if num_chunks > 1:
                print(f"  Processing chunk {i}/{num_chunks}...")
            
            response = client.audio.speech.create(
                model=model,
                voice=voice,
                input=chunk
            )
            
            # Collect audio data
            audio_data.extend(response.content)
        
        # Save combined audio file
        output_path = Path(output_file)
        with open(output_path, 'wb') as f:
            f.write(audio_data)
        
        # Get file size for confirmation
        file_size = output_path.stat().st_size
        file_size_kb = file_size / 1024
        file_size_mb = file_size_kb / 1024
        
        print("\n" + "=" * 60)
        print("✓ Success!")
        print("=" * 60)
        print(f"Audio file saved: {output_path.absolute()}")
        if file_size_mb >= 1:
            print(f"File size: {file_size_mb:.2f} MB")
        else:
            print(f"File size: {file_size_kb:.2f} KB")
        print("\nYou can play it with:")
        print(f"  macOS: afplay {output_file}")
        print(f"  Linux: mpg123 {output_file}")
        print(f"  Windows: start {output_file}")
        print("=" * 60)
        
    except RateLimitError as e:
        print("\nERROR: Rate limit or quota exceeded!")
        print("\nThis means:")
        print("  • Your OpenAI account is out of credits")
        print("  • You've exceeded your usage quota")
        print("\nTo fix this:")
        print("  1. Go to: https://platform.openai.com/account/billing")
        print("  2. Add a payment method or purchase credits")
        print(f"\nFull error: {e}")
        sys.exit(1)
        
    except AuthenticationError as e:
        print("\nERROR: Authentication failed!")
        print("Your API key may be invalid or expired.")
        print("Get a valid key from: https://platform.openai.com/api-keys")
        print(f"\nFull error: {e}")
        sys.exit(1)
        
    except APIError as e:
        print(f"\nERROR: OpenAI API error occurred: {e}")
        sys.exit(1)
        
    except FileNotFoundError as e:
        print(f"\nERROR: File not found: {e}")
        sys.exit(1)
        
    except PermissionError:
        print(f"\nERROR: Permission denied")
        print("Check file permissions for input/output files.")
        sys.exit(1)
        
    except Exception as e:
        print(f"\nERROR: Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

