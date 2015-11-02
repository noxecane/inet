import unittest
from inet.router import Router
from inet import message


class RouterTest(unittest.TestCase):

    def test_transform(self):
        service, req = Router.transform('user://hello/world')
        self.assertEqual(service, 'user')
        self.assertEqual(req.meta['path'], 'hello/world')

    def test_transform_fail(self):
        with self.assertRaises(ValueError):
            service, req = Router.transform('user/hello/world')

    def test_bad_request(self):
        router = Router()
        req = message.message()
        self.assertFalse(router.route(req))

    def test_request(self):
        router = Router()
        router.register('yes/hello', hello)
        service, req = Router.transform('user://yes/hello')
        self.assertEqual(router.route(req), hello)

    def test_404(self):
        router = Router()
        service, req = Router.transform('user://yes/hello')
        self.assertIsNone(router.route(req))


def hello():
    pass

if __name__ == '__main__':
    unittest.main()
