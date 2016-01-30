for $city in doc('city_a.xml')//city/city-tuple
where $city/@name/data()='Manchester'
return $city
