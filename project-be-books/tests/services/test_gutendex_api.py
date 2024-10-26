import unittest
import requests


class GutendexApiTestCase(unittest.TestCase):
    @unittest.skip
    def test_search_book(self):
        response = requests.get("http://gutendex.com/books?search=Frankenstein")

        self.assertEqual(response.status_code, 200)

        content = response.json()

        self.assertTrue("results" in content)
        self.assertTrue(len(content["results"]) != 0)

        first_result = content["results"][0]
        self.assertTrue("id" in first_result)
        self.assertIs(int, type(first_result["id"]))
        self.assertTrue("title" in first_result)
        self.assertIs(str, type(first_result["title"]))
        self.assertTrue("authors" in first_result)
        self.assertTrue(len(first_result["authors"]) != 0)

        first_author = first_result["authors"][0]
        self.assertTrue("name" in first_author)

    @unittest.skip
    def test_get_book_detail(self):
        response = requests.get("http://gutendex.com/books/84")

        self.assertEqual(response.status_code, 200)

        content = response.json()

        self.assertTrue("id" in content)
        self.assertIs(int, type(content["id"]))
        self.assertTrue("title" in content)
        self.assertIs(str, type(content["title"]))
        self.assertTrue("authors" in content)
        self.assertTrue(len(content["authors"]) != 0)
        self.assertTrue("subjects" in content)
        self.assertTrue(len(content["subjects"]) != 0)

        first_author = content["authors"][0]
        self.assertTrue("name" in first_author)

    @unittest.skip
    def test_get_missing_book_detail(self):
        response = requests.get("http://gutendex.com/books/875329578932759823")

        self.assertEqual(response.status_code, 404)

        content = response.json()

        self.assertFalse("id" in content)
        self.assertFalse("title" in content)
        self.assertFalse("authors" in content)
        self.assertFalse("subjects" in content)
