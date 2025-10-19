#!/usr/bin/env python3
"""
Script to generate embeddings from text using OpenAI's Embeddings API.
Embeddings are vector representations of text useful for:
- Semantic search
- Clustering
- Recommendations
- Anomaly detection
- Classification
"""

import os
import sys
import json
import numpy as np
from openai import OpenAI, RateLimitError, AuthenticationError, APIError

def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors."""
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

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
        print("Usage: python text_embeddings.py <text> [model]")
        print("\nExamples:")
        print('  python text_embeddings.py "The quick brown fox"')
        print('  python text_embeddings.py "Machine learning" text-embedding-3-large')
        print("\nAvailable models:")
        print("  - text-embedding-3-small (default, 1536 dimensions, faster, cheaper)")
        print("  - text-embedding-3-large (3072 dimensions, higher quality)")
        print("  - text-embedding-ada-002 (legacy, 1536 dimensions)")
        print("\nOptions:")
        print("  --compare <text1> <text2>  Compare similarity between two texts")
        print("  --save <filename>          Save embeddings to JSON file")
        sys.exit(1)
    
    # Check for comparison mode
    if sys.argv[1] == "--compare":
        if len(sys.argv) < 4:
            print("ERROR: --compare requires two text arguments")
            print('Usage: python text_embeddings.py --compare "text1" "text2" [model]')
            sys.exit(1)
        
        text1 = sys.argv[2]
        text2 = sys.argv[3]
        model = sys.argv[4] if len(sys.argv) > 4 else "text-embedding-3-small"
        
        compare_mode = True
    else:
        text = sys.argv[1]
        model = sys.argv[2] if len(sys.argv) > 2 else "text-embedding-3-small"
        compare_mode = False
    
    # Check for save option
    save_file = None
    if "--save" in sys.argv:
        save_index = sys.argv.index("--save")
        if save_index + 1 < len(sys.argv):
            save_file = sys.argv[save_index + 1]
    
    # Validate model
    valid_models = ["text-embedding-3-small", "text-embedding-3-large", "text-embedding-ada-002"]
    if model not in valid_models:
        print(f"ERROR: Invalid model '{model}'")
        print(f"Valid models: {', '.join(valid_models)}")
        sys.exit(1)
    
    try:
        print("=" * 70)
        print("OpenAI Text Embeddings Generator")
        print("=" * 70)
        
        if compare_mode:
            print(f"\nModel: {model}")
            print(f"Text 1: {text1}")
            print(f"Text 2: {text2}")
            print("\nGenerating embeddings...")
            
            # Generate embeddings for both texts
            response1 = client.embeddings.create(
                model=model,
                input=text1
            )
            
            response2 = client.embeddings.create(
                model=model,
                input=text2
            )
            
            embedding1 = response1.data[0].embedding
            embedding2 = response2.data[0].embedding
            
            # Calculate similarity
            similarity = cosine_similarity(embedding1, embedding2)
            
            print("\n" + "=" * 70)
            print("Results:")
            print("=" * 70)
            print(f"Embedding 1 dimensions: {len(embedding1)}")
            print(f"Embedding 2 dimensions: {len(embedding2)}")
            print(f"\nCosine Similarity: {similarity:.6f}")
            print(f"Similarity Percentage: {similarity * 100:.2f}%")
            
            # Interpretation
            print("\nInterpretation:")
            if similarity > 0.9:
                print("  ✓ Very similar - Nearly identical meaning")
            elif similarity > 0.7:
                print("  ✓ Similar - Related concepts")
            elif similarity > 0.5:
                print("  ~ Somewhat similar - Some relation")
            elif similarity > 0.3:
                print("  ~ Weakly similar - Distant relation")
            else:
                print("  ✗ Different - Unrelated concepts")
            
            print(f"\nTokens used: {response1.usage.total_tokens + response2.usage.total_tokens}")
            
        else:
            print(f"\nText: {text}")
            print(f"Model: {model}")
            print("\nGenerating embedding...")
            
            # Generate embedding
            response = client.embeddings.create(
                model=model,
                input=text
            )
            
            embedding = response.data[0].embedding
            
            print("\n" + "=" * 70)
            print("Embedding Generated Successfully!")
            print("=" * 70)
            print(f"Model: {model}")
            print(f"Dimensions: {len(embedding)}")
            print(f"Tokens used: {response.usage.total_tokens}")
            
            # Display first 10 values as preview
            print(f"\nFirst 10 values (preview):")
            print("[")
            for i in range(min(10, len(embedding))):
                print(f"  {embedding[i]:.8f},")
            print("  ...")
            print("]")
            
            # Statistics
            embedding_array = np.array(embedding)
            print(f"\nStatistics:")
            print(f"  Mean: {np.mean(embedding_array):.8f}")
            print(f"  Std Dev: {np.std(embedding_array):.8f}")
            print(f"  Min: {np.min(embedding_array):.8f}")
            print(f"  Max: {np.max(embedding_array):.8f}")
            print(f"  L2 Norm: {np.linalg.norm(embedding_array):.8f}")
            
            # Save to file if requested
            if save_file:
                data = {
                    "text": text,
                    "model": model,
                    "embedding": embedding,
                    "dimensions": len(embedding),
                    "usage": {
                        "prompt_tokens": response.usage.prompt_tokens,
                        "total_tokens": response.usage.total_tokens
                    }
                }
                with open(save_file, 'w') as f:
                    json.dump(data, f, indent=2)
                print(f"\n✓ Embedding saved to: {save_file}")
            
            # Full embedding output option
            print("\n" + "=" * 70)
            print("Full Embedding Vector:")
            print("=" * 70)
            print(json.dumps(embedding, indent=2))
        
        print("=" * 70)
        
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
        
    except Exception as e:
        print(f"\nERROR: Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

