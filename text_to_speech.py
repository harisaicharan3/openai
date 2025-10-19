#!/usr/bin/env python3
"""
Script to convert text to speech using OpenAI's TTS API.
"""

import os
import sys
from pathlib import Path
from openai import OpenAI, RateLimitError, AuthenticationError, APIError

def main():
    # Check if API key is set
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY environment variable not set!")
        print("Please set it with: export OPENAI_API_KEY='your-api-key-here'")
        sys.exit(1)
    
    # Initialize the OpenAI client
    client = OpenAI(api_key=api_key)
    
    # Get text input
    if len(sys.argv) < 2:
        print("Usage: python text_to_speech.py <text> [output_file] [voice] [model]")
        print("\nExamples:")
        print("  python text_to_speech.py \"Hello, world!\"")
        print("  python text_to_speech.py \"Hello, world!\" output.mp3")
        print("  python text_to_speech.py \"Hello, world!\" output.mp3 alloy")
        print("  python text_to_speech.py \"Hello, world!\" output.mp3 nova tts-1-hd")
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
    text = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "speech.mp3"
    voice = sys.argv[3] if len(sys.argv) > 3 else "alloy"
    model = sys.argv[4] if len(sys.argv) > 4 else "tts-1"
    
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
        print("OpenAI Text-to-Speech Generator")
        print("=" * 60)
        print(f"\nText: {text}")
        print(f"Voice: {voice}")
        print(f"Model: {model}")
        print(f"Output: {output_file}")
        print("\nGenerating speech...")
        
        # Make the API call
        response = client.audio.speech.create(
            model=model,
            voice=voice,
            input=text
        )
        
        # Save the audio file
        output_path = Path(output_file)
        response.stream_to_file(output_path)
        
        # Get file size for confirmation
        file_size = output_path.stat().st_size
        file_size_kb = file_size / 1024
        
        print("\n" + "=" * 60)
        print("✓ Success!")
        print("=" * 60)
        print(f"Audio file saved: {output_path.absolute()}")
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
        
    except PermissionError:
        print(f"\nERROR: Permission denied writing to '{output_file}'")
        print("Try a different output location or check file permissions.")
        sys.exit(1)
        
    except Exception as e:
        print(f"\nERROR: Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

