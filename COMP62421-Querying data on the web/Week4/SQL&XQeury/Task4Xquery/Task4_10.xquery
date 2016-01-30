for $country in doc('country_e.xml')//country/country-tuple
return concat($country/name/data(),' ',count( doc('geo_island_e.xml')//geo_island/geo_island-tuple[country=$country/code]))