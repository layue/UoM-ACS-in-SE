for $city in doc('city_a.xml')//city/city-tuple
where fn:starts-with($city/@name/data(),'Man')
return $city