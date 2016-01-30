(
  for $country in doc('country_a.xml')//country-tuple
  let $sl := sum(
    for $gr in distinct-values(doc('geo_river_a.xml')//geo_river-tuple[@country=$country/@code]/@river)
    let $rl := doc('river_a.xml')//river-tuple/@length[data()!='MISSING']
    return $rl
    )
  order by $sl descending 
  return $country/@name/data()
)[position()=1 to 10]