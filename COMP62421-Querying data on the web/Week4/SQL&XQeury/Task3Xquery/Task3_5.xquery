distinct-values(
for $gr in doc('geo_river_a.xml')//geo_river/geo_river-tuple,
    $r in doc('river_a.xml')//river/river-tuple
where $gr/@country='GB' and $gr/@river=$r/@name
return $r/@length
)