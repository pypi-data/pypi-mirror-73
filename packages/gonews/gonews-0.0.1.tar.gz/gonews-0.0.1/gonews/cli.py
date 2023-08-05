import click

from typing import List

from gonews.utils import GoNews


news = GoNews()


@click.group('cli')
def cli():
    pass


@cli.command('top-stories')
@click.option('--max-stories', '-ms', type=int, default=None, required=False, help='Max number of stories to retrieve')
def top_stories(max_stories: int = None):
    """Print current top stories"""
    news.top_stories(max_stories=max_stories)


@cli.command('top-stories-by-location')
@click.option('--city', '-c', type=str, required=True, help='City name')
@click.option('--state', '-s',
              type=click.Choice(list(news.states.keys())+list(news.states.values()), case_sensitive=False),
              required=True, help='State name. NOTE: Not case sensitive')
@click.option('--max-stories', '-ms', type=int, default=None, required=False, help='Max number of stories to retrieve')
def top_stories_by_location(city:str, state: str, max_stories: int = None):
    """Print current top stories for city, state"""
    news.top_stories_by_location(city, state, max_stories=max_stories)


@cli.command('search-stories')
@click.option('--query', '-q', type=str, required=True, help='Exact search term')
@click.option('--has-word', '-hw', type=str, required=False, multiple=True, help='Stories should have given word')
@click.option('--exclude-word', '-ew', type=str, required=False, multiple=True,
              help='Stories should not contain given word')
@click.option('--timeframe', '--t', type=click.Choice(['1d', '7d', '14d', '30d', '1y']), required=False, default='1d',
              help='Stories from this timeframe')
@click.option('--max-stories', '-ms', type=int, default=None, required=False, help='Max number of stories to retrieve')
def search_stories(query: str, has_word: List[str], exclude_word: List[str], timeframe: str, max_stories: int = None):
    """Print top stories based on search"""
    has_word = list(has_word)
    exclude_word = list(exclude_word)
    news.search_stories(query, has_words=has_word, exclude_words=exclude_word, when=timeframe, max_stories=max_stories)


if __name__ == '__main__':
    cli()