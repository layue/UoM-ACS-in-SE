declare default element namespace "http://www.cs.manchester.ac.uk/pgt/COMP60411/el";
(: You should have a single (if somewhat complex) XPath expression here :)
for $x in doc("el1.xml")/dltheory
return $x//atomic | $x//conjunction | $x//exists