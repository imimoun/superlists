from django.test import TestCase

from utils.utils import remove_csrf, get_csrf_tag


class RemoveCSRFTest(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_there_is_no_csrf(self):
        dom_no_csrf_with_csrf = ("<html>"
                                 "</html>")
        dom_no_csrf_without_csrf = ("<html>"
                                    "</html>")
        self.assertEqual(dom_no_csrf_without_csrf,
                         remove_csrf(dom_no_csrf_with_csrf))

    def test_there_is_one_csrf(self):
        dom_one_csrf_without_csrf = ("<html>"
                                     "  <body>"
                                     "    <form>"
                                     "      <input name=\"first_name\"/>"
                                     "    </form>"
                                     "  </body>"
                                     "</html>")
        dom_one_csrf_with_csrf = ("<html>"
                                  "  <body>"
                                  "    <form>"
                                  + get_csrf_tag() +
                                  "      <input name=\"first_name\"/>"
                                  "    </form>"
                                  "  </body>"
                                  "</html>")
        self.assertEqual(dom_one_csrf_without_csrf,
                         remove_csrf(dom_one_csrf_with_csrf))

    def test_there_is_two_csrf(self):
        dom_two_csrf_without_csrf = ("<html>"
                                     "  <body>"
                                     "    <form>"
                                     "      <input name=\"first_name\"/>"
                                     "    </form>"
                                     "    <form>"
                                     "      <input name=\"first_name\"/>"
                                     "    </form>"
                                     "  </body>"
                                     "</html>")
        dom_two_csrf_with_csrf = ("<html>"
                                  "  <body>"
                                  "    <form>"
                                  + get_csrf_tag() +
                                  "      <input name=\"first_name\"/>"
                                  "    </form>"
                                  "    <form>"
                                  + get_csrf_tag() +
                                  "      <input name=\"first_name\"/>"
                                  "    </form>"
                                  "  </body>"
                                  "</html>")
        self.assertEqual(dom_two_csrf_without_csrf,
                         remove_csrf(dom_two_csrf_with_csrf))


class GetCsrfTag(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_csrf_tag_is_right_regex(self):
        regex_csrf_tag = r"<input type='hidden' name='csrfmiddlewaretoken' value='[a-zA-z0-9]{64}' />"
        self.assertRegex(get_csrf_tag(), regex_csrf_tag)
