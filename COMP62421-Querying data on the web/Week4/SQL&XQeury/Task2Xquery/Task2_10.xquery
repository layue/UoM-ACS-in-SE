for $country in //country
return concat($country/name/text(),' ',count(//island[tokenize(@country)=$country/@car_code]))
