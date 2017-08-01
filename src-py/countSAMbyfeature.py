import click
import sys
import pysam
import os.path
import pickle
from intervaltree import IntervalTree, Interval

def printError(msg):
    print msg
    exit(0);

def inBet(s, e, q):
    if q < s or q > e:
        return False
    else:
        return True

@click.command()
@click.option('--gtf',  help='path for gtf')
@click.option('--bam',  help='path for bam file')
@click.option('--pkl',  help='pickle file gtf dump')
@click.option('--feature',  help='feature can be [CDS, UTR]')
def subsample(gtf, bam, pkl, feature):
    if( not os.path.isfile(pkl)):
        #works with sorted by sequential txp-exon GTF only
        histTxp = {}
        count = 0
        init = True
        featDict = {}
        with open(gtf) as f:
            for line in f:
                count += 1
                if count % 100000 == 0:
                    print "\r Done " + str(count) + " lines",
                    sys.stdout.flush()
                if line[0] == "#":
                    continue;
                toks = line.strip().split("\t")
                if toks[2] == feature:
                    chromo = toks[0]
                    start = int(toks[3])
                    end = int(toks[4])
                    if start == end:
                        continue
                    if chromo not in featDict:
                        featDict[chromo] = IntervalTree()
                    featDict[chromo].addi(start, end, "")
        pickle.dump( featDict, open( pkl, "wb" ) )
    else:
        print "importing pickle"
        featDict = pickle.load( open( pkl, "rb" ) )
        print "GTF Pickle import complete"

    print "\n"

    with pysam.AlignmentFile(bam, 'rb') as f:
        nonGTF = 0
        noOverlap = 0
        overlap = 0
        count = 0
        hist = {'n':"", 'f':False}
        for line in f:
            count += 1
            if (count % 100000 == 0):
                print "\rDone " + str(count) + " reads",
                sys.stdout.flush()
            if hist['n'] == line.query_name and hist['f'] == True:
                continue
            elif hist['n'] != line.query_name:
                if hist['f'] == False:
                    noOverlap += 1
                hist['n'] = line.query_name
                hist['f'] = False

            chromo = line.reference_name
            if chromo not in featDict:
                continue
            pos = int(line.reference_start)
            iTree = featDict[chromo]
            if len(iTree[pos-50:pos+50]):
                overlap += 1
                hist['f'] = True

        print "\nNo Overlap count: " + str(noOverlap)
        print "Overlap count: " + str(overlap)

if __name__=="__main__":
    subsample()

