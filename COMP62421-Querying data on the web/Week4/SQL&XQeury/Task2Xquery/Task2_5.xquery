for $river in  doc('mondial.xml')//river
where $river/tokenize(@country)='GB'
return $river/length/text()
