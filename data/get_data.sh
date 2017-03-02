#!/bin/sh

find canonical/CTS_XML_TEI/perseus/greekLit -type f | xargs grep -l 'TEI P4//DTD' | grep 'grc' >greekLitTemp.txt
find canonical/CTS_XML_TEI/perseus/latinLit -type f | xargs grep -l 'TEI P4//DTD' | grep 'lat' >latinLitTemp.txt

find canonical/CTS_XML_TEI/perseus/greekLit -type f | xargs grep -l '<TEI.2>' | grep 'grc' >>greekLitTemp.txt
find canonical/CTS_XML_TEI/perseus/latinLit -type f | xargs grep -l '<TEI.2>' | grep 'lat' >>latinLitTemp.txt

find canonical/CTS_XML_TEI/perseus/latinLit -type f | xargs grep -l '<teiHeader' | grep '\-lat' >teiHeaderLatin.txt

find canonical/CTS_XML_TEI/perseus/greekLit -type f | xargs grep -l 'templates/tei-xl.rng' | grep 'grc' >>greekLitTemp.txt
find canonical/CTS_XML_TEI/perseus/latinLit -type f | xargs grep -l 'templates/tei-xl.rng' | grep 'lat' >>latinLitTemp.txt

cat greekLitTemp.txt | sort -u > canonical/CTS_XML_TEI/perseus/greekLit.txt
cat latinLitTemp.txt | sort -u > canonical/CTS_XML_TEI/perseus/latinLit.txt
rm greekLitTemp.txt latinLitTemp.txt
