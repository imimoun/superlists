from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.urls.base import resolve

from lists.models import Item
from utils.utils import remove_csrf
from lists.views import home_page


class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html', request=request)

        self.assertEqual(remove_csrf(response.content.decode()),
                         remove_csrf(expected_html))

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'
        response = home_page(request)

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')
        self.assertIn('A new list item', response.content.decode())

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

        expected_html = render_to_string(
            'home.html',
            {'new_item_text': 'A new list item'},
            request=request
        )

        self.assertEqual(remove_csrf(response.content.decode()),
                         remove_csrf(expected_html))

    def test_home_page_only_saves_itmes_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)


class ItemModelsTest(TestCase):
    def test_saveing_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The firest (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_items = saved_items[0]
        second_saved_items = saved_items[1]
        self.assertEqual(first_saved_items.text, 'The firest (ever) list item')
        self.assertEqual(second_saved_items.text, 'Item the second')
