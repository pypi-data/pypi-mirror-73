Django APScheduler
================================

** HELP NEEDED WITH MAINTENANCE **

If anyone feels up to helping maintain this package, please PM me and we can get you some privileges.


[![Build status](http://travis-ci.org/jarekwg/django-apscheduler.svg?branch=master)](http://travis-ci.org/jarekwg/django-apscheduler)
[![codecov](https://codecov.io/gh/jarekwg/django-apscheduler/branch/master/graph/badge.svg)](https://codecov.io/gh/jarekwg/django-apscheduler)
[![PyPI version](https://badge.fury.io/py/django_apscheduler.svg)](https://badge.fury.io/py/django-apscheduler)

[APScheduler](https://github.com/agronholm/apscheduler) for [Django](https://github.com/django/django).

This little wrapper around APScheduler enables storing persistent jobs in the database using Django's ORM rather than requiring SQLAlchemy or some other bloatware.

Features in this project:

* Work on both python2.* and python3+
* Manage jobs from Django admin interface
* Monitor your job execution status: duration, exception, traceback, input parameters.

Installation
------------

```python
pip install django-apscheduler
```

Usage
-----

* Add ``django_apscheduler`` to ``INSTALLED_APPS`` in your Django project settings, You can also specify a different
format for displaying runtime timestamps in the Django admin site using ``APSCHEDULER_DATETIME_FORMAT``:
  ```python

  INSTALLED_APPS = (
    ...
    "django_apscheduler",
  )

  APSCHEDULER_DATETIME_FORMAT =  "N j, Y, f:s a"  # Default

  ```

* Run migrations:
  ```python
  ./manage.py migrate
  ```
* Instantiate a new scheduler as you would with APScheduler. For example:
  ```python
  from apscheduler.schedulers.background import BackgroundScheduler

  scheduler = BackgroundScheduler()
  ```
* Instruct the scheduler to use ``DjangoJobStore``:
  ```python

  from django_apscheduler.jobstores import DjangoJobStore

  # If you want all scheduled jobs to use this store by default,
  # use the name 'default' instead of 'djangojobstore'.
  scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
  ```

* If you want per-execution monitoring, call register_events on your scheduler:
  ```python

    from django_apscheduler.jobstores import register_events
    register_events(scheduler)
  ```

  It provides the following interface:
  ![](http://dl3.joxi.net/drive/2017/05/19/0003/0636/258684/84/bebc279ecd.png)

*  Old job executions can be deleted with:
  ```python
    DjangoJobExecution.objects.delete_old_job_executions(604_800)  # Delete job executions older than 7 days
  ```

* Register any jobs as you would normally. Note that if you haven't set ``DjangoJobStore`` as the ``'default'`` job store,
  you'll need to include ``jobstore='djangojobstore'`` in your ``scheduler.add_job`` calls.

* **Don't forget to give each job a unique id. For example:**
  ```python

  @scheduler.scheduled_job("interval", seconds=60, id="job")
  def job():
    ...
  ```
  or use custom decorator for job registration. It will give id automatically:
  ```python
  from django_apscheduler.jobstores import register_job

  @register_job("interval", seconds=60)
  def job():
    ...
  ```

* Start the scheduler:
  ```python
  scheduler.start()
  ```

A full example project can be found in the example dir. Code snippet:
```python
import time

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")

@register_job(scheduler, "interval", seconds=1)
def test_job():
    time.sleep(4)
    print("I'm a test job!")
    # raise ValueError("Olala!")

register_events(scheduler)

scheduler.start()
print("Scheduler started!")

```
