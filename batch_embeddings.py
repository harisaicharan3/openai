#!/usr/bin/env python3
"""
Script to generate embeddings for multiple texts from a file.
Each line in the input file will be converted to an embedding.
"""

import os
import sys
import json
import numpy as np
from openai import OpenAI, RateLimitError, AuthenticationError, APIError

def main():
    # Check if API key is set
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY environment variable not set!")
        sys.exit(1)
    
    # Get input file
    if len(sys.argv) < 2:
        print("Usage: python batch_embeddings.py <input_file> [output_file] [model]")
        print("\nExamples:")
        print("  python batch_embeddings.py texts.txt")
        print("  python batch_embeddings.py texts.txt embeddings.json")
        print("  python batch_embeddings.py texts.txt embeddings.json text-embedding-3-large")
        print("\nInput file format:")
        print("  One text per line")
        print("\nAvailable models:")
        print("  - text-embedding-3-small (default)")
        print("  - text-embedding-3-large")
        print("  - text-embedding-ada-002")
        sys.exit(1)
    
    # Parse arguments
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "embeddings.json"
    model = sys.argv[3] if len(sys.argv) > 3 else "text-embedding-3-small"
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"ERROR: Input file '{input_file}' not found!")
        sys.exit(1)
    
    # Validate model
    valid_models = ["text-embedding-3-small", "text-embedding-3-large", "text-embedding-ada-002"]
    if model not in valid_models:
        print(f"ERROR: Invalid model '{model}'")
        print(f"Valid models: {', '.join(valid_models)}")
        sys.exit(1)
    
    # Initialize the OpenAI client
    client = OpenAI(api_key=api_key)
    
    try:
        print("=" * 70)
        print("OpenAI Batch Embeddings Generator")
        print("=" * 70)
        
        # Read input file
        print(f"\nReading file: {input_file}")
        with open(input_file, 'r', encoding='utf-8') as f:
            texts = [line.strip() for line in f if line.strip()]
        
        if not texts:
            print("ERROR: Input file is empty!")
            sys.exit(1)
        
        print(f"Found {len(texts)} texts to process")
        print(f"Model: {model}")
        print("\nGenerating embeddings...")
        
        # Generate embeddings in batch (OpenAI supports up to 2048 inputs)
        batch_size = 100  # Process in smaller batches for safety
        all_embeddings = []
        total_tokens = 0
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            print(f"  Processing batch {i//batch_size + 1}/{(len(texts)-1)//batch_size + 1}...")
            
            response = client.embeddings.create(
                model=model,
                input=batch
            )
            
            for j, data in enumerate(response.data):
                all_embeddings.append({
                    "text": batch[j],
                    "embedding": data.embedding,
                    "index": i + j
                })
            
            total_tokens += response.usage.total_tokens
        
        # Prepare output data
        output_data = {
            "model": model,
            "dimensions": len(all_embeddings[0]["embedding"]),
            "total_texts": len(texts),
            "total_tokens": total_tokens,
            "embeddings": all_embeddings
        }
        
        # Save to file
        print(f"\nSaving embeddings to: {output_file}")
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        # Summary
        file_size = os.path.getsize(output_file)
        file_size_mb = file_size / (1024 * 1024)
        
        print("\n" + "=" * 70)
        print("✓ Success!")
        print("=" * 70)
        print(f"Processed: {len(texts)} texts")
        print(f"Dimensions: {output_data['dimensions']}")
        print(f"Tokens used: {total_tokens}")
        print(f"Output file: {output_file}")
        print(f"File size: {file_size_mb:.2f} MB")
        print("\nYou can now use these embeddings for:")
        print("  • Semantic search")
        print("  • Clustering similar texts")
        print("  • Finding recommendations")
        print("  • Classification tasks")
        print("=" * 70)
        
    except RateLimitError as e:
        print(f"\nERROR: Rate limit or quota exceeded: {e}")
        sys.exit(1)
    except AuthenticationError as e:
        print(f"\nERROR: Authentication failed: {e}")
        sys.exit(1)
    except APIError as e:
        print(f"\nERROR: API error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

