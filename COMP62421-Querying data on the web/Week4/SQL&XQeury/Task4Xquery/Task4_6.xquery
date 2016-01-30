(
  for $country in doc('country_e.xml')//country-tuple
  let $sl := sum(
    for $r in distinct-values(doc('geo_river_e.xml')//geo_river-tuple[country=$country/code]/river)
    let $rl := doc('river_e.xml')//river-tuple/length[data()!='MISSING']
    return $rl
    )
order by $sl descending 
return $country/name/data()
)[position()=1 to 10]