distinct-values(
for $gs in doc('geo_sea_e.xml')//geo_sea,
    $country in doc('country_e.xml')//country
where $gs/geo_sea-tuple/country=$country/country-tuple/code
return data($country/country-tuple/name)
)