
declare namespace bjp = 'http://ex.org/';

declare function bjp:nsBindingsForNode($node)
{
    for $n in $node
    for $pre in in-scope-prefixes($n)
    for $ns in namespace-uri-for-prefix($pre, $n)
    return <nsb pre="{$pre}" ns="{$ns}" />
};

declare function bjp:multiPrefixedNs($bindings)
{
    for $b in $bindings
    for $b2 in $bindings
    where ($b/@pre = $b2/@pre) and not($b/@ns = $b2/@ns)
    return <multi>{$b}{$b2}</multi>
};

declare function bjp:isDeceptive($root)
{
    for $m in bjp:multiPrefixedNs(bjp:nsBindingsForNode($root))
    return "YES - it's deceptive!"
};

distinct-values(bjp:isDeceptive(//*))