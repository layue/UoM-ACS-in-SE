distinct-values(
for $country in doc('mondial.xml')//country,
    $sea in doc('mondial.xml')//sea/tokenize(@country)
where $country/@car_code = $sea
return $country/name/text()
)