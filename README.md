## File Converter Online
Find all in one video converter, document, images, audios, pdfs, ebooks, software and much more.

## Setup development envirnment

Install python 3.6 or greator

```
pip install -r requirements.txt
python app.py
```

## Translation

For html template use `{% trans %} your text {% endtrans %}` and to translate strings in .py files use `_("your text")` function `from flask_babel import gettext as  _`

### Extract translations
```
pybabel extract -F babel.cfg -o messages.pot .
```

### Add new translation
```
pybabel init -i messages.pot -d translations -l fr
```

### Update existing translations
```
pybabel update -i messages.pot -d translations
```

### Compile tranlations
```
pybabel compile -d translations
```