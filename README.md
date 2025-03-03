# BNF Structure
```
<program>::=<statement>|<statement><program>
<statement>::=<declaration>|<assignment>|<IF>|<PRINT>
<declaration>::=<type><identfier>;
<assignment>::=<identifier>=<expression>;
<expression>::=<term>|<expression>+<term>|<expression>-<term>|<expression>*<term>|<expression>/<term>
<IF>::="if" (<condition>) {<program>}
<PRINT>::="print"(expression);
<term>::=<number>|<identifier>|<string>
<condition>::=<expression><conditionalOperators><expression>
<conditonalOperators>::= <|>|==|!=
<type>::=int|float|string
<number>::=0-9+['.'0-9+]*
<string>::=".*"
<identifier>::=[a-zA-Z_][a-zA-Z0-9_]*
```
