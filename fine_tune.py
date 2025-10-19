#!/usr/bin/env python3
"""
Script to create and start a fine-tuning job with OpenAI.
"""

import os
import sys
import time
from openai import OpenAI, RateLimitError, AuthenticationError, APIError

def check_file_status(client, file_id):
    """Check if the uploaded file is ready for fine-tuning."""
    file_info = client.files.retrieve(file_id)
    return file_info.status

def main():
    # Check if API key is set
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY environment variable not set!")
        print("Please set it with: export OPENAI_API_KEY='your-api-key-here'")
        sys.exit(1)
    
    # Initialize the OpenAI client
    client = OpenAI(api_key=api_key)
    
    # Path to your training data file (JSONL format)
    training_file_path = "training_data.jsonl"
    
    if not os.path.exists(training_file_path):
        print(f"ERROR: Training file '{training_file_path}' not found!")
        print("Please create a training data file in JSONL format.")
        print("See the example file for the required format.")
        sys.exit(1)
    
    try:
        print("=" * 60)
        print("OpenAI Fine-Tuning Job Creator")
        print("=" * 60)
        
        # Step 1: Upload the training file
        print(f"\n[1/3] Uploading training file: {training_file_path}")
        with open(training_file_path, "rb") as f:
            training_file = client.files.create(
                file=f,
                purpose="fine-tune"
            )
        
        print(f"✓ File uploaded successfully!")
        print(f"  File ID: {training_file.id}")
        print(f"  Filename: {training_file.filename}")
        print(f"  Status: {training_file.status}")
        
        # Step 2: Wait for file to be processed
        print("\n[2/3] Waiting for file to be processed...")
        while True:
            status = check_file_status(client, training_file.id)
            if status == "processed":
                print("✓ File processed successfully!")
                break
            elif status == "error":
                print("✗ File processing failed!")
                sys.exit(1)
            else:
                print(f"  Current status: {status}. Waiting...")
                time.sleep(2)
        
        # Step 3: Create fine-tuning job
        print("\n[3/3] Creating fine-tuning job...")
        fine_tuning_job = client.fine_tuning.jobs.create(
            training_file=training_file.id,
            model="gpt-3.5-turbo",  # You can use gpt-4o-mini-2024-07-18 or other models
            hyperparameters={
                "n_epochs": 3  # Number of training epochs
            }
        )
        
        print("✓ Fine-tuning job created successfully!")
        print("\n" + "=" * 60)
        print("Job Details:")
        print("=" * 60)
        print(f"Job ID: {fine_tuning_job.id}")
        print(f"Model: {fine_tuning_job.model}")
        print(f"Status: {fine_tuning_job.status}")
        print(f"Training file: {fine_tuning_job.training_file}")
        
        if fine_tuning_job.hyperparameters:
            print(f"Epochs: {fine_tuning_job.hyperparameters.n_epochs}")
        
        print("\n" + "=" * 60)
        print("Next Steps:")
        print("=" * 60)
        print("1. Monitor your job status at:")
        print("   https://platform.openai.com/finetune")
        print("\n2. Check job status with:")
        print(f"   python check_fine_tune_status.py {fine_tuning_job.id}")
        print("\n3. Once complete, use your fine-tuned model:")
        print(f"   model='ft:gpt-3.5-turbo:...'")
        print("\nNote: Fine-tuning can take several minutes to hours depending on")
        print("the size of your training data.")
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
        
    except FileNotFoundError as e:
        print(f"\nERROR: File not found: {e}")
        sys.exit(1)
        
    except APIError as e:
        print(f"\nERROR: OpenAI API error occurred: {e}")
        sys.exit(1)
        
    except Exception as e:
        print(f"\nERROR: Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

