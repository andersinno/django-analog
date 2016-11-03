Django-Analog
=============

[![Build Status](https://travis-ci.org/andersinno/django-analog.svg?branch=master)](https://travis-ci.org/andersinno/django-analog)
[![Coverage Status](https://coveralls.io/repos/andersinno/django-analog/badge.svg?branch=master&service=github)](https://coveralls.io/github/andersinno/django-analog?branch=master)
[![Documentation Status](https://readthedocs.org/projects/django-analog/badge/?version=latest)](http://django-analog.readthedocs.org/en/latest/?badge=latest)

> Simple per-model log models for Django apps

Compatibility
-------------

* Django 1.8+
* Python 2.7 or Python 3.4+

Basic Usage
-----------

```python
from django.db import models
from analog import define_log_model

class MyModel(models.Model):
    value = models.IntegerField(default=0)

MyModelLogEntry = define_log_model(MyModel)

m = MyModel.objects.create(value=42)
m.add_log_entry('Something occurred')
assert m.log_entries.last().message == 'Something occurred'
```

Development
-----------

### Tests

```
py.test
```

### Documentation

```
sphinx-build -b html docs docs\_build
```
