for $country in doc('country_a.xml')//country/country-tuple
where count(doc('geo_island_a.xml')//geo_island/geo_island-tuple[@country=$country/@code]) > 10
return $country/@name/data()