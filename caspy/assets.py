from django_assets import Bundle, register
js = Bundle('caspy/static/js/*.js',)
register('js_all', js)
