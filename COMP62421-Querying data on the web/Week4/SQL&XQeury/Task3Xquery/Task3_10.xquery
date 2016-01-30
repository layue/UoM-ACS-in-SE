for $country in doc('country_a.xml')//country/country-tuple
return concat($country/@name/data(),' ',count(doc('geo_island_a.xml')//geo_island/geo_island-tuple[@country=$country/@code]))