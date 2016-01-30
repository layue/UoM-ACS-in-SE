<?xml version="1.0" encoding="UTF-8"?>
<sch:schema xmlns:sch="http://purl.oclc.org/dsdl/schematron" queryBinding="xslt2"
    xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
    <sch:pattern>
        <sch:rule context="family">
            <sch:let name="L" value="@name" />
            <sch:assert test="$L = //MainContact/LastName">
                The name of family should coincide with its last name
            </sch:assert>
            
            <sch:let name="fName" value="@name"/>
            <sch:assert test="count(//family[@name = $fName]) = 1">
                No two families share the same name
            </sch:assert>
            
            <sch:let name="L" value="@name"/>
            <sch:assert test="count(//period[@family = $L]) >= 1">
                Every family should occur in some occupancy
            </sch:assert>
            
            <sch:let name="fName" value="@name"/>
            <sch:assert test="count(distinct-values(//period[@family = $fName]/@time)) >= count(distinct-values(//period/@time))">
                For each period, each family occupies some house
            </sch:assert>
        </sch:rule>
    </sch:pattern>
    
    <sch:pattern>
        <sch:rule context="house">
            <sch:assert test="count(//house[@castle = 'true']) = 1">
                There should be exactly one house that is a castle
            </sch:assert>
            
            <sch:let name="hName" value="@name"/>
            <sch:assert test="count(//period[@house = $hName]) >= 1">
                Every house should occur in some occupancy
            </sch:assert>
        </sch:rule>
    </sch:pattern>
    
      
    <sch:pattern>
        <sch:rule context="period">
            <sch:let name="fName" value="@family"/>
            <sch:assert test="count(//family[@name = $fName]) >= 1">
                Every family that occurs in an occupancy also occurs in one of the families
            </sch:assert>
            
            <sch:let name="hName" value="@house"/>
            <sch:assert test="count(//house[@name = $hName]) >= 1">
                Every house that occurs in an occupancy also occurs in one of the houses
            </sch:assert>
            
            <sch:let name="t" value="@time"/>
            <sch:let name="hName" value="@house"/>
            <sch:assert test="count(//period[@time = $t and @house = $hName])&lt; 2">
                For every period, each house is occupied by at most one family
            </sch:assert>
            
        </sch:rule>
    </sch:pattern>
    
</sch:schema>