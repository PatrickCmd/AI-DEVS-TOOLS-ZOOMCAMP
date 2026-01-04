#!/usr/bin/env python3
"""
Documentation Search CLI

A command-line interface for indexing and searching documentation from
GitHub repositories or websites.

Usage:
    python cli.py index --url <url> --name <name>
    python cli.py search --name <name> --query <query>
    python cli.py interactive

Examples:
    # Index FastMCP documentation
    python cli.py index --url https://github.com/jlowin/fastmcp --name fastmcp

    # Search indexed documentation
    python cli.py search --name fastmcp --query "how to create tools"

    # Interactive mode
    python cli.py interactive
"""

import click
import re
import requests
from pathlib import Path
from typing import Optional
from doc_indexer import DocumentationIndexer


# Global storage for indexed repositories
INDEXES = {}
CACHE_DIR = Path("data")


def detect_default_branch(org: str, repo: str) -> str:
    """
    Detect the default branch of a GitHub repository.

    Args:
        org: GitHub organization/user
        repo: Repository name

    Returns:
        Default branch name ('main', 'master', etc.)
    """
    # Common branch names to try in order
    branches = ['main', 'master', 'develop', 'trunk']

    for branch in branches:
        # Try to access the archive URL
        test_url = f"https://github.com/{org}/{repo}/archive/refs/heads/{branch}.zip"
        try:
            response = requests.head(test_url, timeout=5, allow_redirects=True)
            if response.status_code == 200:
                return branch
        except:
            continue

    # Default to 'main' if detection fails
    return 'main'


def get_repo_url(url: str, branch: Optional[str] = None) -> tuple[str, str]:
    """
    Convert GitHub URL or website URL to archive URL.

    Args:
        url: GitHub repo URL or website URL
        branch: Optional branch name (auto-detected if not provided)

    Returns:
        Tuple of (archive_url, detected_branch)
    """
    # Check if it's a GitHub URL
    github_pattern = r'https?://github\.com/([^/]+)/([^/]+)'
    match = re.match(github_pattern, url.rstrip('/'))

    if match:
        org, repo = match.groups()
        # Remove .git suffix if present
        repo = repo.replace('.git', '')

        # Detect branch if not provided
        if branch is None:
            click.echo("🔍 Detecting default branch...")
            branch = detect_default_branch(org, repo)
            click.echo(f"   Detected branch: {branch}")

        archive_url = f"https://github.com/{org}/{repo}/archive/refs/heads/{branch}.zip"
        return archive_url, branch
    else:
        # For non-GitHub URLs, return as-is (will be scraped)
        return url, 'main'


def get_cache_filename(name: str) -> str:
    """Generate cache filename from repository name."""
    # Sanitize name for filesystem
    safe_name = re.sub(r'[^\w\-]', '_', name.lower())
    return f"{safe_name}-main.zip"


@click.group()
def cli():
    """Documentation Search CLI - Index and search documentation from GitHub repos."""
    pass


@cli.command()
@click.option('--url', prompt='Repository or website URL',
              help='GitHub repository URL or website URL to index')
@click.option('--name', prompt='Name for this index',
              help='Friendly name to identify this documentation index')
@click.option('--branch', default=None,
              help='Branch name (auto-detected if not specified)')
@click.option('--cache-dir', default='data',
              help='Directory to store cached files (default: data)')
def index(url: str, name: str, branch: Optional[str], cache_dir: str):
    """
    Download and index documentation from a GitHub repository or website.

    This command will:
    1. Download the repository as a ZIP file (with caching)
    2. Extract markdown files (.md and .mdx)
    3. Create a searchable index using MinSearch
    4. Save the index for future searches

    Examples:
        python cli.py index --url https://github.com/jlowin/fastmcp --name fastmcp
        python cli.py index --url https://github.com/alexeygrigorev/minsearch --name minsearch
    """
    click.echo()
    click.secho(f"🔍 Indexing: {name}", fg='blue', bold=True)
    click.echo(f"URL: {url}")
    click.echo("-" * 60)

    try:
        # Create indexer
        indexer = DocumentationIndexer(cache_dir=cache_dir)

        # Get repository URL with branch detection
        repo_url, detected_branch = get_repo_url(url, branch)
        cache_file = get_cache_filename(name)

        click.echo(f"Archive URL: {repo_url}")
        click.echo(f"Branch: {detected_branch}")
        click.echo(f"Cache file: {cache_file}")
        click.echo()

        # Load and index
        with click.progressbar(length=3, label='Indexing') as bar:
            # Download
            indexer.download_repo(repo_url, cache_file)
            bar.update(1)

            # Extract
            docs = indexer.extract_markdown_files(CACHE_DIR / cache_file)
            bar.update(1)

            # Create index
            indexer.create_search_index(docs)
            bar.update(1)

        # Store in global registry
        INDEXES[name] = indexer

        # Display stats
        stats = indexer.get_stats()
        click.echo()
        click.secho("✓ Indexing complete!", fg='green', bold=True)
        click.echo(f"Documents indexed: {stats['num_documents']}")
        click.echo(f"Total characters: {stats['total_characters']:,}")
        click.echo()
        click.secho(f"You can now search with: python cli.py search --name {name} --query 'your query'", fg='cyan')

    except Exception as e:
        click.secho(f"✗ Error during indexing: {str(e)}", fg='red', bold=True)
        raise click.Abort()


@cli.command()
@click.option('--name', prompt='Index name',
              help='Name of the documentation index to search')
@click.option('--query', prompt='Search query',
              help='What do you want to search for?')
@click.option('--top-k', default=5, type=click.IntRange(1, 10),
              help='Number of results to return (1-10)')
@click.option('--cache-dir', default='data',
              help='Directory where cached files are stored (default: data)')
def search(name: str, query: str, top_k: int, cache_dir: str):
    """
    Search indexed documentation.

    This command searches through previously indexed documentation
    and returns the most relevant results.

    Examples:
        python cli.py search --name fastmcp --query "how to create tools"
        python cli.py search --name fastmcp --query "getting started" --top-k 3
    """
    click.echo()
    click.secho(f"🔎 Searching: {name}", fg='blue', bold=True)
    click.echo(f"Query: \"{query}\"")
    click.echo("-" * 60)

    try:
        # Check if index exists in memory
        if name not in INDEXES:
            click.echo(f"Loading index for '{name}'...")

            # Try to load from cache
            indexer = DocumentationIndexer(cache_dir=cache_dir)
            cache_file = get_cache_filename(name)
            cache_path = CACHE_DIR / cache_file

            if not cache_path.exists():
                click.secho(f"✗ Index '{name}' not found!", fg='red', bold=True)
                click.echo(f"Available cache files: {list(CACHE_DIR.glob('*.zip'))}")
                click.echo()
                click.secho(f"Please index it first: python cli.py index --name {name}", fg='yellow')
                raise click.Abort()

            # Load the index
            docs = indexer.extract_markdown_files(cache_path)
            indexer._documents = docs  # Store documents
            indexer._index = indexer.create_search_index(docs)  # Store index
            INDEXES[name] = indexer

        # Perform search
        indexer = INDEXES[name]
        results = indexer.search(query, top_k=top_k)

        if not results:
            click.secho(f"No results found for '{query}'", fg='yellow')
            return

        # Display results
        click.echo()
        click.secho(f"Found {len(results)} result(s):", fg='green', bold=True)
        click.echo()

        for i, doc in enumerate(results, 1):
            filename = doc.get('filename', 'Unknown')
            content = doc.get('content', '')

            # Preview (first 150 characters)
            preview = content[:150].replace('\n', ' ').strip()
            if len(content) > 150:
                preview += "..."

            click.secho(f"{i}. {filename}", fg='cyan', bold=True)
            click.echo(f"   {preview}")
            click.echo()

    except Exception as e:
        if not isinstance(e, click.Abort):
            click.secho(f"✗ Error during search: {str(e)}", fg='red', bold=True)
            raise click.Abort()


@cli.command()
@click.option('--cache-dir', default='data',
              help='Directory for cached files (default: data)')
def interactive(cache_dir: str):
    """
    Interactive mode - Index and search documentation interactively.

    This command provides an interactive experience where you can:
    1. Choose to index a new repository
    2. Search existing indexed documentation
    3. Continue querying without re-indexing

    Example:
        python cli.py interactive
    """
    click.clear()
    click.secho("=" * 60, fg='blue')
    click.secho("  Documentation Search CLI - Interactive Mode", fg='blue', bold=True)
    click.secho("=" * 60, fg='blue')
    click.echo()

    current_index = None
    indexer = None

    while True:
        if current_index is None:
            # Ask what to do
            click.secho("\nWhat would you like to do?", fg='cyan', bold=True)
            click.echo("1. Index a new repository")
            click.echo("2. Search existing index")
            click.echo("3. Exit")
            choice = click.prompt("Your choice", type=click.IntRange(1, 3), default=1)

            if choice == 3:
                click.secho("\n👋 Goodbye!", fg='green')
                break

            elif choice == 1:
                # Index new repository
                click.echo()
                url = click.prompt("Repository or website URL",
                                 default="https://github.com/jlowin/fastmcp")
                name = click.prompt("Name for this index",
                                  default="fastmcp")

                click.echo()
                click.secho(f"Indexing '{name}' from {url}...", fg='blue')

                try:
                    # Create indexer
                    indexer = DocumentationIndexer(cache_dir=cache_dir)
                    repo_url, detected_branch = get_repo_url(url)
                    cache_file = get_cache_filename(name)

                    click.echo(f"Branch: {detected_branch}")

                    # Load and index
                    indexer.load_and_index(repo_url, cache_file)

                    stats = indexer.get_stats()
                    click.echo()
                    click.secho(f"✓ Indexed {stats['num_documents']} documents!", fg='green', bold=True)

                    current_index = name
                    INDEXES[name] = indexer

                except Exception as e:
                    click.secho(f"✗ Error: {str(e)}", fg='red')
                    continue

            elif choice == 2:
                # Search existing
                name = click.prompt("Index name to search")

                if name not in INDEXES:
                    try:
                        indexer = DocumentationIndexer(cache_dir=cache_dir)
                        cache_file = get_cache_filename(name)
                        cache_path = CACHE_DIR / cache_file

                        if not cache_path.exists():
                            click.secho(f"✗ Index '{name}' not found!", fg='red')
                            continue

                        docs = indexer.extract_markdown_files(cache_path)
                        indexer._documents = docs
                        indexer._index = indexer.create_search_index(docs)
                        INDEXES[name] = indexer

                    except Exception as e:
                        click.secho(f"✗ Error loading index: {str(e)}", fg='red')
                        continue

                current_index = name
                indexer = INDEXES[name]

        # Query loop
        click.echo()
        query = click.prompt(f"Search '{current_index}' (or 'quit' to go back)",
                            default="demo")

        if query.lower() in ['quit', 'exit', 'q']:
            current_index = None
            indexer = None
            continue

        # Perform search
        try:
            results = indexer.search(query, top_k=5)

            if not results:
                click.secho(f"No results found for '{query}'", fg='yellow')
                continue

            click.echo()
            click.secho(f"Found {len(results)} result(s):", fg='green', bold=True)
            click.echo()

            for i, doc in enumerate(results, 1):
                filename = doc.get('filename', 'Unknown')
                content = doc.get('content', '')
                preview = content[:150].replace('\n', ' ').strip()
                if len(content) > 150:
                    preview += "..."

                click.secho(f"{i}. {filename}", fg='cyan', bold=True)
                click.echo(f"   {preview}")
                click.echo()

        except Exception as e:
            click.secho(f"✗ Search error: {str(e)}", fg='red')


if __name__ == '__main__':
    cli()
