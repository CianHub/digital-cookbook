import unittest
from functions import get_pages, generate_pagination_links

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

        self.assertEqual(generate_pagination_links(0, 10, 3, 'recipes', 'null'),
        ['/recipes?limit=10&offset=0','/recipes?limit=10&offset=10','/recipes?limit=10&offset=20','/recipes?limit=10&offset=30'])
        
        self.assertEqual(generate_pagination_links(0, 10, 3, 'search', 'chicken'),
        ['/search/chicken?limit=10&offset=0','/search/chicken?limit=10&offset=10',
        '/search/chicken?limit=10&offset=20','/search/chicken?limit=10&offset=30'])
        
        self.assertEqual(generate_pagination_links(0, 10, 4, 'search', 'chicken'),
        ['/search/chicken?limit=10&offset=0','/search/chicken?limit=10&offset=10',
        '/search/chicken?limit=10&offset=20','/search/chicken?limit=10&offset=30','/search/chicken?limit=10&offset=40'])
        
        assert type(generate_pagination_links(0, 10, 3, 'recipes', 'null')) is list
        
