# Twitter Wall

Twitter Wall pro terminál. Aplikace, která bude zobrazovat tweety odpovídající určitému hledání do terminálu v nekonečné smyčce.

Aplikace načte určitý počet tweetů odpovídající hledanému výrazu, zobrazí je a v nějakém intervalu se bude dotazovat na nové tweety (použijte API argument since_id).

Pomocí argumentů půjde nastavit:

* cesta ke konfiguračnímu souboru s přístupovými údaji
* hledaný výraz
* počet na začátku načtených tweetů
* časový interval dalších dotazů
* nějaké vlastnosti ovlivňující chování (např. zda zobrazovat retweety)

## Spuštění

```bash
Usage: twitterwall.py [OPTIONS]

  Simple program which reads posts from Twitter via its API.

Options:
  -q, --query TEXT            Query string.
  --conf TEXT                 Configuration path. Defaults to ./conf/auth.cfg.
  --count INTEGER             Count of first tweets, up to a maximum of 100.
                              Defaults to 15.
  --loop INTEGER              How often tweets will be reloaded in seconds.
                              Defaults to 5.
  --retweets / --no-retweets  Flag that shows retweets. Defaults to true.
  --help                      Show this message and exit.
```

V konfiguračním souboru lze nastavit přístupové údaje pro váš účet na [Twitteru](https://twitter.com/).

## Příklad použití

```
$ ./twitterwall.py
Your query string [#python]: hroncok
----------
RT @stillgray: Reading this really upset me. SJWs went Harambe on an autistic man who wanted high-fives and sent him death threats. https:/…
----------
@JakubJirutka Těžko. Už od státnic v #cvutsenat nejsem a být nemůžu. @FIT_CTU
----------
@hroncok Doufám, že tě můžeme zvolit i na další období?! @fit_ctu
----------
Studenti @FIT_CTU, je mezi vámi nějaký frajer, či frajerka, co bude na #cvutsenat pořádně prudit a tweetovat? https://t.co/uEdt4ybkPj
----------
RT @michalillich: Ne zcela optimistická zpráva o ANO.
(Souhlasím a navíc myslím, že ANO v druhém kole moc senátorů nezíská)
https://t.co/Jc…
----------
@martinvarecha @viktorvesely @rozanek smysl ta úprava nemá
----------
@honzajavorek @naPyvo se také chystám. Střelnice je obvykle na hodinku, ale nemá smysl spěchat. Půjdeme tedy s @hroncok a příp. @petrjoachim
----------
@lumirbalhar @petrjoachim @hroncok já to budu mít mega nabité, pro mě nepřipadá v úvahu - navíc ve čtvrtek je v Brně @naPyvo ;-)
----------
@petrjoachim @hroncok @honzajavorek Padl nápad skočit na střelnici před PyConem ve čtvrtek 27. 10. odpoledne. Co Vy na to?
----------
@lumirbalhar @hroncok @honzajavorek to zni jako plan
----------
@lumirbalhar @hroncok @petrjoachim já si to nechám na sprint, v Brně do Pyconu nebudu
----------
@hroncok Oukej, tak třeba příští týden v Brně? Objednám střelnici a vezmu více sypání. @honzajavorek @petrjoachim
----------
@lumirbalhar jo! @honzajavorek @petrjoachim
----------
@hroncok @honzajavorek @petrjoachim Chcete si to zkusit a zajit se mnou na strelnici?
----------
@hroncok @honzajavorek @petrjoachim Ne. Strelba je skvela zabava a svym zpusobem meditace. Kdo to nezkusil, nepochopi. Obrana je jen bonus.
----------
```