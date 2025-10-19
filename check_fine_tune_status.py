#!/usr/bin/env python3
"""
Script to check the status of a fine-tuning job.
"""

import os
import sys
from openai import OpenAI

def main():
    # Check if API key is set
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY environment variable not set!")
        sys.exit(1)
    
    # Get job ID from command line argument
    if len(sys.argv) < 2:
        print("Usage: python check_fine_tune_status.py <job_id>")
        print("\nOr list all jobs:")
        print("python check_fine_tune_status.py --list")
        sys.exit(1)
    
    client = OpenAI(api_key=api_key)
    
    try:
        if sys.argv[1] == "--list":
            # List all fine-tuning jobs
            print("\n" + "=" * 60)
            print("All Fine-Tuning Jobs")
            print("=" * 60)
            jobs = client.fine_tuning.jobs.list(limit=10)
            
            for job in jobs.data:
                print(f"\nJob ID: {job.id}")
                print(f"Model: {job.model}")
                print(f"Status: {job.status}")
                print(f"Created: {job.created_at}")
                if job.finished_at:
                    print(f"Finished: {job.finished_at}")
                if job.fine_tuned_model:
                    print(f"Fine-tuned Model: {job.fine_tuned_model}")
                print("-" * 60)
        else:
            # Check specific job
            job_id = sys.argv[1]
            print(f"\nChecking status for job: {job_id}")
            print("=" * 60)
            
            job = client.fine_tuning.jobs.retrieve(job_id)
            
            print(f"Status: {job.status}")
            print(f"Model: {job.model}")
            print(f"Training file: {job.training_file}")
            
            if job.hyperparameters:
                print(f"Epochs: {job.hyperparameters.n_epochs}")
            
            if job.trained_tokens:
                print(f"Trained tokens: {job.trained_tokens}")
            
            if job.fine_tuned_model:
                print(f"\n✓ Fine-tuned model ready: {job.fine_tuned_model}")
                print("\nYou can now use this model in your API calls:")
                print(f"  model='{job.fine_tuned_model}'")
            elif job.status == "running":
                print("\n⟳ Job is still running...")
            elif job.status == "validating_files":
                print("\n⟳ Validating training files...")
            elif job.status == "queued":
                print("\n⟳ Job is queued...")
            elif job.status == "failed":
                print("\n✗ Job failed!")
                if job.error:
                    print(f"Error: {job.error}")
            
            # Show recent events
            print("\n" + "=" * 60)
            print("Recent Events:")
            print("=" * 60)
            events = client.fine_tuning.jobs.list_events(job_id, limit=5)
            for event in events.data:
                print(f"[{event.created_at}] {event.message}")
            
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

