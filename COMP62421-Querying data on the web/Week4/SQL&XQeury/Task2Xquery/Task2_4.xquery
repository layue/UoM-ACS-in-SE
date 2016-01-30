for $country in  doc('mondial.xml')//country
where count( doc('mondial.xml')//island[tokenize(@country)=$country/@car_code]) > 10
return $country/name/text()
