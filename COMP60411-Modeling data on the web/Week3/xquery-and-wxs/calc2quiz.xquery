import schema default element namespace "" at "flashcardhtml.xsd";
import schema namespace q="http://www.cs.manchester.ac.uk/pgt/COMP60411/examples/quiz" at "quiz.xsd";

declare function local:expr2humanReadable($expr) {
    (:Replace this with a function that turns the XML into a nice string:)
    (:let $x := "3 + 5"
    return $x:)
    let $children := $expr/*
    return
        if(fn:name($expr) = "expr")
        then local:expr2humanReadable($children)
        else if(fn:name($expr) = "number")
        then $expr
        else
            switch(fn:name($expr))
                case "plus" return concat("(", local:expr2humanReadable($children[1]), "+", local:expr2humanReadable($children[2]), ")")
                case "times" return concat("(", local:expr2humanReadable($children[1]), "*", local:expr2humanReadable($children[2]), ")")
                case "minus" return concat("(", local:expr2humanReadable($children[1]), "-", local:expr2humanReadable($children[2]), ")")
                case "dividedBy" return concat("(", local:expr2humanReadable($children[1]), "/", local:expr2humanReadable($children[2]), ")")
                default return "ERROR"
                
};

declare function local:answerFor($expr) as xs:decimal{
    (:Replace this with a function that calculates the value of the expression.:)
    (:let $x := 9
    return $x:)
    let $children := $expr/*
    return
        if(fn:name($expr) = "number")
        then xs:decimal($expr)
        else if(fn:name($expr) = "expr")
        then local:answerFor($children)
        else
            switch(fn:name($expr))
                case "plus" return xs:decimal(local:answerFor($children[1])) + xs:decimal(local:answerFor($children[2]))
                case "times" return xs:decimal(local:answerFor($children[1])) * xs:decimal(local:answerFor($children[2]))
                case "minus" return xs:decimal(local:answerFor($children[1])) - xs:decimal(local:answerFor($children[2]))
                case "dividedBy" return xs:decimal(local:answerFor($children[1])) div xs:decimal(local:answerFor($children[2]))
                default return "ERROR"
};  

validate{<html>
    <head>
        <title>{/*/q:title/text()}</title>
        <script type="text/javascript" src="miniformvalidator.js"/>
    </head>
    <body>
        <h1>{/*/q:title/text()}</h1>
        <form>
            <ol>{let $exprs := /*/q:expr, 
                     $count := count($exprs)
                 for $i in (1 to $count)
                 let $expr := $exprs[$i]
                 let $id := concat("q", $i)
                 return 
                 <li>
                    {local:expr2humanReadable($expr)}=
                    <input type="text" id="{$id}" data-answer="{local:answerFor($expr)}" size="8" />
                    <span>
                        <input type="button" onclick="check(document.getElementById('{$id}'))"
                            value="Check answer" />
                    </span>
                 </li>}
            </ol>
        </form>
    </body>
</html>}