a = **544k**(543947)  
b = **441k**(441144)  
c = **5,644k**(5643479)  
d = **569k**(568971)  
e = f = **0**  
g = **280k**(280162)  

Genome = a + b + c + d = **7,198k**(7197541)  
Gentrome = b + c = **6,085k**(6084623)  
Txome = c + d + g = **6,493k**(6492612)  

## 3' only Exon-Tree w/ each txp
1. **b**  
    * 402k (overlap)  
    * 39k (non-overlap)  
reason being quite clear that UTR Annotation is a problem and
since not present in GTF so not reported by txome
2. **a**  
    * 36k (overlap)  
    * 504k (non-overlap)  
Doesn't make sense, read could come from intron, may be?
3. **d**  
    * 104k (overlap)  
    * 465k (non-overlap)  
Again, no idea what's happening

## Gene interval tree for intron count
1. **b**  
All 441k comes from genomic locus, which make sense.  
2. **a**  
    * 411k (overlap)  
    * 133k (non-overlap)  
This makes much more sense, since 411k-36k would are coming
from intron region while some 133k are mapped outside of
genomic locus. Could be genes annotation error but no-idea
for now.
3. d  
    * 405k (overlap)  
    * 164k (non-overlap)  
Confused, but hypothetically these are the cases where there
is confused mapping among txome and genome individually but
once given combination aligner just throws it away.
