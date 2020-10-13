Configuration
=============

Analog has two settings configurable in your project's Django settings:

ANALOG_KINDS
------------

You can use this to add custom log entry kinds.  Kind _mnemonics_ are what
you might usually pass to :func:`add_log_entry`; short, understandable names
for the log entry kind.  These are mapped to integers on the database level.

.. note:: It's a good idea to "namespace" your custom log entry kinds by
          starting them at some arbitrary value, as in the example below.
          In particular, kinds from 0 to 10 are "reserved" by Analog itself.
          However, if you really feel like it, there's nothing stopping you
          from reassigning those kinds too.

For example, an application hell-bent on logging different kinds of food
might declare custom log entry kinds like this.

.. code-block:: python

   _KIND_BASE = 0x10000
   ANALOG_KINDS = {
     "hamburger": _KIND_BASE + 1,
     "tortilla": _KIND_BASE + 2
   }

ANALOG_KIND_LABELS
------------------

This dictionary represents the human-readable, likely localizable labels
for the custom log kinds declared in ``ANALOG_KINDS``.

Declaring labels is optional -- the mnemonic will be substituted instead
if you don't declare them -- but it's definitely good sportsmanship.

.. note:: For your localization convenience, any bare strings here will
          be converted to Django's ``gettext_lazy`` instances.

.. code-block:: python

   ANALOG_KIND_LABELS = {
     "hamburger": "hämmbörger",
     "tortilla": "delicious tortilla"
   }
