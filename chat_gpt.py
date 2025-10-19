#!/usr/bin/env python3
"""
Simple script to call OpenAI GPT and print a response.
"""

import os
import sys
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
    
    # Define the prompt/message
    user_message = "can u give the model id that u are using ? ai model"
    
    print(f"Sending message: {user_message}\n")
    
    try:
        # Make the API call
        response = client.chat.completions.create(
            model="ft:gpt-3.5-turbo-0125:born2rule::CSC05TYi",  # You can also use "gpt-4" or other models
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        # Extract and print the response
        assistant_message = response.choices[0].message.content
        print("GPT Response:")
        print("-" * 50)
        print(assistant_message)
        print("-" * 50)
        
        # Optional: Print usage information
        print(f"\nTokens used: {response.usage.total_tokens}")
        
    except RateLimitError as e:
        print("ERROR: Rate limit or quota exceeded!")
        print("\nThis means:")
        print("  • Your OpenAI account is out of credits")
        print("  • You've exceeded your usage quota")
        print("\nTo fix this:")
        print("  1. Go to: https://platform.openai.com/account/billing")
        print("  2. Add a payment method or purchase credits")
        print("  3. Check your usage limits and billing details")
        print(f"\nFull error: {e}")
        sys.exit(1)
        
    except AuthenticationError as e:
        print("ERROR: Authentication failed!")
        print("Your API key may be invalid or expired.")
        print("Get a valid key from: https://platform.openai.com/api-keys")
        print(f"\nFull error: {e}")
        sys.exit(1)
        
    except APIError as e:
        print(f"ERROR: OpenAI API error occurred: {e}")
        sys.exit(1)
        
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

