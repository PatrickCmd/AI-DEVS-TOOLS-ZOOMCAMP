# Multi-Term Search Implementation

## Overview

The FreeCodeCamp MCP server now supports **multi-term search queries**, allowing users to search for articles and videos using multiple topics/keywords at once.

## How It Works

### Query Parsing
The search query is automatically split into individual terms:
```python
query = "react python javascript"
# Splits into: ["react", "python", "javascript"]
```

### Two Matching Modes

#### 1. ANY Match (Default - `match_all_terms=False`)
Finds content containing **any** of the search terms.

**Example:**
```python
query = "react python javascript"
# Finds articles about React OR Python OR JavaScript
```

**Use Case:** Broad search across multiple topics
- "Find articles about machine learning, ai, or python"
- "Show me content on react, vue, or angular"

#### 2. ALL Match (`match_all_terms=True`)
Finds content containing **all** of the search terms.

**Example:**
```python
query = "react hooks"
match_all_terms = True
# Finds articles that contain BOTH "react" AND "hooks"
```

**Use Case:** Precise search for specific topic combinations
- "Find articles about both javascript and next.js"
- "Show me content covering react and hooks"

## API Usage

### News Search

```python
fcc_news_search(
    query="react python javascript",
    max_results=5,
    include_content=False,
    match_all_terms=False  # ANY match (default)
)
```

#### Parameters:
- `query` (str): Search term(s). Multiple terms separated by spaces.
- `max_results` (int, optional): Maximum results to return. Default: 3
- `include_content` (bool, optional): Include full article content in markdown. Default: False
- `match_all_terms` (bool, optional): If True, ALL terms must match. If False, ANY term matches. Default: False

### YouTube Search

```python
fcc_youtube_search(
    query="python tutorial beginner",
    max_results=3,
    include_description=True,
    match_all_terms=False  # ANY match (default)
)
```

#### Parameters:
- `query` (str): Search term(s). Multiple terms separated by spaces.
- `max_results` (int, optional): Maximum results to return. Default: 3
- `include_description` (bool, optional): Include video descriptions. Default: True
- `match_all_terms` (bool, optional): If True, ALL terms must match. If False, ANY term matches. Default: False

## Search Behavior Comparison

### Before Enhancement
```python
# Only exact phrase matching
query = "react hooks"
# Searched for: "react hooks" as one phrase
# Result: Often 0 results (phrase must appear exactly)
```

### After Enhancement

#### ANY Match
```python
query = "react hooks"
match_all_terms = False
# Searched for: "react" OR "hooks"
# Result: All articles mentioning either term
```

#### ALL Match
```python
query = "react hooks"
match_all_terms = True
# Searched for: "react" AND "hooks"
# Result: Only articles mentioning both terms
```

## Example Queries

### Broad Topic Search (ANY)
```python
# Find articles about any of these topics
queries = [
    "react python javascript",
    "machine learning ai data science",
    "css html bootstrap tailwind",
]

for query in queries:
    results = fcc_news_search(query, max_results=5, match_all_terms=False)
    # Returns articles matching ANY of the terms
```

### Specific Topic Combination (ALL)
```python
# Find articles covering specific combinations
queries = [
    "react hooks",           # Articles about React Hooks
    "javascript next.js",    # Articles about Next.js and JavaScript
    "python machine learning", # Articles about Python ML
]

for query in queries:
    results = fcc_news_search(query, max_results=5, match_all_terms=True)
    # Returns only articles matching ALL terms
```

## Test Results

### Test 1: Single Term
```
Query: "react"
Results: 2 articles
- How to Build Your First Shopify App
- How to Not Be Overwhelmed by AI
```

### Test 2: Multiple Terms (ANY)
```
Query: "react python javascript"
Mode: ANY
Results: 5 articles
- How to Run an LLM Locally (Python)
- How to Build an In-Memory Rate Limiter (JavaScript, Next.js)
- First developer job at age 38 (Podcast)
- How to Build and Deploy an AI Agent (Python, FastAPI)
- How to Build Your First Shopify App (JavaScript)
```

### Test 3: Multiple Terms (ALL)
```
Query: "javascript next.js"
Mode: ALL
Results: 1 article
- How to Build an In-Memory Rate Limiter in Next.js
  (Contains both "javascript" AND "next.js")
```

### Test 4: Topic Combination (ANY)
```
Query: "machine learning ai python"
Mode: ANY
Results: 5 articles
- How to Run an LLM Locally
- How to Build a Local-First CLI
- How to Build an In-Memory Rate Limiter
- First developer job at age 38
- How to Build and Deploy an AI Agent
```

### Test 5: Precise Search (ALL)
```
Query: "react hooks"
Mode: ALL
Results: 2 articles
- How to Build Your First Shopify App
- How to Not Be Overwhelmed by AI
(Both contain "react" AND "hooks" in their content)
```

## Search Scope

The search looks in **multiple fields**:

### For News Articles:
- ✅ Title
- ✅ Description
- ✅ Full article content
- ✅ Categories/Tags

### For YouTube Videos:
- ✅ Video title
- ✅ Video description

## Agent Usage Examples

### Example 1: Explore Multiple Topics
```
User: "Show me articles about react, vue, or angular"

Agent uses: fcc_news_search("react vue angular", match_all_terms=False)

Result: Returns articles about any of these frameworks
```

### Example 2: Specific Topic Combination
```
User: "Find tutorials that cover both python and machine learning"

Agent uses: fcc_news_search("python machine learning", match_all_terms=True)

Result: Returns only articles covering both topics
```

### Example 3: Broad Research
```
User: "I'm interested in AI, machine learning, and data science"

Agent uses: fcc_news_search("ai machine learning data science", max_results=10, match_all_terms=False)

Result: Comprehensive list of AI-related content
```

## Performance Benefits

### More Flexible
- **Before**: "react hooks" → 0 results (exact phrase not found)
- **After (ANY)**: "react hooks" → Multiple results (articles about either topic)
- **After (ALL)**: "react hooks" → Precise results (articles about both)

### Better Discovery
- Users can explore multiple topics in one query
- Easier to find related content
- More natural search behavior

### Intelligent Matching
- Searches across title, content, and categories
- Finds relevant articles even if exact terms don't appear in title
- Category-based matching improves accuracy

## Implementation Details

### Term Splitting
```python
search_terms = [term.strip().lower() for term in query.split() if term.strip()]
```

### ANY Match Logic
```python
is_match = any(term in searchable_text for term in search_terms)
```

### ALL Match Logic
```python
is_match = all(term in searchable_text for term in search_terms)
```

### Backward Compatibility
```python
# Single term queries work exactly as before
if len(search_terms) <= 1:
    search_terms = [query.lower()]
    match_all_terms = False
```

## When to Use Each Mode

### Use ANY Match When:
- ✅ Exploring multiple topics
- ✅ Broad research
- ✅ Finding content across different areas
- ✅ User is unsure of exact topic
- ✅ Looking for alternatives

**Examples:**
- "react vue angular" (find frontend frameworks)
- "python javascript rust" (find programming languages)
- "ai ml data science" (find AI-related content)

### Use ALL Match When:
- ✅ Looking for specific combinations
- ✅ Need precise results
- ✅ Researching intersection of topics
- ✅ Advanced/specific queries

**Examples:**
- "react hooks" (React Hooks specifically)
- "python machine learning" (Python ML)
- "javascript typescript" (JS with TS)

## Future Enhancements

Potential improvements:
- 🔲 Weighted term matching (prioritize certain terms)
- 🔲 Synonym support ("ml" → "machine learning")
- 🔲 Phrase detection ("react hooks" as a phrase)
- 🔲 Relevance scoring
- 🔲 Term highlighting in results

## Files Modified

- ✅ [feed_deployment.py](feed_deployment.py) - Added multi-term search logic
- ✅ [test_multiterm_direct.py](test_multiterm_direct.py) - Comprehensive tests
- ✅ [test_multi_term_search.py](test_multi_term_search.py) - Comparison tests

---

**Status**: ✅ IMPLEMENTED
**Date**: 2026-01-10
**Feature**: Multi-term search with ANY/ALL matching modes
**Backward Compatible**: ✅ Yes (single terms work as before)
