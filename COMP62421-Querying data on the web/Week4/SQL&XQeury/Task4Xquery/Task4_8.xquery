for $city in doc('city_e.xml')//city/city-tuple
where fn:starts-with($city/name/data(),'Man')
return $city