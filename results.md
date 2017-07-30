a = 544k
b = 441k
c = 5,644k
d = 569k
e = f = 0
g = 280k

Genome = a + b + c + d = 7,198k
Gentrome = b + c = 6,085k
Txome = c + d + g = 6,493k

##3' only Exon-Tree w/ each txp
* b
    402k (overlap)
     39k (non-overlap)
reason being quite clear that UTR Annotation is a problem and
since not present in GTF so not reported by txome
* a
    36k (overlap)
    504k (non-overlap)
Doesn't make sense, read could come from intron, may be?
* d
    104k (overlap)
    465k (non-overlap)
Again, no idea what's happening

##Gene interval tree for intron count
* b
All 441k comes from genomic locus, which make sense.
* a
    411k (overlap)
    133k (non-overlap)
This makes much more sense, since 411k-36k would are coming
from intron region while some 133k are mapped outside of
genomic locus. Could be genes annotation error but no-idea
for now.
* d
    405k (overlap)
    164k (non-overlap)
Confused, but hypothetically these are the cases where there
is confused mapping among txome and genome individually but
once given combination aligner just throws it away.
