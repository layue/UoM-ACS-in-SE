<?xml version="1.0" encoding="UTF-8"?>
<sch:schema xmlns:sch="http://purl.oclc.org/dsdl/schematron" queryBinding="xslt2"
    xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
    
    <sch:pattern>
        <sch:rule context="title">
            <sch:let name="titleName" value="@value"/>
            <sch:assert test="count(//title[@value = $titleName]) = 1">
                ERROR:No two articles share the same name
            </sch:assert>
        </sch:rule>
    </sch:pattern>
    
    <sch:pattern>
        <sch:rule  context="authorName">
            <sch:let name="authorName" value="@value"/>
            <sch:assert test="count(//author/name[@value = $authorName]) >= 1">
                ERROR:Every author occurs in an article also occurs in author list
            </sch:assert>
        </sch:rule>
    </sch:pattern>
    
    <sch:pattern>
        <sch:rule  context="author/institution">
            <sch:let name="institutionName" value="@value"/>
            <sch:assert test="count(//institution/name[@value = $institutionName]) >= 1">
                ERROR:Every institution occurs in an author also occurs in institution list
            </sch:assert>
        </sch:rule>
    </sch:pattern>
</sch:schema>