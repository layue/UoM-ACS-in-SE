for $ismemountry in doc('country_e.xml')//*/country-tuple,
    $org in doc('organization_e.xml')//*/organization-tuple,
    $ismem in doc('ismember_e.xml')//*/ismember-tuple,
    $reli in doc('religion_e.xml')//*/religion-tuple
where $ismemountry/code=$ismem/country and $ismem/organization=$org/abbreviation and $ismemountry/code=$reli/country and $reli/name='Buddhist' and $org/established>'1994-12-01'
return concat(data($ismemountry/name),' ',data($org/name))