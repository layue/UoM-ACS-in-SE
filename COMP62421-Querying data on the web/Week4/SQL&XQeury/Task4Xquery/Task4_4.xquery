for $country in doc('country_e.xml')//country/country-tuple
where count(doc('geo_island_e.xml')//geo_island/geo_island-tuple[country=$country/code]) > 10
return $country/name/data()