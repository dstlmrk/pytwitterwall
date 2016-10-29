# Twitter Wall

## Spuštění

```
Usage: pytwitterwall [OPTIONS] COMMAND [ARGS]...

  Simple program which reads posts from Twitter via its API.

Options:
  --conf TEXT                     Configuration path [./conf/auth.cfg].
  --initial-count INTEGER         Count of first tweets [15]. Max 100.
  --retweets-are-allowed / --no-retweets
                                  Flag that shows retweets. Defaults to true.
  --help                          Show this message and exit.

Commands:
  console  Run the console app
  web      Run the web app
```

Webová aplikace příjímá hledaný řetězec pomocí URL adresy:

```
/search/put-your-query
```

## Konfigurační soubor

V konfiguračním souboru (implicitně `./conf/auth.cfg`) lze nastavit přístupové údaje pro váš účet na [Twitteru](https://twitter.com/). Jeho podoba musí být následující:

```
[twitter]
key = your-api-key
secret = your-api-secret
```

## Příklad použití

```
$ pytwitterwall --no-retweets console
Your query string [#python]:
----------
How to get item's position in a list? #python #list https://t.co/npvrx5fFCs
----------
3 simple things you can do every day to harness the power of #PyCharm keyboard shortcuts
...
```

```
$ pytwitterwall web --debug
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger pin code: 133-764-633
...
```

## Testování

```
$ python setup.py test
```

Pro testování API (aktuální data, znovunačtení kazet) je nutné zadat přístupové údaje k Twitter API pomocí systémové proměnné:

```
$ export AUTH_FILE="./conf/auth.cfg"
```

## Požadavky

* click
* requests
* Flask
* Jinja2

## Zadání 1. úkolu

Twitter Wall pro terminál. Aplikace, která bude zobrazovat tweety odpovídající určitému hledání do terminálu v nekonečné smyčce.

Aplikace načte určitý počet tweetů odpovídající hledanému výrazu, zobrazí je a v nějakém intervalu se bude dotazovat na nové tweety (použijte API argument since_id).

Pomocí argumentů půjde nastavit:

* cesta ke konfiguračnímu souboru s přístupovými údaji
* hledaný výraz
* počet na začátku načtených tweetů
* časový interval dalších dotazů
* nějaké vlastnosti ovlivňující chování (např. zda zobrazovat retweety)

## Zadání 2. úkolu

Konzole není pro Twitter Wall dostatečně vhodné médium, doplňte do aplikace webový frontend, který bude zobrazovat výsledky hledání. Hledaný pojem by měl jít zadat pomocí URL.

Pro plný počet bodů musí rozhraní zobrazovat avatary uživatelů a zpracovávat entity jako obrázky, odkazy, zmínky a hash tagy. Ideální je k tomu využít filtr.