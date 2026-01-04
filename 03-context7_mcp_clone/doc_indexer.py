"""
Documentation Indexer Module

This module provides functionality to:
1. Download GitHub repositories as ZIP files with caching
2. Extract markdown files from ZIP archives
3. Create and manage MinSearch indexes for documentation search

Author: AI Dev Tools Zoomcamp
Date: January 2026
"""

import os
import zipfile
from pathlib import Path
from typing import List, Dict, Optional
import requests
from minsearch import Index


class DocumentationIndexer:
    """
    A class to handle documentation indexing for GitHub repositories.

    Features:
    - Downloads and caches GitHub repos as ZIP files
    - Extracts markdown (.md and .mdx) files
    - Creates searchable indexes using MinSearch
    - Supports lazy loading for better performance
    """

    def __init__(self, cache_dir: str = "data"):
        """
        Initialize the DocumentationIndexer.

        Args:
            cache_dir: Directory to store cached ZIP files (default: "data")
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self._index: Optional[Index] = None
        self._documents: List[Dict[str, str]] = []

    def download_repo(self, repo_url: str, cache_filename: str) -> Path:
        """
        Download GitHub repository as ZIP if not already cached.

        Args:
            repo_url: GitHub archive URL (e.g., 'https://github.com/user/repo/archive/refs/heads/main.zip')
            cache_filename: Filename to use for cached ZIP (e.g., 'fastmcp-main.zip')

        Returns:
            Path to downloaded/cached ZIP file

        Raises:
            requests.RequestException: If download fails
        """
        cache_path = self.cache_dir / cache_filename

        # Check if already downloaded
        if cache_path.exists():
            print(f"✓ Using cached repository: {cache_path}")
            return cache_path

        print(f"⬇ Downloading repository from {repo_url}...")

        try:
            # Download the ZIP file
            response = requests.get(repo_url, timeout=60)
            response.raise_for_status()

            # Save to cache
            with open(cache_path, 'wb') as f:
                f.write(response.content)

            print(f"✓ Repository downloaded and cached: {cache_path}")
            return cache_path

        except requests.RequestException as e:
            raise requests.RequestException(f"Failed to download repository: {str(e)}")

    def extract_markdown_files(self, zip_path: Path) -> List[Dict[str, str]]:
        """
        Extract markdown files from ZIP archive.

        Args:
            zip_path: Path to ZIP file

        Returns:
            List of dicts with 'filename' and 'content' keys

        Example:
            [
                {
                    "filename": "docs/getting-started.md",
                    "content": "# Getting Started\\n\\n..."
                },
                ...
            ]

        Raises:
            zipfile.BadZipFile: If ZIP file is corrupted
        """
        documents = []

        print(f"📄 Extracting markdown files from {zip_path.name}...")

        try:
            with zipfile.ZipFile(zip_path, 'r') as zf:
                # Get all files in the archive
                for file_info in zf.filelist:
                    filename = file_info.filename

                    # Filter for markdown files
                    if filename.endswith(('.md', '.mdx')):
                        # Read file content
                        with zf.open(file_info) as f:
                            try:
                                content = f.read().decode('utf-8')
                            except UnicodeDecodeError:
                                # Skip files that can't be decoded
                                print(f"⚠️  Skipping {filename} (encoding error)")
                                continue

                        # Remove path prefix (e.g., "fastmcp-main/" -> "")
                        # This normalizes paths across different repo structures
                        parts = filename.split('/', 1)
                        if len(parts) > 1:
                            processed_filename = parts[1]
                        else:
                            processed_filename = filename

                        documents.append({
                            "filename": processed_filename,
                            "content": content
                        })

            print(f"✓ Extracted {len(documents)} markdown files")
            return documents

        except zipfile.BadZipFile as e:
            raise zipfile.BadZipFile(f"Invalid ZIP file: {str(e)}")

    def create_search_index(
        self,
        documents: List[Dict[str, str]],
        text_fields: Optional[List[str]] = None,
        keyword_fields: Optional[List[str]] = None
    ) -> Index:
        """
        Create MinSearch index from documents.

        Args:
            documents: List of dicts with 'filename' and 'content'
            text_fields: Fields to index for full-text search (default: ["content"])
            keyword_fields: Fields for exact keyword matching (default: ["filename"])

        Returns:
            Configured and fitted MinSearch index

        Example:
            >>> docs = [{"filename": "README.md", "content": "# Hello"}]
            >>> index = indexer.create_search_index(docs)
            >>> results = index.search("hello")
        """
        if text_fields is None:
            text_fields = ["content"]
        if keyword_fields is None:
            keyword_fields = ["filename"]

        print(f"🔍 Creating search index...")
        print(f"   Text fields: {text_fields}")
        print(f"   Keyword fields: {keyword_fields}")

        # Initialize Index with specified fields
        index = Index(
            text_fields=text_fields,
            keyword_fields=keyword_fields
        )

        # Fit index with documents
        index.fit(documents)

        print(f"✓ Index created with {len(documents)} documents")

        return index

    def search(
        self,
        query: str,
        top_k: int = 5,
        filter_dict: Optional[Dict] = None,
        boost_dict: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Search documentation using the index.

        Args:
            query: Search query string
            top_k: Number of results to return (default: 5)
            filter_dict: Optional filters for keyword fields
            boost_dict: Optional field boosting weights

        Returns:
            List of top K most relevant documents

        Example:
            >>> results = indexer.search("getting started", top_k=3)
            >>> print(results[0]['filename'])
            'docs/getting-started.md'
        """
        if self._index is None:
            raise RuntimeError("Index not initialized. Call load_and_index() first.")

        # Perform search
        results = self._index.search(
            query=query,
            filter_dict=filter_dict,
            boost_dict=boost_dict,
            num_results=top_k
        )

        return results

    def load_and_index(
        self,
        repo_url: str,
        cache_filename: str,
        text_fields: Optional[List[str]] = None,
        keyword_fields: Optional[List[str]] = None
    ) -> Index:
        """
        Complete workflow: download, extract, and index documentation.

        This is a convenience method that combines all steps:
        1. Download repository (with caching)
        2. Extract markdown files
        3. Create search index

        Args:
            repo_url: GitHub archive URL
            cache_filename: Filename for cached ZIP
            text_fields: Fields for full-text search
            keyword_fields: Fields for keyword filtering

        Returns:
            Fitted MinSearch index

        Example:
            >>> indexer = DocumentationIndexer()
            >>> index = indexer.load_and_index(
            ...     "https://github.com/user/repo/archive/main.zip",
            ...     "repo-main.zip"
            ... )
            >>> results = indexer.search("query")
        """
        # Download repo
        zip_path = self.download_repo(repo_url, cache_filename)

        # Extract markdown files
        self._documents = self.extract_markdown_files(zip_path)

        # Create index
        self._index = self.create_search_index(
            self._documents,
            text_fields=text_fields,
            keyword_fields=keyword_fields
        )

        return self._index

    @property
    def index(self) -> Optional[Index]:
        """Get the current search index."""
        return self._index

    @property
    def documents(self) -> List[Dict[str, str]]:
        """Get the loaded documents."""
        return self._documents

    def get_stats(self) -> Dict[str, int]:
        """
        Get statistics about the indexed documentation.

        Returns:
            Dictionary with document count and total content size
        """
        total_chars = sum(len(doc['content']) for doc in self._documents)

        return {
            "num_documents": len(self._documents),
            "total_characters": total_chars,
            "has_index": self._index is not None
        }
