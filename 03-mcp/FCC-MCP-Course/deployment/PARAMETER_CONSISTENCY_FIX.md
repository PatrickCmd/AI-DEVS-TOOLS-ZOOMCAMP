# Parameter Consistency Fix

## The Problem

Users were experiencing validation errors when the AI model called `fcc_youtube_search`:

```json
{
  "arguments": {
    "query": "django react",
    "max_results": "3",
    "include_content": false,  // ❌ Wrong parameter for YouTube search
    "include_description": true,
    "match_all_terms": false
  },
  "name": "fcc_youtube_search"
}
```

**Error Message**:
```
1 validation error for call[fcc_youtube_search]
include_content
  Unexpected keyword argument [type=unexpected_keyword_argument, input_value=False, input_type=bool]
```

## Root Cause

The two search functions had **inconsistent parameter names** for including additional content:

| Function | Parameter Name | Purpose |
|----------|---------------|---------|
| `fcc_news_search` | `include_content` | Include article content |
| `fcc_youtube_search` | `include_description` | Include video descriptions |

**Why This Caused Errors**:

1. AI models learned that `fcc_news_search` uses `include_content`
2. When calling `fcc_youtube_search`, the model sometimes incorrectly used `include_content` instead of `include_description`
3. The function rejected `include_content` as an "unexpected keyword argument"
4. This happened intermittently depending on the AI's token context and pattern matching

## The Solution

**Standardized parameter naming across both functions** to use `include_content`:

### Before (Inconsistent)

```python
# News search - uses include_content ✅
@mcp.tool()
def fcc_news_search(
    query: str,
    max_results: int = 3,
    include_content: bool = False,  # ← include_content
    match_all_terms: bool = False
):
    ...

# YouTube search - uses include_description ❌
@mcp.tool()
def fcc_youtube_search(
    query: str,
    max_results: int = 3,
    include_description: bool = True,  # ← include_description (different!)
    match_all_terms: bool = False
):
    ...
```

### After (Consistent)

```python
# News search - uses include_content ✅
@mcp.tool()
def fcc_news_search(
    query: str,
    max_results: int = 3,
    include_content: bool = False,  # ← include_content
    match_all_terms: bool = False
):
    ...

# YouTube search - NOW uses include_content ✅
@mcp.tool()
def fcc_youtube_search(
    query: str,
    max_results: int = 3,
    include_content: bool = True,  # ← include_content (now consistent!)
    match_all_terms: bool = False
):
    ...
```

## Changes Made

### File: [feed_deployment.py](feed_deployment.py)

**Line 125**: Changed function signature
```python
# Before
def fcc_youtube_search(query: str, max_results: int = 3, include_description: bool = True, ...):

# After
def fcc_youtube_search(query: str, max_results: int = 3, include_content: bool = True, ...):
```

**Line 138**: Updated parameter documentation
```python
# Before
Args:
    include_description (bool, optional): Include video descriptions. Defaults to True.

# After
Args:
    include_content (bool, optional): Include video descriptions. Defaults to True.
```

**Line 206**: Updated parameter usage in code
```python
# Before
if include_description and description:
    result["description"] = description

# After
if include_content and description:
    result["description"] = description
```

## Why `include_content` Instead of `include_description`?

We chose to standardize on `include_content` for these reasons:

1. **More Generic**: "content" applies to both articles and videos
2. **Consistent Semantics**: In both cases, we're including additional content beyond the basic metadata
3. **Less Confusion**: One parameter name to remember across all search functions
4. **Better AI Compatibility**: Reduces cognitive load for AI models using these tools
5. **Future-Proof**: If we add more search functions (podcasts, courses), `include_content` works for all

## Testing

### Test Script: [test_parameter_consistency.py](test_parameter_consistency.py)

```bash
python test_parameter_consistency.py
```

**Test Results**: ✅ All tests passed

```
TEST 1: fcc_news_search with include_content=True
✓ Found 2 articles
✓ Content included: 203 chars

TEST 2: fcc_news_search with include_content=False
✓ Found 2 articles
✓ No content (correct)

TEST 3: fcc_youtube_search with include_content=True
✓ Found 2 videos
✓ Description included: 136 chars

TEST 4: fcc_youtube_search with include_content=False
✓ Found 2 videos
✓ No description (correct)
```

## Benefits

### 1. No More Validation Errors

**Before**:
```
Error: Unexpected keyword argument 'include_content'
```

**After**:
```
✅ Request succeeds - parameter recognized
```

### 2. Improved AI Model Reliability

- AI models can use the same parameter for both functions
- Reduces confusion and incorrect tool calls
- More predictable behavior across queries

### 3. Better Developer Experience

**Before**:
```python
# Developer has to remember two different names
results1 = fcc_news_search(query, include_content=True)
results2 = fcc_youtube_search(query, include_description=True)  # Different!
```

**After**:
```python
# Same parameter name for both
results1 = fcc_news_search(query, include_content=True)
results2 = fcc_youtube_search(query, include_content=True)  # Consistent!
```

### 4. Easier Documentation

- One concept to explain instead of two
- Simpler examples
- Less cognitive overhead

## API Usage Examples

### News Search

```python
# Without content (metadata only)
results = fcc_news_search(
    query="python django",
    max_results=5,
    include_content=False  # Just title, URL, author, categories
)

# With full article content
results = fcc_news_search(
    query="python django",
    max_results=5,
    include_content=True  # Includes full article in markdown
)
```

### YouTube Search

```python
# Without descriptions (metadata only)
results = fcc_youtube_search(
    query="django react",
    max_results=3,
    include_content=False  # Just title, URL, thumbnail
)

# With video descriptions
results = fcc_youtube_search(
    query="django react",
    max_results=3,
    include_content=True  # Includes video descriptions
)
```

### Both Functions (Consistent API)

```python
# Search both news and YouTube with same parameters
def search_all(query: str, with_content: bool = True):
    news = fcc_news_search(
        query=query,
        include_content=with_content  # ← Same parameter
    )

    videos = fcc_youtube_search(
        query=query,
        include_content=with_content  # ← Same parameter
    )

    return {"news": news, "videos": videos}
```

## Migration Guide

### For Existing Code

If you have code using the old `include_description` parameter:

**Old Code**:
```python
fcc_youtube_search(query="python", include_description=True)
```

**New Code**:
```python
fcc_youtube_search(query="python", include_content=True)
```

### For AI Prompts

If you have system prompts or instructions mentioning the old parameter:

**Old Instructions**:
```
Use include_description=True for YouTube searches to get video descriptions
```

**New Instructions**:
```
Use include_content=True for both news and YouTube searches to get full content
```

## Backward Compatibility

⚠️ **Breaking Change**: This is a breaking change if you were using `include_description` directly.

**Mitigation**:
- This is an MCP server, so clients get updated tool schemas automatically
- AI models will learn the new parameter from the schema
- No code changes needed for OpenAI Responses API users
- Manual API users need to update parameter names

## Related Issues

### Issue: "Some queries work, others fail with validation error"

**Cause**: Inconsistent parameter naming causing AI model confusion

**Solution**: ✅ Fixed with parameter consistency

### Issue: "AI sometimes forgets to include descriptions"

**Cause**: Model confused about which parameter to use

**Solution**: ✅ Fixed - model now uses consistent `include_content` parameter

## Deployment

After making this change:

1. **Redeploy to FastMCP Cloud**:
   ```bash
   fastmcp deploy feed_deployment.py
   ```

2. **Verify tool schema**:
   ```bash
   # Check that both functions show include_content in their schema
   curl https://freedcodecamp-content.fastmcp.app/mcp/list_tools
   ```

3. **Test with AI client**:
   ```bash
   python agent_client_advanced.py
   # Try: "Find django react tutorials on YouTube"
   ```

## Summary

**Problem**: Inconsistent parameter names causing validation errors
**Root Cause**: `include_content` (news) vs `include_description` (YouTube)
**Solution**: Standardized both to use `include_content`
**Result**: ✅ No more validation errors, better AI reliability

**Key Takeaway**: When building MCP tools, use **consistent parameter names** across similar functions to avoid confusing AI models and improve developer experience.

---

**Last Updated**: January 2026
**Status**: ✅ Fixed and Tested
**Affects**: feed_deployment.py
**Related**: CHANGELOG.md, ENHANCED_FEED_PARSING.md
