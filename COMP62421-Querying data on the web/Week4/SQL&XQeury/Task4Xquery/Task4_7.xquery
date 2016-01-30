for $city in doc('city_e.xml')//city/city-tuple
where $city/name/data()='Manchester'
return $city
