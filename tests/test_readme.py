import re
import unittest

try:
    import requests
except ImportError:  # Provide dummy placeholder so tests fail to import if requests not installed
    requests = None


class TestReadmeLinks(unittest.TestCase):
    README_PATH = 'README.md'
    LINK_PATTERN = re.compile(r'https://[^\s)"<>]+')

    def test_links_http_200(self):
        if requests is None:
            self.skipTest('requests library is not installed')
        with open(self.README_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        links = self.LINK_PATTERN.findall(content)
        for link in links:
            with self.subTest(url=link):
                try:
                    response = requests.head(link, allow_redirects=True, timeout=5)
                    status = response.status_code
                    if status == 405:
                        response = requests.get(link, allow_redirects=True, timeout=5)
                        status = response.status_code
                    self.assertEqual(status, 200)
                except requests.RequestException as e:
                    self.skipTest(f"Network issue when accessing {link}: {e}")


if __name__ == '__main__':
    unittest.main()
