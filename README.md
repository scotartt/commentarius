De Commentariis
===============

De Commentariis is a web app that allows social annotations and commentaries to be created on ancient texts in TEI-compliant formats.

It runs in a Django container (version 1.10) with Python 3.5.

It was deployed at [decommentariis.net](http://decommenariis.net) which has been inactive for sometime (due to hosting costs), but will be shortly reactivated (as of January 2017).

Licence
=======

This software is licensed using the GNU GPL version 2. See file LICENSE.

No warranty, responsibility, or liability is assumed by the author in any use of this software.

Required modules
================

Currently it runs on python 3.5.2 and django 1.10

Pip commands needed to configure python:

    pip install Django
    pip install allauth
    pip install django-allauth
    pip install django-tastypie
    pip install django-crispy_forms
    pip install lxml
    pip install markdown
