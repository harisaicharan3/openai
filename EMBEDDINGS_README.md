# OpenAI Embeddings Guide

Convert text into vector representations (embeddings) for semantic search, clustering, recommendations, and more.

## What are Embeddings?

Embeddings are numerical vector representations of text that capture semantic meaning. Similar texts have similar embeddings, enabling:

- **Semantic Search**: Find relevant content based on meaning, not just keywords
- **Clustering**: Group similar texts together
- **Recommendations**: Suggest similar items
- **Classification**: Categorize text into groups
- **Anomaly Detection**: Find unusual or outlier texts

## Files Included

1. **`text_embeddings.py`** - Generate embeddings for single texts
2. **`batch_embeddings.py`** - Generate embeddings for multiple texts from a file
3. **`semantic_search.py`** - Search through texts using natural language
4. **`sample_texts.txt`** - Example texts for testing

## Quick Start

### Generate a Single Embedding

```bash
python text_embeddings.py "Machine learning is fascinating"
```

### Compare Two Texts

```bash
python text_embeddings.py --compare "Python programming" "Coding in Python"
```

### Batch Process Multiple Texts

```bash
# Create embeddings for all texts in a file
python batch_embeddings.py sample_texts.txt

# Then search through them
python semantic_search.py embeddings.json "artificial intelligence"
```

## Available Models

| Model | Dimensions | Use Case | Cost per 1M tokens |
|-------|------------|----------|-------------------|
| **text-embedding-3-small** | 1536 | General purpose, fast, affordable | ~$0.02 |
| **text-embedding-3-large** | 3072 | Higher quality, more accurate | ~$0.13 |
| **text-embedding-ada-002** | 1536 | Legacy model (still supported) | ~$0.10 |

**Recommendation**: Use `text-embedding-3-small` for most use cases. Use `text-embedding-3-large` when you need maximum accuracy.

## Detailed Usage

### 1. Generate Single Embedding

```bash
# Basic usage
python text_embeddings.py "Your text here"

# Use specific model
python text_embeddings.py "Your text" text-embedding-3-large

# Save to file
python text_embeddings.py "Your text" --save embedding.json
```

**Output includes:**
- Full embedding vector (array of numbers)
- Dimensions (1536 or 3072)
- Statistics (mean, std dev, min, max)
- Token usage

### 2. Compare Text Similarity

```bash
python text_embeddings.py --compare "cat" "dog"
python text_embeddings.py --compare "machine learning" "artificial intelligence"
```

**Similarity scores:**
- **> 0.9**: Very similar (nearly identical meaning)
- **0.7-0.9**: Similar (related concepts)
- **0.5-0.7**: Somewhat similar
- **0.3-0.5**: Weakly similar
- **< 0.3**: Different (unrelated)

**Example:**
```bash
python text_embeddings.py --compare "Python programming" "Coding in Python"
# Output: Similarity: ~0.95 (Very similar)

python text_embeddings.py --compare "Python programming" "Making pizza"
# Output: Similarity: ~0.30 (Different)
```

### 3. Batch Processing

```bash
# Generate embeddings for all texts
python batch_embeddings.py sample_texts.txt

# Custom output file and model
python batch_embeddings.py mytexts.txt my_embeddings.json text-embedding-3-large
```

**Input file format** (one text per line):
```
First piece of text
Second piece of text
Third piece of text
```

### 4. Semantic Search

```bash
# Search with default top 5 results
python semantic_search.py embeddings.json "programming languages"

# Get top 10 results
python semantic_search.py embeddings.json "artificial intelligence" 10
```

**How it works:**
1. Converts your query to an embedding
2. Compares it with all stored embeddings
3. Returns the most similar texts ranked by relevance

## Use Cases & Examples

### Use Case 1: Document Search

```bash
# Step 1: Create a file with document snippets
echo "Product documentation for API authentication" >> docs.txt
echo "User guide for mobile app installation" >> docs.txt
echo "Troubleshooting network connectivity issues" >> docs.txt
# ... add more documents

# Step 2: Generate embeddings
python batch_embeddings.py docs.txt doc_embeddings.json

# Step 3: Search
python semantic_search.py doc_embeddings.json "How to login?"
```

### Use Case 2: FAQ Matching

```bash
# Create FAQ file
cat > faq.txt << EOF
How do I reset my password?
What are your business hours?
How can I contact support?
What payment methods do you accept?
EOF

# Generate embeddings
python batch_embeddings.py faq.txt faq_embeddings.json

# Find matching FAQ
python semantic_search.py faq_embeddings.json "I forgot my login credentials"
# Returns: "How do I reset my password?" (high similarity)
```

### Use Case 3: Content Recommendation

```bash
# If a user likes "Machine learning tutorials"
python semantic_search.py embeddings.json "Machine learning tutorials" 5
# Returns similar content they might enjoy
```

### Use Case 4: Duplicate Detection

```bash
# Compare two texts to find duplicates
python text_embeddings.py --compare "Text version 1" "Text version 2"
# High similarity (>0.95) suggests duplicates
```

### Use Case 5: Text Clustering

Generate embeddings for your texts, then use the vectors for clustering:

```python
import json
import numpy as np
from sklearn.cluster import KMeans

# Load embeddings
with open('embeddings.json') as f:
    data = json.load(f)

# Extract vectors
vectors = [item['embedding'] for item in data['embeddings']]
texts = [item['text'] for item in data['embeddings']]

# Cluster into 5 groups
kmeans = KMeans(n_clusters=5, random_state=42)
labels = kmeans.fit_predict(vectors)

# Group texts by cluster
for i in range(5):
    print(f"\nCluster {i}:")
    cluster_texts = [texts[j] for j in range(len(texts)) if labels[j] == i]
    for text in cluster_texts:
        print(f"  - {text}")
```

## Understanding the Output

### Single Embedding Output

```
Embedding Generated Successfully!
Model: text-embedding-3-small
Dimensions: 1536
Tokens used: 8

First 10 values (preview):
[
  0.01234567,
  -0.02345678,
  0.03456789,
  ...
]

Statistics:
  Mean: 0.00012345
  Std Dev: 0.12345678
  Min: -0.45678901
  Max: 0.56789012
  L2 Norm: 1.00000000
```

**What it means:**
- **Dimensions**: Length of the vector (1536 or 3072 numbers)
- **Mean/Std Dev**: Distribution of values
- **L2 Norm**: Magnitude of the vector (usually normalized to 1.0)

### Comparison Output

```
Cosine Similarity: 0.850000
Similarity Percentage: 85.00%

Interpretation:
  ✓ Similar - Related concepts
```

**Cosine Similarity** ranges from -1 to 1:
- **1.0**: Identical
- **0.0**: Unrelated
- **-1.0**: Opposite (rare with text)

## Tips for Best Results

### 1. Text Preprocessing

Clean your text before generating embeddings:

```python
import re

def clean_text(text):
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    # Remove special characters if needed
    # text = re.sub(r'[^\w\s]', '', text)
    return text
```

### 2. Optimal Text Length

- **Sweet spot**: 50-500 tokens
- Too short (<10 tokens): Less meaningful embeddings
- Too long (>8000 tokens): Will be truncated

### 3. Choose the Right Model

```bash
# For general use (fast, cheap)
python batch_embeddings.py data.txt embeddings.json text-embedding-3-small

# For maximum accuracy (slower, more expensive)
python batch_embeddings.py data.txt embeddings.json text-embedding-3-large
```

### 4. Batch Processing Benefits

- More efficient (fewer API calls)
- Faster processing
- Lower cost per text

```bash
# Instead of 100 API calls:
# for i in {1..100}; do python text_embeddings.py "$text"; done

# Do one batch call:
python batch_embeddings.py texts.txt
```

## Cost Estimation

Embeddings are very affordable:

| Model | Cost | Example |
|-------|------|---------|
| text-embedding-3-small | $0.02 / 1M tokens | 1000 texts (100 words each) ≈ $0.002 |
| text-embedding-3-large | $0.13 / 1M tokens | 1000 texts (100 words each) ≈ $0.013 |

**Real-world examples:**
- 10,000 product descriptions: ~$0.20
- 1 million short texts: ~$20-130
- FAQ database (500 questions): ~$0.01

Check current pricing: https://openai.com/pricing

## Advanced Integration

### Storing Embeddings in a Database

```python
# Example with SQLite
import sqlite3
import json

conn = sqlite3.connect('embeddings.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS embeddings
             (id INTEGER PRIMARY KEY, text TEXT, embedding TEXT)''')

# Store
c.execute("INSERT INTO embeddings VALUES (?, ?, ?)",
          (1, "Some text", json.dumps(embedding)))
conn.commit()

# Retrieve
c.execute("SELECT text, embedding FROM embeddings WHERE id=?", (1,))
text, embedding_json = c.fetchone()
embedding = json.loads(embedding_json)
```

### Using with Vector Databases

For production use at scale, consider vector databases:
- **Pinecone**: Fully managed
- **Weaviate**: Open source
- **Milvus**: Scalable
- **Qdrant**: Rust-based, fast
- **FAISS**: Facebook's similarity search

### Real-time Search API

```python
from flask import Flask, request, jsonify
from openai import OpenAI
import json

app = Flask(__name__)
client = OpenAI()

# Load pre-computed embeddings
with open('embeddings.json') as f:
    data = json.load(f)

@app.route('/search', methods=['POST'])
def search():
    query = request.json['query']
    
    # Generate query embedding
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )
    query_emb = response.data[0].embedding
    
    # Find similar (implement cosine similarity)
    # ... similarity calculation ...
    
    return jsonify(results)

if __name__ == '__main__':
    app.run()
```

## Troubleshooting

### Issue: Low similarity for obviously related texts

**Solution:**
- Use `text-embedding-3-large` for better accuracy
- Ensure texts are clean and properly formatted
- Consider the context and domain

### Issue: Large file size for embeddings

**Solution:**
- Each embedding takes ~6-12 KB
- Consider storing in a database
- Use compression for storage
- Only store embeddings you need

### Issue: Slow batch processing

**Solution:**
- Process in batches of 100-500 texts
- Use `text-embedding-3-small` for faster processing
- Consider parallel processing for very large datasets

## Limitations

- **Context window**: Max ~8,000 tokens per input
- **Language**: Works best with English, but supports 100+ languages
- **Not real-time**: Pre-compute embeddings for best performance
- **Storage**: Large datasets require significant storage

## Example Workflow: Building a Search Engine

```bash
# 1. Prepare your documents
cat > articles.txt << EOF
Article about machine learning
Article about web development
Article about data science
EOF

# 2. Generate embeddings
python batch_embeddings.py articles.txt articles_emb.json

# 3. Search
python semantic_search.py articles_emb.json "AI and ML" 5

# 4. Integrate into your application
# Use the embeddings JSON in your app for real-time search
```

## Additional Resources

- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)
- [API Reference](https://platform.openai.com/docs/api-reference/embeddings)
- [Pricing](https://openai.com/pricing)
- [Best Practices](https://platform.openai.com/docs/guides/embeddings/use-cases)

