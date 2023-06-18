importujeme ze souboru market.__init__ ale init je inicializacni soubor - proto staci napsat jen market

>>> from market import app, db
>>> app.app_context().push()
>>> db.create_all()