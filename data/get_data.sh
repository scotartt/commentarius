#!/bin/sh

find canonical/CTS_XML_TEI/perseus/greekLit -type f | xargs grep -l 'TEI P4//DTD' | grep 'perseus-grc' >greekLitTemp.txt
find canonical/CTS_XML_TEI/perseus/latinLit -type f | xargs grep -l 'TEI P4//DTD' | grep 'perseus-lat' >latinLitTemp.txt

find canonical/CTS_XML_TEI/perseus/greekLit -type f | xargs grep -l '<TEI.2>' | grep 'perseus-grc' >>greekLitTemp.txt
find canonical/CTS_XML_TEI/perseus/latinLit -type f | xargs grep -l '<TEI.2>' | grep 'perseus-lat' >>latinLitTemp.txt

find canonical/CTS_XML_TEI/perseus/greekLit -type f | xargs grep -l 'templates/tei-xl.rng' | grep 'perseus-grc' >>greekLitTemp.txt
find canonical/CTS_XML_TEI/perseus/latinLit -type f | xargs grep -l 'templates/tei-xl.rng' | grep 'perseus-lat' >>latinLitTemp.txt

cat greekLitTemp.txt | sort -u > greekLit.txt 
cat latinLitTemp.txt | sort -u > latinLit.txt
rm greekLitTemp.txt latinLitTemp.txt
