declare default element namespace "http://www.cs.manchester.ac.uk/pgt/COMP60411/el";
declare namespace ssd="http://www.cs.manchester.ac.uk/pgt/COMP60411/";
(:You should define a *function* ssd:classexpression, that takes a node and returns true if that node is an class expression,
e.g., a conjunction element. :)

declare function ssd:axiom ($y as node())
as xs:boolean
{
    if (fn:string(fn:node-name($y)) = "atomic" or fn:string(fn:node-name($y)) = "conjunction" or fn:string(fn:node-name($y)) = "exists")
    then true()
    else false()
};

for $x in doc("el1.xml")/dltheory//element()
return
    if ( ssd:axiom($x) )
    then $x
    else()