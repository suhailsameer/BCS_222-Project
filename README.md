# BNF Structure
```
<program>::=<statement>|<statement><program>
<statement>::=<declaration>|
              <assignment>|
              <IF>|
              <PRINT>
<declaration>::=<type><identfier>;
<assignment>::=<identifier>=<expression>;
<expression>::=<term>|
               <expression>+<term>|
               <expression>-<term>
<term>::=<number>|<identifier>
<IF>::="if" (<condition>) {<program>}
<PRINT>::="print"(expression);
<condition>::=<expression><conditionalOperators><expression>
<conditonalOperators>::= <|>|==|!=
<type>::=int|float
<number>::=0-9+['.'0-9+]*
<identifier>::=[a-zA-Z_][a-zA-Z0-9_]*
```
