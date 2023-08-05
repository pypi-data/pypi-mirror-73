The data is orgainized as a dictionary in the [`tzcity/__init__.py`](https://github.com/ju-sh/tzcity/blob/master/tzcity/__init__.py) file where each key is a time zone name whose value is a list of cities associated with that time zone.

Inaccuracies or spelling mistakes, if any, are regretted and can be corrected.

A good source of data: http://download.geonames.org/export/dump/

---

Generally, the mapping is between a time zone and a major cities in it.

The cities of a time zone may be ordered by its population.

The city whose name is part of the time zone is always included.

---

In case of multiple cities with the same name, use the more populous city.

---

For backward compatibility, the cities which have been added may not be removed. But new cities may be added as needed.

---

Inorder to limit the size of the package, only most populous cities of each time zone may be added.

---

A country or region name is mapped to its time zone only if that country has only one time zone.

Steer clear of controversial topics like territorial disputes.
