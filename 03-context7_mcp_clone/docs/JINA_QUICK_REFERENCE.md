# Jina Reader API - Quick Reference Card

## URL Encoding Quick Reference

### Common Characters to Encode

| Character | Encoded | Example |
|-----------|---------|---------|
| Space | `%20` | `What is AI?` → `What%20is%20AI%3F` |
| `?` | `%3F` | |
| `&` | `%26` | |
| `=` | `%3D` | |
| `/` (in query) | `%2F` | |
| `:` | `%3A` | `https:` → `https%3A` |

### Quick Encode Methods

**Using Python:**
```bash
# Command line
python3 -c "from urllib.parse import quote; print(quote('What is RAG in AI?'))"
# Output: What%20is%20RAG%20in%20AI%3F

# In script
from urllib.parse import quote
encoded = quote("https://example.com/path with spaces")
```

**Using Online Tools:**
- https://www.urlencoder.org/
- https://meyerweb.com/eric/tools/dencoder/

## Common Use Cases

### 1. Basic URL Reading (No Auth Required)

```bash
# Simple URL
curl "https://r.jina.ai/https://example.com"

# Wikipedia article
curl "https://r.jina.ai/https://en.wikipedia.org/wiki/Artificial_intelligence"

# Blog post
curl "https://r.jina.ai/https://blog.openai.com/latest-post"
```

### 2. JSON Output (Recommended for Programming)

```bash
curl -H "Accept: application/json" \
  "https://r.jina.ai/https://example.com"
```

**Response Format:**
```json
{
  "url": "https://example.com",
  "title": "Page Title",
  "content": "Markdown content here...",
  "timestamp": "2026-01-04T12:00:00Z"
}
```

### 3. Image Captions

```bash
curl -H "x-with-generated-alt: true" \
  "https://r.jina.ai/https://example.com/article-with-images"
```

### 4. Target Specific Section

```bash
# Extract only the main article
curl -H "x-target-selector: article.main" \
  "https://r.jina.ai/https://example.com"

# Extract specific div
curl -H "x-target-selector: #content" \
  "https://r.jina.ai/https://example.com"
```

### 5. Dynamic Content (SPAs)

```bash
# Wait for content to load
curl -H "x-wait-for-selector: .loaded-content" \
  -H "x-timeout: 30" \
  "https://r.jina.ai/https://app.example.com"
```

### 6. PDF Reading

```bash
# Direct PDF URL
curl "https://r.jina.ai/https://arxiv.org/pdf/2005.11401.pdf"
```

### 7. Streaming Large Documents

```bash
curl -H "Accept: text/event-stream" \
  "https://r.jina.ai/https://example.com/long-document"
```

## Python Quick Examples

### Simple Fetch
```python
import requests

url = "https://r.jina.ai/https://example.com"
response = requests.get(url, headers={"Accept": "application/json"})
result = response.json()

# Important: Extract 'data' field from response
data = result['data']

print(f"Title: {data['title']}")
print(f"Content: {data['content'][:500]}...")
print(f"Tokens: {data['usage']['tokens']}")
```

### With Error Handling
```python
import requests

def fetch_url(target_url: str) -> dict:
    try:
        reader_url = f"https://r.jina.ai/{target_url}"
        response = requests.get(
            reader_url,
            headers={"Accept": "application/json"},
            timeout=30
        )
        response.raise_for_status()

        # Extract 'data' field from nested response
        result = response.json()
        return result['data']
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

# Usage
data = fetch_url("https://en.wikipedia.org/wiki/Python_(programming_language)")
if data:
    print(f"Title: {data['title']}")
    print(f"Tokens: {data['usage']['tokens']}")
```

### Batch Processing
```python
import requests
from concurrent.futures import ThreadPoolExecutor

def fetch_url(url: str) -> dict:
    reader_url = f"https://r.jina.ai/{url}"
    response = requests.get(reader_url, headers={"Accept": "application/json"})
    result = response.json()
    return result['data']  # Extract 'data' field

urls = [
    "https://docs.python.org/3/",
    "https://fastapi.tiangolo.com/",
    "https://flask.palletsprojects.com/"
]

with ThreadPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(fetch_url, urls))

for data in results:
    print(f"- {data['title']} ({data['usage']['tokens']} tokens)")
```

## Headers Reference

### Must-Know Headers

| Header | Value | Purpose |
|--------|-------|---------|
| `Accept` | `application/json` | Get JSON instead of markdown |
| `Accept` | `text/event-stream` | Stream response |
| `x-with-generated-alt` | `true` | Add AI image captions |
| `x-respond-with` | `markdown`/`html`/`text`/`screenshot` | Output format |
| `x-target-selector` | CSS selector | Extract specific element |
| `x-wait-for-selector` | CSS selector | Wait for dynamic content |
| `x-timeout` | seconds | Max wait time |
| `x-no-cache` | `true` | Bypass cache |
| `Authorization` | `Bearer API_KEY` | For Search API |

## Troubleshooting

### Error: "Malformed input to a URL function"
**Cause:** Unencoded special characters in URL

**Fix:**
```bash
# ❌ Wrong
curl "https://r.jina.ai/https://example.com/path with spaces"

# ✅ Correct
curl "https://r.jina.ai/https://example.com/path%20with%20spaces"

# Or use Python to encode
python3 -c "from urllib.parse import quote; print('https://r.jina.ai/' + quote('https://example.com/path with spaces'))"
```

### Error: "Authentication is required"
**Cause:** Using Search API (`s.jina.ai`) without API key

**Fix:**
```bash
# Option 1: Get API key and use it
curl -H "Authorization: Bearer YOUR_API_KEY" \
  "https://s.jina.ai/query"

# Option 2: Use Reader API instead
curl "https://r.jina.ai/https://www.google.com/search?q=your+query"
```

### Error: Timeout
**Cause:** Page takes too long to load

**Fix:**
```bash
# Increase timeout
curl -H "x-timeout: 60" \
  "https://r.jina.ai/https://slow-loading-site.com"
```

### Error: Content incomplete
**Cause:** JavaScript-rendered content not loaded

**Fix:**
```bash
# Wait for specific element
curl -H "x-wait-for-selector: #main-content" \
  -H "x-timeout: 30" \
  "https://r.jina.ai/https://spa-website.com"
```

## Rate Limits

| Tier | Requests/Min | Best For |
|------|-------------|----------|
| Free | 20 RPM | Testing, small projects |
| API Key | 500 RPM | Production apps |
| Premium | 5,000 RPM | Large-scale systems |

## Integration Patterns

### Pattern 1: Simple RAG
```python
# 1. Fetch documentation
docs = fetch_url("https://docs.example.com")

# 2. Chunk content
chunks = [docs['content'][i:i+1000] for i in range(0, len(docs['content']), 800)]

# 3. Create embeddings (use your preferred model)
# embeddings = model.encode(chunks)

# 4. Store in vector DB
# vector_db.add(chunks, embeddings)
```

### Pattern 2: Real-time Web Augmentation
```python
# 1. Search your vector DB
# kb_results = vector_db.search(user_query)

# 2. Augment with fresh web content
web_result = fetch_url(f"https://example.com/latest")

# 3. Combine and send to LLM
# context = kb_results + web_result['content']
# response = llm.generate(context, user_query)
```

### Pattern 3: Documentation Indexing
```python
urls = ["https://docs.library.com/page1", "https://docs.library.com/page2"]

for url in urls:
    data = fetch_url(url)
    # Process and index
    # index.add(data['content'], metadata={'url': url, 'title': data['title']})
```

## Testing Your Setup

Run this quick test:

```bash
# Test 1: Basic fetch
curl "https://r.jina.ai/https://example.com" | head -n 20

# Test 2: JSON output
curl -H "Accept: application/json" "https://r.jina.ai/https://example.com" | python3 -m json.tool

# Test 3: Wikipedia (real content)
curl "https://r.jina.ai/https://en.wikipedia.org/wiki/Python_(programming_language)" | grep -i "python is"
```

## Resources

- **Official Docs**: https://jina.ai/reader/
- **GitHub**: https://github.com/jina-ai/reader
- **API Status**: https://status.jina.ai/
- **Get API Key**: https://jina.ai/ (sign up)

---

**Pro Tip**: Always use `Accept: application/json` header in production code for reliable parsing!
