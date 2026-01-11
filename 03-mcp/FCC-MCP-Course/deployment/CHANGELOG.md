# Changelog

All notable changes to the FreeCodeCamp MCP project.

---

## [2026-01-11] - Empty Response Fix

### Fixed
- **Empty responses in multi-turn conversations**
  - Root cause: Model hitting `max_output_tokens` limit before completing text synthesis
  - Tool calls were consuming tokens, leaving none for final response
  - Added fallback logic to extract tool outputs when synthesis fails
  - Added warning when hitting token limit

### Changed
- **Increased default token limits** across all use cases:
  - Default: `1000` → `2000` tokens
  - Basic usage demo: `1000` → `2000` tokens
  - Multi-turn demo: `1000` → `2500` tokens
  - Interactive demo: `1500` → `3000` tokens

- **Enhanced response handling**:
  - Detects incomplete responses (`incomplete_details.reason`)
  - Extracts tool call outputs as fallback when `output_text` is empty
  - Provides user-friendly warnings about token limits

### Added
- Created `debug_response.py` - Debug script to inspect response object structure
- Created `EMPTY_RESPONSES_FIX.md` - Comprehensive documentation on the issue and solution
- Added incomplete response detection in `query()` method

### Testing
- ✅ Multi-turn conversations now return full responses
- ✅ Query 1: 1985 tokens - Complete programming guide
- ✅ Query 2: 1802 tokens - Detailed Python learning path
- ✅ Query 3: 1663 tokens - List of Python tutorials
- ✅ No more empty responses

---

## [2026-01-11] - GPT-5 Compatibility Fix

### Fixed
- **Removed temperature parameter** from `agent_client_advanced.py`
  - GPT-5 models (gpt-5-mini, gpt-5) do not support the `temperature` parameter
  - This was causing 400 errors: "Unsupported parameter: 'temperature'"

- **Updated parameter naming** from `max_tokens` to `max_output_tokens`
  - GPT-5 models use `max_output_tokens` instead of `max_tokens`
  - Ensures compatibility with latest OpenAI API changes

### Changed
- Constructor signature in `AdvancedFCCAgentClient`:
  - Removed: `temperature: float = 0.7`
  - Changed: `max_tokens: int = 1000` → `max_output_tokens: int = 2000`

- Updated all API calls to exclude temperature parameter
- Updated status displays to show `Max Output Tokens` instead of `Temperature`
- Updated demo functions to use `max_output_tokens` parameter

### Added
- Created `test_gpt5_fix.py` - Test script to verify GPT-5 compatibility
- Created `GPT5_COMPATIBILITY.md` - Comprehensive documentation on the fix

### Testing
- ✅ Tested with `gpt-5-mini` model
- ✅ No parameter errors
- ✅ MCP server connection successful
- ✅ Tool calls working properly
- ✅ Response generation working

---

## [2026-01-10] - Multi-Term Search Implementation

### Added
- **Multi-term search support** in both `fcc_news_search` and `fcc_youtube_search`
  - Split queries into individual terms (e.g., "react python javascript")
  - ANY mode (default): finds content with any search term
  - ALL mode (`match_all_terms=True`): finds content with all search terms

- **New parameter**: `match_all_terms` (bool) in both search functions
  - Default: `False` (ANY match)
  - Set to `True` for precise matching (ALL terms must be present)

### Changed
- Search now looks across multiple fields:
  - News: title, description, content, categories
  - YouTube: title, description

- Improved search flexibility and recall

### Documentation
- Created `MULTI_TERM_SEARCH.md` - Comprehensive guide
- Created `test_multiterm_direct.py` - Direct implementation tests
- Created `test_multi_term_search.py` - Comparison tests

### Test Results
- Single term "react": 2 results
- Multi-term ANY "react python javascript": 5 results
- Multi-term ALL "javascript next.js": 1 precise result
- Topic combination "machine learning ai python": 5 results

---

## [2026-01-10] - Enhanced RSS Feed Parsing

### Added
- **Full article content** extraction in markdown format
  - HTML to Markdown conversion using `markdownify` library
  - Configurable via `include_content` parameter

- **Rich metadata extraction**:
  - Categories/tags from RSS feed
  - Publication dates (formatted: "January 09, 2026 at 07:24 PM UTC")
  - Authors/creators
  - Featured images (media:content)

- **YouTube enhancements**:
  - Video descriptions with HTML to Markdown conversion
  - Thumbnails
  - Formatted publication dates

### Changed
- Both `fcc_news_search` and `fcc_youtube_search` now return comprehensive metadata
- Search spans across all extracted fields (title, description, content, categories)

### Dependencies
- Added `markdownify>=0.11.6` to requirements.txt

### Documentation
- Created `ENHANCED_FEED_PARSING.md` - Complete documentation with examples

### Test Results
- Content extraction: 29,071 chars HTML → 20,835 chars Markdown
- Categories: ["Next.js", "ratelimit", "JavaScript"]
- Author: "Orim Dominic Adah"
- Published: "January 09, 2026 at 07:24 PM UTC"

---

## [2026-01-09] - FastMCP Cloud Deployment

### Added
- **Cloud deployment** to FastMCP Cloud
  - Public URL: `https://freedcodecamp-content.fastmcp.app/mcp`
  - No localhost limitations
  - Compatible with OpenAI Responses API

### Changed
- Updated `agent_client.py` to use cloud deployment by default
- Updated `agent_client_advanced.py` to use cloud deployment by default
- Simplified MCP tool configuration:
  - Changed from nested `require_approval` to flat `"require_approval": "never"`
  - Updated `server_label` to `"freedcodecamp-content"`

### Fixed
- **Resolved 424 Failed Dependency error**
  - Root cause: OpenAI Responses API cannot connect to localhost servers
  - Solution: Deploy to publicly accessible URL

### Documentation
- Created `CLOUD_DEPLOYMENT_SUCCESS.md` - Deployment guide and troubleshooting

### Test Results
- ✅ Successfully connected to cloud deployment
- ✅ 1245 character response received
- ✅ No 424 errors

---

## [2026-01-09] - Initial MCP Server and Agent Clients

### Added
- **MCP Server** (`feed_deployment.py`)
  - HTTP transport support
  - Tools: `fcc_news_search`, `fcc_youtube_search`, `fcc_secret_message`
  - RSS feed parsing with feedparser

- **Basic Agent Client** (`agent_client.py`)
  - OpenAI Responses API integration
  - MCP type tool support
  - Interactive mode

- **Advanced Agent Client** (`agent_client_advanced.py`)
  - Conversation history tracking
  - Token usage statistics
  - Cost estimation
  - Export to JSON
  - Interactive chat mode

### Dependencies
- fastmcp>=2.14.2
- feedparser>=6.0.12
- openai
- python-dotenv

### Documentation
- Created `README.md` - Quick start guide
- Created `QUICKSTART.md` - Detailed usage guide
- Created `quickstart.sh` - Setup script

### Examples
- Created `example_usage.py` - 7 usage examples
- Created `test_cloud_deployment.py` - Cloud deployment tests

---

## Model Compatibility

| Model | Status | Notes |
|-------|--------|-------|
| **gpt-5-mini** | ✅ Fully Supported | Recommended (fast, cost-effective) |
| **gpt-5** | ✅ Fully Supported | No temperature parameter |
| **gpt-4.1** | ✅ Fully Supported | Supports temperature |
| **gpt-4.5** | ✅ Fully Supported | Supports temperature |
| **gpt-4o** | ⚠️ May work | Older model, use with caution |
| **gpt-4o-mini** | ⚠️ May work | Older model, use with caution |

---

## Repository Structure

```
deployment/
├── feed_deployment.py          # MCP server with HTTP transport
├── agent_client.py             # Basic OpenAI agent client
├── agent_client_advanced.py    # Advanced client with conversation management
├── requirements.txt            # Server dependencies
├── requirements_client.txt     # Client dependencies
├── .env                        # Environment configuration
│
├── test_cloud_deployment.py    # Cloud deployment tests
├── test_enhanced_feed.py       # Enhanced feed parsing tests
├── test_multiterm_direct.py    # Multi-term search tests
├── test_multi_term_search.py   # Search comparison tests
├── test_gpt5_fix.py           # GPT-5 compatibility tests
│
├── README.md                   # MCP fundamentals documentation
├── QUICKSTART.md              # Quick start guide
├── CLOUD_DEPLOYMENT_SUCCESS.md # Cloud deployment guide
├── ENHANCED_FEED_PARSING.md   # Feed parsing documentation
├── MULTI_TERM_SEARCH.md       # Multi-term search guide
├── GPT5_COMPATIBILITY.md      # GPT-5 compatibility documentation
└── CHANGELOG.md               # This file
```

---

## Contributors

- Patrick Walukagga (@patrickwalukagga)
- Claude Sonnet 4.5 (AI Assistant)

---

**For more information**, see the main [README.md](README.md).
