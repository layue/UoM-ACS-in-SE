for $city_name in  doc('mondial.xml')//city/name
where fn:starts-with($city_name/text(),'Man')
return $city_name/text()