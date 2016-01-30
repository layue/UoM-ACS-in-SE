declare default element namespace "http://www.cs.manchester.ac.uk/pgt/COMP60411/el";
declare namespace ssd="http://www.cs.manchester.ac.uk/pgt/COMP60411/";
(: You should define a *function* ssd:axiom, that takes a node and returns true if that node is an axiom,
e.g., an instance-of, subsumes, etc. element. :)

declare function ssd:axiom ($y as node())
as xs:boolean
{
    if (fn:string(fn:node-name($y)) = "subsumes" or fn:string(fn:node-name($y)) = "equivalent" or fn:string(fn:node-name($y)) = "instance-of" or fn:string(fn:node-name($y)) = "related-to")
    then true()
    else false()
};

for $x in doc("el1.xml")/dltheory/element()
return
    if ( ssd:axiom($x) )
    then $x
    else()
