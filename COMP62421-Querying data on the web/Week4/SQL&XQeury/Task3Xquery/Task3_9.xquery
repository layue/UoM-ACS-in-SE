for $ismemountry in doc('country_a.xml')//*/country-tuple,
    $org in doc('organization_a.xml')//*/organization-tuple,
    $ismem in doc('ismember_a.xml')//*/ismember-tuple,
    $reli in doc('religion_a.xml')//*/religion-tuple
where $ismemountry/@code=$ismem/@country and $ismem/@organization=$org/@abbreviation and $ismemountry/@code=$reli/@country and $reli/@name='Buddhist' and $org/@established>'1994-12-01'
return concat(data($ismemountry/@name),' ',data($org/@name))