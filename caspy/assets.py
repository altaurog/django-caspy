from django_assets import Bundle, register
js = Bundle(
    'caspy/static/js/controllers.js',
    'caspy/static/js/services.js',
)
register('js_all', js)
