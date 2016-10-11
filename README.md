# Twitter Wall

Twitter Wall pro terminál. Aplikace, která bude zobrazovat tweety odpovídající určitému hledání do terminálu v nekonečné smyčce.

Aplikace načte určitý počet tweetů odpovídající hledanému výrazu, zobrazí je a v nějakém intervalu se bude dotazovat na nové tweety (použijte API argument since_id).

Pomocí argumentů půjde nastavit:

* cesta ke konfiguračnímu souboru s přístupovými údaji
* hledaný výraz
* počet na začátku načtených tweetů
* časový interval dalších dotazů
* nějaké vlastnosti ovlivňující chování (např. zda zobrazovat retweety)
