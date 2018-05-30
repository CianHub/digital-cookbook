import unittest
from utils import get_pages, generate_pagination_links, get_countries, increment_field

class test_functions(unittest.TestCase):
    # Test Suite #
    def test_get_pages(self):
        # Test if function returns the correct number of pages #
        
        self.assertEqual(get_pages(20,5), 4)
        self.assertEqual(get_pages(21,5), 5)
        self.assertEqual(get_pages(19,4), 5)
        assert type(get_pages(19,4)) is int

        
    def test_get_pagination_links(self):
        # Test if function returns an array of urls for pagination buttons #

        self.assertEqual(generate_pagination_links(0, 10, 3, 'recipes', 'null', 'Paul'),
        ['/Paul/recipes?limit=10&offset=0','/Paul/recipes?limit=10&offset=10','/Paul/recipes?limit=10&offset=20','/Paul/recipes?limit=10&offset=30'])
        
        self.assertEqual(generate_pagination_links(0, 10, 3, 'search', 'chicken', 'Paul'),
        ['/Paul/search/chicken?limit=10&offset=0','/Paul/search/chicken?limit=10&offset=10',
        '/Paul/search/chicken?limit=10&offset=20','/Paul/search/chicken?limit=10&offset=30'])
        
        self.assertEqual(generate_pagination_links(0, 10, 4, 'search', 'chicken', 'Jim'),
        ['/Jim/search/chicken?limit=10&offset=0','/Jim/search/chicken?limit=10&offset=10',
        '/Jim/search/chicken?limit=10&offset=20','/Jim/search/chicken?limit=10&offset=30','/Jim/search/chicken?limit=10&offset=40'])
        
        assert type(generate_pagination_links(0, 10, 3, 'recipes', 'null','Kim')) is list
    
    def test_get_countries(self):
        # Test if function returns an array of countries  #
        
        assert type(get_countries()) is list
        
        country_list = get_countries()
        self.assertEqual(country_list[0][1],"Choose a Country of Origin")
        self.assertEqual(country_list[-1][1],"Zimbabwe")
        
    def test_increment_field(self):
        # Test if function returns an int  #
        
        current = [{'upvotes': 2}, {'downvotes': 0}]
        
        assert type(increment_field('upvotes', current)) is int
        self.assertEqual(increment_field('downvotes', current), 1)
