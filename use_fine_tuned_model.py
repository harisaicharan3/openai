#!/usr/bin/env python3
"""
Script to use a fine-tuned model for chat completions.
"""

import os
import sys
from openai import OpenAI, RateLimitError, AuthenticationError, APIError

def main():
    # Check if API key is set
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY environment variable not set!")
        sys.exit(1)
    
    # Get model name from command line
    if len(sys.argv) < 2:
        print("Usage: python use_fine_tuned_model.py <fine_tuned_model_name>")
        print("\nExample:")
        print("  python use_fine_tuned_model.py ft:gpt-3.5-turbo-0125:my-org:custom-model:9ABcDEf")
        sys.exit(1)
    
    fine_tuned_model = sys.argv[1]
    
    # Initialize the OpenAI client
    client = OpenAI(api_key=api_key)
    
    # Get user prompt
    if len(sys.argv) >= 3:
        user_message = " ".join(sys.argv[2:])
    else:
        user_message = "What are your business hours?"
    
    print(f"Using model: {fine_tuned_model}")
    print(f"User message: {user_message}\n")
    
    try:
        # Make the API call with fine-tuned model
        response = client.chat.completions.create(
            model=fine_tuned_model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant for a tech company."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        # Extract and print the response
        assistant_message = response.choices[0].message.content
        print("Response:")
        print("-" * 60)
        print(assistant_message)
        print("-" * 60)
        print(f"\nTokens used: {response.usage.total_tokens}")
        
    except RateLimitError as e:
        print(f"ERROR: Rate limit or quota exceeded: {e}")
        sys.exit(1)
    except AuthenticationError as e:
        print(f"ERROR: Authentication failed: {e}")
        sys.exit(1)
    except APIError as e:
        print(f"ERROR: API error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

