[![MIT Licensed](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/paaksing/django-cassiopeia/blob/master/LICENSE.txt)
[![Documentation Status](https://readthedocs.org/projects/django-cassiopeia/badge/?version=latest)](https://django-cassiopeia.readthedocs.io/en/latest/?badge=latest)
[![GitHub issues](https://img.shields.io/github/issues/Naereen/StrapDown.js.svg)](https://github.com/paaksing/django-cassiopeia/issues)


# Django Cassiopeia

An Integration of [Cassiopeia](https://github.com/meraki-analytics/cassiopeia) to the Django Framework (Compatible with DRF) including more new features.

Cassiopeia itself is a Python adaptation of the Riot Games League of Legends API (https://developer.riotgames.com/). For instance it is also the sister library to [Orianna](https://github.com/robrua/Orianna) (Java). It's been designed with usability in mind - making sure all the bookkeeping is done right so you can focus on getting the data you need and building your application.

## Documentation
Django Cassiopeia has detailed [documentation](https://django-cassiopeia.readthedocs.io/en/latest/).
For functions and methods of Cassiopeia is found is this [documentation](http://cassiopeia.readthedocs.org/en/latest/).
A changelog of the last 10 releases is at the bottom of this page.

## Installation and Requirements
```python
Django>=3.0.1
Python>=3.6

pip install django-cassiopeia
```

## Quick Start and/or Setup for your Django Project

* Please check out the things that you should NOT do when using django-cassiopeia in this [page](https://django-cassiopeia.readthedocs.io/en/latest/cautions/)
* For setup in your Django environment, follow the setup instructions in django-cassiopeia's [documentation](https://django-cassiopeia.readthedocs.io/en/latest/django-setup/)
* A Quick Start is also provided on django-cassiopeia's [documentation](https://django-cassiopeia.readthedocs.io/en/latest/examples/)
* Taking in mind the instruction above, for all the methods and function of cassiopeia is found in this [documentation](http://cassiopeia.readthedocs.org/en/latest/)

## Why use Cassiopeia (quoting from Cassiopeia repository)?

* An excellent user interface that makes working with data from the Riot API easy and fun.

* "Perfect" rate limiting.

* Guaranteed optimal usage of your API key.

* Built in caching and (coming) the ability to easily hook into a database for offline storage of data.

* Extendability to non-Riot data. Because Cass is a framework and not just an API wrapper, you can integrate your own data sources into your project. Cass already supports Data Dragon and the ``champion.gg`` API in addition to the Riot API.

* Dynamic settings so you can configure Cass for your specific use case.

## Features Integration and Fixed Issues

* **_Issue:_** Cassiopeia current caching system does not automatically (or regularly) expire objects on expirations which might cause severe memory issues when working with web frameworks if it goes out of your control. **_Solution:_** This integration will give you the ability to use Django's cache framework for your caching, which is full production tested.

* **_Issue:_** The variety of cache backends that Cass provides may not fit your needs when paired with Django. **_Solution:_** Now you can use ANY cache backends of your like that the Django's cache framework supports: Django-Redis, python-Memcached, pylibmc, Filebased, MySQL, Postgre, SQLite, ... (Check out [Django's cache framework official docs](https://docs.djangoproject.com/en/dev/topics/cache/) for more). Also ! You can configure it to have more than 1 cache, the ability to separate multiple objects to different caching system. 

* **_Issue:_** When not imported Cassiopeia correctly within the Django environment, each time you call a function that uses cass will create a new instance of it and killing all existing Ghost modules (for information of Cassiopeia's Ghost(Lazy) loading check out its [documentations](http://cassiopeia.readthedocs.org/en/latest/)), creating conflicts that might crash your server. **_Solution:_** Django Cassiopeia is an app, which you add it through the `INSTALLED_APPS` settings which automatically loads the adapted version of Cassiopeia.

* **_Issue:_** Cassiopeia's settings code block is too large compared to others Django settings. **_Solution:_** The Settings interface is adapted to a syntax that is compatible (visually) with Django Settings (see Setup for Django environment in documentations).

* **_Issue:_** When cassiopeia is paired with a web framework (e.g. Django, Flask), the "Perfect" rate limiting is not totally "Perfect" **_(it STILL WORKS, just not as atomic as in a single process environment, AKA normal python scripts without Multi-threading/processing modules)_**, since a Web Framework can behave in a variety of process flow: multi-process, async, conj. (see Existing Problems below).

## Existing and Future Plans.

* The current rate limiter is the SAME used in `cassiopeia`, so is rather a "Do not black list me" rate limiter **_(it holds calls for the time returned in retry-after header when an unexpected 429 is returned, which is what the Riot Team recommends)_**, but we (both cass and django-cass devs) prefer to not get a single 429 (or only in extreme cases), a rate limiter that fits (or may fits) to Django is under going research. _See the **Project** tab if you want to contribute for this, if compatible, we will consider porting it over to the main cassiopeia._

* Django's Cache cannot cache `Champion.gg` data yet .. in a very very short time will be updated the support. _I currently don't feel the need, the support is good to go by just adding some 50 lines of codes, fire me an issue if you need it._

* **_If you want any new feature for Django Cassiopeia_**, fire me a Feature Request and I will try to give you a response, I have some thoughts about replacing ddragon's champion json files with meraki's json files, or have an additional object for that.

## Trade-offs

* There is a minor caveat when using Django's cache over the Standard cache that Cassiopeia provides: It cannot cache `cassiopeia.core` objects due to the fact of its `key` not being of type `string` or a `picklable` object, so it rather caches `cassiopeia.dto` objects which then automatically be transform to `cassiopeia.core`. The time consumption difference is super minimal `cassiopeia.dto` needs some 20ms more than `cassiopeia.core`, **_but this is considered this is a good trade-off because `cassiopeia.core` takes a lot more memory (at least 5 times more if you use compressors on your Django's cache) compared to `cassiopeia.dto`._**

## Questions/Contributions/Bugs
* For Django Cassiopeia: Feel free to send pull requests or to contact us via this github or our general [discord](https://discord.gg/uYW7qhP). More information can be found in our [documentation](https://django-cassiopeia.readthedocs.io/en/latest/).
* For Cassiopeia: feel free to send pull requests or to contact cassiopeia devs via [cassiopeia's github](https://github.com/meraki-analytics/cassiopeia) or the same discord server. More information about main cassiopeia is found in this [documentation](http://cassiopeia.readthedocs.org/en/latest/).

## Citing Cassiopeia (Quoting from cassiopeia repository)
If you used Cassiopeia for your research, please [cite the project](https://doi.org/10.5281/zenodo.1170906).

## Supporting Cassiopeia and Django Cassiopeia
* If you've loved using Cassiopeia, consider supporting the former developers of the main framework through [PayPal](https://www.paypal.me/merakianalytics) or [Patreon](https://www.patreon.com/merakianalytics).
* If you want to support this specific project (`django-cassiopeia`), consider supporting me through [Patreon](https://www.patreon.com/paaksing) too. 

## Disclaimer
Django Cassiopeia existence is acknowleged by cassiopeia's former developers. Both package/framework/library is updated in parallel with some exceptions due to the fact of different use cases.

Cassiopeia/Django-Cassiopeia isn't endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing League of Legends. League of Legends and Riot Games are trademarks or registered trademarks of Riot Games, Inc. League of Legends © Riot Games, Inc.

## Change Log

### 1.1.0
* Shorten the Django settings for handling Riot API request errors (in a 1:3 ratio), check out the [documentation](https://django-cassiopeia.readthedocs.io/en/latest/django-setup/) for its new syntax (Ctrl F5 to clean reload in case your brower loads the cached page).
* Moved out the entire setting mapping logic to a separate file for better maintainance, mainly `_cassiopeia.settings.py -> django_cassiopeia.utils.py`.

### 1.0.0
* First Release of Django Cassiopeia
