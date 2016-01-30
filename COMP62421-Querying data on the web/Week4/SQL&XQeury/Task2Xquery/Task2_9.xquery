for $country in doc('mondial.xml')//country,
    $organization in doc('mondial.xml')//organization 
where $organization/members/tokenize(@country)=$country/@car_code and
      $organization/established > '1994-12-01' and $country/religion/text()='Buddhist'
return concat($country/name,' ',$organization/name/text())