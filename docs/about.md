# De Commentariis β

(*On Commentaries - beta version*)

This β version web application enables users to 'crowd-source' commentaries on ancient texts. You can construct your own commentaries on ancient texts, and view commentaries others have made. We will soon bring online features for instructors in the Classical Languages to help their advanced classes not only read their assigned texts, but develop ways to critically engage with those texts, both in understanding linguistic constructions and engaging with historical context and textual reception.

https://decommentariis.net/  \
https://github.com/scotartt/commentarius/

## Features
* Create and Edit your own commentary items on any available ancient text
* View other commentary items created by other users
* Vote items from other users to increase their reputation

## Planned features
* Filter items by reputation level
* Collate all your own commentaries for view/print
* View individual users commentaries
* Teachers and Lecturers can create cohorts for their classes

## A note about the works available
We are reliant on works and editions from the Perseus project (see credits) which have been ported to the standard "CTS XML TEI" format. There are many texts which are missing, especially Greek ones (we also haven't yet done the job of converting the Greek text in Betacode format to Unicode, so it looks like gibberish). Also some editions claim to be in the database but no actual text is available due to various parsing errors. Poetry formats are particularly tricky. These sorts of errors will gradually be corrected over time, please have patience. The project founder is a Livy specialist and Livy isn't yet available so please have pity!

## Credits

Ancient text data is licensed from the Perseus Digital Library and taken from their github repository, with the following license conditions:

> Tufts University holds the overall copyright to the Perseus Digital Library; the materials therein (including all texts, translations, images, descriptions, drawings, etc.) are provided for the personal use of students, scholars, and the public.

> Materials within the Perseus DL have varying copyright status: please contact the project for more information about a specific component or object. Copyright is protected by the copyright laws of the United States and the Universal Copyright Convention.

> Unless otherwise indicated, all contents of this repository are licensed under a Creative Commons Attribution-ShareAlike 3.0 United States License. You must offer Perseus any modifications you make. Perseus provides credit for all accepted changes.

## Technology stack

Technology used to make the site as follows:

### back end
* Python 3.5
* Django 1.10
* Django Tasty Pie
* Django All Auth
* lxml xpath

### front end
* html5
* jQuery REST/JSON
* Twitter Bootstrap
* Thomas Park's bootstrap-readable theme

### built with
* Sublime Text 3 editor
* Jet Brains' PyCharm
* git &amp; github
