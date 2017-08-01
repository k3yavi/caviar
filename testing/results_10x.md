a = **38M**(38,348,007)  
b = **10M**(10,051,964)  
d = **17.5M**(17,504,096)  
g = **513k**(513,449)  

Genome = a + b + c + d = **183M**(182,448,569)  
Gentrome = b + c = **127M**(126,596,466)  
Txome = c + d + g = **135M**(134,562,047)  

| feat/area |  a(38M) | b(10M)  | d(17.5M)  |
|---|---|---|---|
| *gene* |   |   |   |
| overlap  |  35M | 10M  | 16M  |
| non-overlap  | 3M  | 880  | 1.5M  |
|   |   |   |   |
| *exon* |   |   |   |
| overlap  |  829k | 10M  | 1.2M  |
| non-overlap  | 37.9M  | 37k  | 16.3M  |
|   |   |   |   |
| *3'-exon* |   |   |   |
| overlap | 430k | 9.1M | 800k |
| non-overlap | 37.9M | 900k | 16.7M |
|   |   |   |   |



* Q: Why does **b** 10M is not mapped by txome?  
  * Almost *none* intergenic data
  * Almost everything is inside *exonic* region.
  * Only (900k-37k) out of 10M is from **non** 3' exons i.e. padding would not help alot.

* Q: Why does **a** 38M not mapped by txome?  
  * 3M are intergenic so even genomce can't map it
  * 34.5M(37.5M-3M) are intronic-region (can we recover from these?) so txome can't map.
  * only 829k are from exonic of which 430k is from 3'

* Q: Can we possibly gain anything by padding in any set (a,b,d)?  

