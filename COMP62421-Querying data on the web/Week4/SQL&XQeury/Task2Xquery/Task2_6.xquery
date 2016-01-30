(
  for $country in  doc('mondial.xml')//country
  let $sum := sum( doc('mondial.xml')//river[tokenize(@country)=$country/@car_code]/length)
  order by $sum descending
  return $country/name/text()
) [position() = 1 to 10]