from django import test
from django.core.urlresolvers import reverse


class TestHTML:
    def setup(self):
        self.client = test.Client()

    def test_home(self):
        home_url = reverse('caspy.views.home')
        response = self.client.get(home_url)
        assert 'caspy/index.html' in [t.name for t in response.templates]
