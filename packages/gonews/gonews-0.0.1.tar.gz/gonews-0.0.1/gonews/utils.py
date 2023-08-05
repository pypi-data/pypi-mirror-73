from time import sleep
from xmltodict import parse
from modutils import BaseSession
from logging import CRITICAL, getLogger

class GoNews(BaseSession):
    states = {
        'Alabama': 'AL',
        'Alaska': 'AK',
        'Arizona': 'AZ',
        'Arkansas': 'AR',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'Delaware': 'DE',
        'District of Columbia': 'DC',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Hawaii': 'HI',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Iowa': 'IA',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Maine': 'ME',
        'Maryland': 'MD',
        'Massachusetts': 'MA',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Mississippi': 'MS',
        'Missouri': 'MO',
        'Montana': 'MT',
        'Nebraska': 'NE',
        'Nevada': 'NV',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'New York': 'NY',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Vermont': 'VT',
        'Virginia': 'VA',
        'Washington': 'WA',
        'West Virginia': 'WV',
        'Wisconsin': 'WI',
        'Wyoming': 'WY'
    }

    def __init__(self):
        super().__init__()
        self.resolve_status_codes.extend([400, 404, 500])
        self.base_url = 'https://news.google.com/news/rss'
        self.session_logger.setLevel(CRITICAL)
        getLogger('urllib3').setLevel(CRITICAL)


    def search(self, query: str = None, has_words: list = None, exclude_words: list = None, when: str = '1d'):
        """search google news feed

        :param query: Exact query to search
        :param has_words: words that news articles should contain
        :param exclude_words:
        :param when:
        :return:
        """
        full_query = f'"{query}" when:{when} '
        if has_words:
            if isinstance(has_words, str):
                full_query += f'{has_words} '
            elif isinstance(has_words, list):
                full_query += f'{" ".join(has_words)} '
        if exclude_words:
            if isinstance(exclude_words, str):
                full_query += f'-{exclude_words} '
            elif isinstance(exclude_words, list):
                full_query += f'{" ".join([f"-{w}" for w in exclude_words])} '
        return self.get(f'{self.base_url}/search', params={'q': full_query})

    def search_stories(self, query: str = None, has_words: list = None, exclude_words: list = None, when: str = '1d',
                       max_stories: int = None):
        news: dict = {}
        resp = self.search(query, has_words=has_words, exclude_words=exclude_words, when=when)
        if resp.status_code == 200:
            news = parse(resp.content.decode('utf-8'))
        self.print_news(self.parse_news(news), max_stories=max_stories)

    def get_news_by_location(self, city: str, state_abbr: str):
        return self.get(f'{self.base_url}/headlines/section/geo/{city}{state_abbr}')

    def get_news_top_stories(self):
        return self.get(f'{self.base_url}/news/rss')

    def parse_news(self, news: dict):
        results: dict = {}
        for index, item in enumerate(news.get('rss', {}).get('channel', {}).get('item', [])):
            results.update({str(index+1): {'title': item.get('title', None), 'link': item.get('link', None)}})
        return results

    def top_stories_by_location(self, city: str, state: str, max_stories: int = None):
        news: dict = {}
        assert any([state.lower() == st_key.lower() for st_key in self.states.keys()]) or any(
            [state.lower() == st_abbr.lower() for st_abbr in self.states.values()]), f'{state!r} is not a valid ' \
                                                                                     f'state name or state abbreviation'
        resp = self.get_news_by_location(city, state)
        if resp.status_code == 200:
            news = parse(resp.content.decode('utf-8'))
        self.print_news(self.parse_news(news), max_stories=max_stories)

    def top_stories(self, max_stories: int = None):
        news: dict = {}
        resp = self.get_news_top_stories()
        if resp.status_code == 200:
            news = parse(resp.content.decode('utf-8'))
        self.print_news(self.parse_news(news), max_stories=max_stories)

    def resolve_redirect(self, link: str):
        resp = self.get(link)
        return resp.url

    def print_news(self, parsed_news: dict, max_stories: int = None):
        if parsed_news:
            for headline_number, content in parsed_news.items():
                if max_stories and int(headline_number) > max_stories:
                    break
                print(f'{headline_number}. {content["title"]}\nURL: {self.resolve_redirect(content["link"])}\n\n')
                sleep(1)

        else:
            print(f'No news was found')

