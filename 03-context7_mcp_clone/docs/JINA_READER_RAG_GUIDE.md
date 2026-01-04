# Jina Reader API for RAG Applications

## Table of Contents
- [Overview](#overview)
- [Basic Usage](#basic-usage)
- [API Features](#api-features)
- [Python Integration Examples](#python-integration-examples)
- [RAG Application Patterns](#rag-application-patterns)
- [Advanced Features](#advanced-features)
- [Best Practices](#best-practices)
- [Rate Limits & Performance](#rate-limits--performance)

## Overview

The Jina Reader API (r.jina.ai) is a powerful service that converts any URL into clean, LLM-friendly markdown content. It's designed specifically for Retrieval-Augmented Generation (RAG) applications, making it easy to extract and index web content for vector search and embeddings.

### Key Benefits for RAG
- **Clean Markdown Output**: Automatically extracts main content, removing ads, navigation, and clutter
- **LLM-Optimized**: Formatted for direct consumption by language models
- **Image Captioning**: Optional AI-generated alt text for images
- **No Browser Required**: Server-side rendering handles JavaScript-heavy sites
- **PDF Support**: Natively reads PDFs and converts to markdown
- **Built-in Search**: Web search with automatic content extraction

## Basic Usage

### Simple URL Conversion

The simplest way to use Jina Reader is to prepend `https://r.jina.ai/` to any URL:

```
https://r.jina.ai/https://en.wikipedia.org/wiki/Artificial_intelligence
```

### Command Line Example

```bash
# Basic request
curl "https://r.jina.ai/https://www.example.com"

# With JSON output
curl -H "Accept: application/json" "https://r.jina.ai/https://www.example.com"

# With image captions enabled
curl -H "x-with-generated-alt: true" "https://r.jina.ai/https://blog.example.com/article"
```

## API Features

### Response Formats

| Header | Output Format | Use Case |
|--------|--------------|----------|
| `Accept: application/json` | JSON with url, title, content | Programmatic access |
| `Accept: text/event-stream` | Streaming markdown | Large documents |
| Default | Plain markdown | Direct LLM consumption |

### Request Headers

| Header | Purpose | Example |
|--------|---------|---------|
| `x-with-generated-alt: true` | Enable AI image captions | For visual context in RAG |
| `x-respond-with: markdown` | Bypass readability filter | Maximum content extraction |
| `x-respond-with: html` | Get raw HTML | Custom processing |
| `x-respond-with: text` | Plain text only | Minimal formatting |
| `x-respond-with: screenshot` | Page screenshot URL | Visual documentation |
| `x-no-cache: true` | Bypass cache | Fresh content needed |
| `x-timeout: 30` | Set timeout (seconds) | SPA/dynamic content |
| `x-target-selector: #main` | Focus on CSS selector | Extract specific sections |
| `x-wait-for-selector: .content` | Wait for element | Dynamic loading |

### Search API

```bash
# Web search with top 5 results
curl "https://s.jina.ai/What is RAG in AI?"

# Site-specific search
curl "https://s.jina.ai/vector embeddings?site=openai.com&site=pinecone.io"
```

## Python Integration Examples

### 1. Basic URL Fetching

```python
import requests

def fetch_url_as_markdown(url: str) -> dict:
    """
    Fetch any URL and convert to LLM-friendly markdown.

    Args:
        url: The target URL to convert

    Returns:
        dict with 'url', 'title', 'content' keys
    """
    reader_url = f"https://r.jina.ai/{url}"

    response = requests.get(
        reader_url,
        headers={"Accept": "application/json"}
    )
    response.raise_for_status()

    return response.json()


# Example usage
result = fetch_url_as_markdown("https://en.wikipedia.org/wiki/Vector_database")
print(f"Title: {result['title']}")
print(f"Content length: {len(result['content'])} characters")
print(f"First 500 chars:\n{result['content'][:500]}")
```

### 2. Enhanced Fetching with Image Captions

```python
import requests
from typing import Optional

def fetch_with_images(
    url: str,
    enable_captions: bool = True,
    timeout: int = 30
) -> dict:
    """
    Fetch URL with optional AI-generated image captions.

    Args:
        url: Target URL
        enable_captions: Generate alt text for images
        timeout: Request timeout in seconds

    Returns:
        JSON response with url, title, content
    """
    reader_url = f"https://r.jina.ai/{url}"

    headers = {
        "Accept": "application/json",
        "x-timeout": str(timeout)
    }

    if enable_captions:
        headers["x-with-generated-alt"] = "true"

    response = requests.get(reader_url, headers=headers)
    response.raise_for_status()

    return response.json()


# Example: Fetch blog post with image descriptions
article = fetch_with_images(
    "https://blog.example.com/machine-learning-tutorial",
    enable_captions=True
)
```

### 3. Web Search for RAG

```python
import requests
from urllib.parse import quote

def search_and_extract(query: str, sites: Optional[list] = None) -> dict:
    """
    Search the web and get LLM-ready content from top 5 results.

    Args:
        query: Search query
        sites: Optional list of sites to restrict search

    Returns:
        Aggregated search results in markdown
    """
    # URL encode the query
    encoded_query = quote(query)
    search_url = f"https://s.jina.ai/{encoded_query}"

    # Add site restrictions if provided
    if sites:
        site_params = "&".join([f"site={site}" for site in sites])
        search_url = f"{search_url}?{site_params}"

    response = requests.get(
        search_url,
        headers={"Accept": "application/json"}
    )
    response.raise_for_status()

    return response.json()


# Example: Search for RAG information
results = search_and_extract(
    "retrieval augmented generation tutorial",
    sites=["openai.com", "pinecone.io", "langchain.com"]
)
```

### 4. Batch Processing for RAG Index Creation

```python
import requests
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

class JinaReaderBatch:
    """Batch process URLs with Jina Reader for RAG indexing."""

    def __init__(self, max_workers: int = 5, delay: float = 0.1):
        """
        Initialize batch processor.

        Args:
            max_workers: Max concurrent requests (respect rate limits)
            delay: Delay between requests (seconds)
        """
        self.max_workers = max_workers
        self.delay = delay
        self.base_url = "https://r.jina.ai/"

    def fetch_single(self, url: str, headers: dict = None) -> dict:
        """Fetch single URL with error handling."""
        try:
            reader_url = f"{self.base_url}{url}"
            default_headers = {"Accept": "application/json"}

            if headers:
                default_headers.update(headers)

            response = requests.get(reader_url, headers=default_headers)
            response.raise_for_status()

            result = response.json()
            result['success'] = True
            result['error'] = None

            return result

        except Exception as e:
            return {
                'url': url,
                'success': False,
                'error': str(e),
                'content': None,
                'title': None
            }

    def fetch_batch(
        self,
        urls: List[str],
        enable_captions: bool = False
    ) -> List[Dict]:
        """
        Fetch multiple URLs in parallel with rate limiting.

        Args:
            urls: List of URLs to fetch
            enable_captions: Enable image captions

        Returns:
            List of results with url, title, content, success, error
        """
        headers = {}
        if enable_captions:
            headers["x-with-generated-alt"] = "true"

        results = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_url = {
                executor.submit(self.fetch_single, url, headers): url
                for url in urls
            }

            # Process completed tasks
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    result = future.result()
                    results.append(result)

                    # Rate limiting
                    time.sleep(self.delay)

                except Exception as e:
                    results.append({
                        'url': url,
                        'success': False,
                        'error': str(e),
                        'content': None,
                        'title': None
                    })

        return results


# Example usage
batch_processor = JinaReaderBatch(max_workers=5, delay=0.2)

urls_to_index = [
    "https://docs.python.org/3/tutorial/index.html",
    "https://fastapi.tiangolo.com/",
    "https://www.langchain.com/",
    "https://docs.pinecone.io/docs/overview",
]

results = batch_processor.fetch_batch(urls_to_index, enable_captions=True)

for result in results:
    if result['success']:
        print(f"✓ {result['title']} - {len(result['content'])} chars")
    else:
        print(f"✗ {result['url']} - Error: {result['error']}")
```

## RAG Application Patterns

### Pattern 1: Building a Documentation Index

```python
import requests
from typing import List, Dict
import hashlib

class DocumentationIndexer:
    """Index documentation using Jina Reader for RAG."""

    def __init__(self, cache_dir: str = "cache"):
        self.cache_dir = cache_dir
        self.documents = []

    def fetch_and_chunk(
        self,
        url: str,
        chunk_size: int = 1000,
        overlap: int = 200
    ) -> List[Dict]:
        """
        Fetch URL and split into chunks for vector embedding.

        Args:
            url: Documentation URL
            chunk_size: Characters per chunk
            overlap: Overlap between chunks

        Returns:
            List of document chunks with metadata
        """
        # Fetch content
        reader_url = f"https://r.jina.ai/{url}"
        response = requests.get(
            reader_url,
            headers={"Accept": "application/json"}
        )
        response.raise_for_status()

        data = response.json()
        content = data['content']
        title = data['title']

        # Split into overlapping chunks
        chunks = []
        start = 0

        while start < len(content):
            end = start + chunk_size
            chunk_text = content[start:end]

            # Create chunk metadata
            chunk_id = hashlib.md5(
                f"{url}_{start}".encode()
            ).hexdigest()[:12]

            chunks.append({
                'id': chunk_id,
                'text': chunk_text,
                'url': url,
                'title': title,
                'start_pos': start,
                'end_pos': end,
                'chunk_index': len(chunks)
            })

            # Move to next chunk with overlap
            start = end - overlap

        return chunks

    def index_documentation(self, urls: List[str]) -> List[Dict]:
        """
        Index multiple documentation pages.

        Args:
            urls: List of documentation URLs

        Returns:
            All document chunks ready for embedding
        """
        all_chunks = []

        for url in urls:
            print(f"Indexing: {url}")
            try:
                chunks = self.fetch_and_chunk(url)
                all_chunks.extend(chunks)
                print(f"  ✓ Created {len(chunks)} chunks")
            except Exception as e:
                print(f"  ✗ Error: {e}")

        self.documents = all_chunks
        return all_chunks


# Example: Index FastAPI documentation
indexer = DocumentationIndexer()

docs_urls = [
    "https://fastapi.tiangolo.com/",
    "https://fastapi.tiangolo.com/tutorial/first-steps/",
    "https://fastapi.tiangolo.com/tutorial/path-params/",
]

chunks = indexer.index_documentation(docs_urls)
print(f"\nTotal chunks for embedding: {len(chunks)}")
```

### Pattern 2: RAG with Vector Embeddings

```python
import requests
from typing import List, Dict
import numpy as np

class JinaRAGPipeline:
    """Complete RAG pipeline using Jina Reader and embeddings."""

    def __init__(self, embedding_model: str = "sentence-transformers"):
        self.embedding_model = embedding_model
        self.documents = []
        self.embeddings = []

    def fetch_urls(self, urls: List[str]) -> List[Dict]:
        """Fetch and prepare documents from URLs."""
        documents = []

        for url in urls:
            reader_url = f"https://r.jina.ai/{url}"
            try:
                response = requests.get(
                    reader_url,
                    headers={
                        "Accept": "application/json",
                        "x-with-generated-alt": "true"
                    }
                )
                response.raise_for_status()

                data = response.json()
                documents.append({
                    'url': url,
                    'title': data['title'],
                    'content': data['content'],
                    'metadata': {
                        'source': 'jina_reader',
                        'fetched_at': data.get('timestamp')
                    }
                })
            except Exception as e:
                print(f"Error fetching {url}: {e}")

        self.documents = documents
        return documents

    def create_embeddings(self, documents: List[Dict]) -> np.ndarray:
        """
        Create vector embeddings for documents.

        Note: This is a placeholder. In production, use:
        - OpenAI embeddings (text-embedding-3-small)
        - Sentence Transformers
        - Jina Embeddings API
        - Cohere embeddings
        """
        # Placeholder for embedding generation
        # In production, replace with actual embedding model

        print(f"Creating embeddings for {len(documents)} documents...")

        # Example using sentence-transformers (install: pip install sentence-transformers)
        # from sentence_transformers import SentenceTransformer
        # model = SentenceTransformer('all-MiniLM-L6-v2')
        # texts = [doc['content'][:512] for doc in documents]  # Truncate for demo
        # embeddings = model.encode(texts)
        # self.embeddings = embeddings
        # return embeddings

        # For now, return placeholder
        return np.random.rand(len(documents), 384)  # Placeholder

    def semantic_search(
        self,
        query: str,
        top_k: int = 3
    ) -> List[Dict]:
        """
        Search documents using semantic similarity.

        Args:
            query: Search query
            top_k: Number of results

        Returns:
            Top matching documents with scores
        """
        # Placeholder for semantic search
        # In production, use vector database (Pinecone, Weaviate, Chroma, etc.)

        print(f"Searching for: '{query}'")

        # Simple keyword match for demo (replace with vector similarity)
        results = []
        for i, doc in enumerate(self.documents):
            if query.lower() in doc['content'].lower():
                results.append({
                    'document': doc,
                    'score': 0.95,  # Placeholder score
                    'index': i
                })

        return results[:top_k]


# Example usage
rag = JinaRAGPipeline()

# Index documentation
knowledge_base_urls = [
    "https://docs.langchain.com/docs/",
    "https://python.langchain.com/docs/get_started/introduction",
    "https://python.langchain.com/docs/modules/data_connection/",
]

documents = rag.fetch_urls(knowledge_base_urls)
embeddings = rag.create_embeddings(documents)

# Search
results = rag.semantic_search("How do I load documents?", top_k=3)
for result in results:
    print(f"\n{result['document']['title']}")
    print(f"Score: {result['score']}")
    print(f"URL: {result['document']['url']}")
```

### Pattern 3: Real-time Web Search in RAG

```python
import requests
from typing import List, Dict

class JinaSearchRAG:
    """Use Jina Search API for real-time information retrieval."""

    def search_and_retrieve(
        self,
        query: str,
        sites: List[str] = None,
        max_results: int = 5
    ) -> Dict:
        """
        Search web and get pre-processed content for RAG.

        Args:
            query: Search query
            sites: Optional site restrictions
            max_results: Max results (default 5)

        Returns:
            Aggregated search results with metadata
        """
        from urllib.parse import quote

        encoded_query = quote(query)
        search_url = f"https://s.jina.ai/{encoded_query}"

        # Add site filters
        if sites:
            site_params = "&".join([f"site={site}" for site in sites])
            search_url = f"{search_url}?{site_params}"

        try:
            response = requests.get(
                search_url,
                headers={"Accept": "application/json"}
            )
            response.raise_for_status()

            data = response.json()

            return {
                'query': query,
                'results_count': 5,  # Jina returns top 5
                'content': data.get('content', ''),
                'title': data.get('title', ''),
                'timestamp': data.get('timestamp'),
                'success': True
            }

        except Exception as e:
            return {
                'query': query,
                'success': False,
                'error': str(e)
            }

    def augment_with_web_search(
        self,
        user_query: str,
        knowledge_base_results: List[str],
        search_sites: List[str] = None
    ) -> str:
        """
        Augment knowledge base with real-time web search.

        Args:
            user_query: Original user question
            knowledge_base_results: Results from vector DB
            search_sites: Sites to search

        Returns:
            Combined context for LLM
        """
        # Get real-time search results
        search_results = self.search_and_retrieve(
            user_query,
            sites=search_sites
        )

        if not search_results['success']:
            # Fall back to knowledge base only
            return "\n\n".join(knowledge_base_results)

        # Combine knowledge base + web search
        context_parts = [
            "# Knowledge Base Results:",
            *knowledge_base_results,
            "\n# Recent Web Search Results:",
            search_results['content']
        ]

        return "\n\n".join(context_parts)


# Example usage
search_rag = JinaSearchRAG()

# Simulate knowledge base results
kb_results = [
    "RAG combines retrieval with generation...",
    "Vector databases store embeddings..."
]

# Augment with web search
augmented_context = search_rag.augment_with_web_search(
    user_query="What are the latest RAG techniques in 2024?",
    knowledge_base_results=kb_results,
    search_sites=["arxiv.org", "openai.com", "anthropic.com"]
)

print("Augmented Context for LLM:")
print(augmented_context)
```

## Advanced Features

### PDF Processing

```python
import requests

def fetch_pdf_as_markdown(pdf_url: str) -> dict:
    """
    Convert PDF to LLM-friendly markdown.

    Args:
        pdf_url: Direct URL to PDF file

    Returns:
        JSON with extracted text in markdown
    """
    reader_url = f"https://r.jina.ai/{pdf_url}"

    response = requests.get(
        reader_url,
        headers={"Accept": "application/json"}
    )
    response.raise_for_status()

    return response.json()


# Example: Research paper
paper = fetch_pdf_as_markdown(
    "https://arxiv.org/pdf/2005.11401.pdf"  # RAG paper
)
print(f"Extracted {len(paper['content'])} characters from PDF")
```

### Handling Dynamic Content (SPAs)

```python
import requests

def fetch_spa_content(
    url: str,
    wait_selector: str = None,
    timeout: int = 30
) -> dict:
    """
    Fetch content from Single Page Applications.

    Args:
        url: SPA URL
        wait_selector: CSS selector to wait for
        timeout: Max wait time

    Returns:
        Rendered content
    """
    reader_url = f"https://r.jina.ai/{url}"

    headers = {
        "Accept": "application/json",
        "x-timeout": str(timeout)
    }

    if wait_selector:
        headers["x-wait-for-selector"] = wait_selector

    response = requests.get(reader_url, headers=headers)
    response.raise_for_status()

    return response.json()


# Example: Wait for content to load
spa_content = fetch_spa_content(
    "https://app.example.com/dashboard",
    wait_selector="#main-content",
    timeout=30
)
```

### Targeted Content Extraction

```python
import requests

def extract_specific_section(url: str, css_selector: str) -> dict:
    """
    Extract only specific section using CSS selector.

    Args:
        url: Target URL
        css_selector: CSS selector for target element

    Returns:
        Only the targeted content
    """
    reader_url = f"https://r.jina.ai/{url}"

    response = requests.get(
        reader_url,
        headers={
            "Accept": "application/json",
            "x-target-selector": css_selector
        }
    )
    response.raise_for_status()

    return response.json()


# Example: Extract only main article
article = extract_specific_section(
    "https://blog.example.com/post",
    css_selector="article.main-content"
)
```

### Streaming Large Documents

```python
import requests

def stream_large_document(url: str):
    """
    Stream large documents using Server-Sent Events.

    Args:
        url: Target URL

    Yields:
        Content chunks as they arrive
    """
    reader_url = f"https://r.jina.ai/{url}"

    response = requests.get(
        reader_url,
        headers={"Accept": "text/event-stream"},
        stream=True
    )
    response.raise_for_status()

    for line in response.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            if decoded_line.startswith('data: '):
                yield decoded_line[6:]  # Remove 'data: ' prefix


# Example usage
print("Streaming content...")
for chunk in stream_large_document("https://example.com/long-document"):
    print(chunk, end='', flush=True)
```

## Best Practices

### 1. Rate Limiting Strategy

```python
import time
from functools import wraps
from collections import deque

class RateLimiter:
    """Rate limiter for Jina API requests."""

    def __init__(self, max_requests: int, time_window: int):
        """
        Args:
            max_requests: Max requests allowed
            time_window: Time window in seconds
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = deque()

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()

            # Remove old requests outside time window
            while self.requests and self.requests[0] < now - self.time_window:
                self.requests.popleft()

            # Wait if at limit
            if len(self.requests) >= self.max_requests:
                sleep_time = self.time_window - (now - self.requests[0])
                if sleep_time > 0:
                    print(f"Rate limit reached, waiting {sleep_time:.2f}s...")
                    time.sleep(sleep_time)

            # Record this request
            self.requests.append(time.time())

            return func(*args, **kwargs)

        return wrapper


# Usage
@RateLimiter(max_requests=20, time_window=60)  # 20 RPM for free tier
def fetch_url(url: str) -> dict:
    reader_url = f"https://r.jina.ai/{url}"
    response = requests.get(reader_url, headers={"Accept": "application/json"})
    return response.json()
```

### 2. Caching Strategy

```python
import hashlib
import json
from pathlib import Path
from datetime import datetime, timedelta

class JinaCache:
    """Local cache for Jina Reader responses."""

    def __init__(self, cache_dir: str = "jina_cache", ttl_hours: int = 24):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.ttl = timedelta(hours=ttl_hours)

    def _get_cache_path(self, url: str) -> Path:
        """Generate cache file path from URL."""
        url_hash = hashlib.md5(url.encode()).hexdigest()
        return self.cache_dir / f"{url_hash}.json"

    def get(self, url: str) -> dict:
        """Get cached response if valid."""
        cache_path = self._get_cache_path(url)

        if not cache_path.exists():
            return None

        with open(cache_path, 'r') as f:
            cached = json.load(f)

        # Check TTL
        cached_time = datetime.fromisoformat(cached['cached_at'])
        if datetime.now() - cached_time > self.ttl:
            cache_path.unlink()  # Remove stale cache
            return None

        return cached['data']

    def set(self, url: str, data: dict):
        """Cache response."""
        cache_path = self._get_cache_path(url)

        cached = {
            'url': url,
            'cached_at': datetime.now().isoformat(),
            'data': data
        }

        with open(cache_path, 'w') as f:
            json.dump(cached, f, indent=2)

    def fetch_with_cache(self, url: str, force_refresh: bool = False) -> dict:
        """Fetch URL with caching."""
        if not force_refresh:
            cached = self.get(url)
            if cached:
                print(f"Cache hit for {url}")
                return cached

        # Fetch fresh
        reader_url = f"https://r.jina.ai/{url}"
        response = requests.get(reader_url, headers={"Accept": "application/json"})
        response.raise_for_status()

        data = response.json()
        self.set(url, data)

        return data


# Usage
cache = JinaCache(ttl_hours=24)
content = cache.fetch_with_cache("https://example.com/article")
```

### 3. Error Handling

```python
import requests
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JinaReaderClient:
    """Robust Jina Reader client with error handling."""

    def __init__(self, max_retries: int = 3, timeout: int = 30):
        self.max_retries = max_retries
        self.timeout = timeout

    def fetch(
        self,
        url: str,
        headers: Optional[dict] = None
    ) -> Optional[dict]:
        """
        Fetch URL with retry logic and error handling.

        Args:
            url: Target URL
            headers: Optional custom headers

        Returns:
            Response dict or None on failure
        """
        reader_url = f"https://r.jina.ai/{url}"
        default_headers = {"Accept": "application/json"}

        if headers:
            default_headers.update(headers)

        for attempt in range(self.max_retries):
            try:
                logger.info(f"Fetching {url} (attempt {attempt + 1}/{self.max_retries})")

                response = requests.get(
                    reader_url,
                    headers=default_headers,
                    timeout=self.timeout
                )
                response.raise_for_status()

                return response.json()

            except requests.exceptions.Timeout:
                logger.warning(f"Timeout on attempt {attempt + 1}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff

            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:  # Rate limit
                    logger.warning("Rate limit exceeded, waiting...")
                    time.sleep(60)  # Wait 1 minute
                elif e.response.status_code >= 500:  # Server error
                    logger.warning(f"Server error: {e}")
                    if attempt < self.max_retries - 1:
                        time.sleep(5)
                else:
                    logger.error(f"HTTP error: {e}")
                    return None

            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                return None

        logger.error(f"Failed to fetch {url} after {self.max_retries} attempts")
        return None


# Usage
client = JinaReaderClient(max_retries=3, timeout=30)
result = client.fetch("https://example.com/article")
```

## Rate Limits & Performance

### Rate Limits by Tier

| Tier | Rate Limit | Latency | Best For |
|------|-----------|---------|----------|
| Free | 20 RPM | ~7.9s avg | Testing, small projects |
| API Key | 500 RPM | ~5-7s | Production apps |
| Premium | 5,000 RPM | ~3-5s | Large-scale RAG systems |

### Caching Behavior

- **Cache Duration**: 5 minutes (300 seconds) for identical URLs
- **Bypass Cache**: Use `x-no-cache: true` header
- **Custom Cache TTL**: Use `x-cache-tolerance` header (in seconds)

### Token Counting

- Tokens counted based on **output response length**
- Each search request: minimum **10,000 tokens**
- Image captions add to token count

### Performance Tips

1. **Use caching**: Implement local cache for frequently accessed URLs
2. **Batch wisely**: Respect rate limits with delays between requests
3. **Target selectors**: Use `x-target-selector` to reduce content size
4. **Disable image captions**: Only enable when needed (performance cost)
5. **Monitor timeouts**: Adjust `x-timeout` based on page complexity
6. **Stream large docs**: Use `Accept: text/event-stream` for large pages

## Sources

- [Jina Reader API Official Documentation](https://jina.ai/reader/)
- [Jina Reader GitHub Repository](https://github.com/jina-ai/reader)
- [ReaderLM-v2 Model Documentation](https://jina.ai/models/ReaderLM-v2/)
- [Jina AI Reader Connector - Airbyte](https://docs.airbyte.com/integrations/sources/jina-ai-reader)

---

**Last Updated**: January 2026

For questions or issues, refer to the [official documentation](https://jina.ai/reader/) or [GitHub repository](https://github.com/jina-ai/reader).
