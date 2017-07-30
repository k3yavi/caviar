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
def subsample(gtf, bam, pkl):
    if( not os.path.isfile(pkl)):
        #works with sorted by sequential txp-exon GTF only
        histTxp = {}
        count = 0
        init = True
        utrDict = {}
        with open(gtf) as f:
            for line in f:
                count += 1
                if count % 100000 == 0:
                    print "\r Done " + str(count) + " lines",
                    sys.stdout.flush()
                if line[0] == "#":
                    continue;
                toks = line.strip().split("\t")
                if toks[2] == "transcript":
                    if(init):
                        init = False
                    else:
                        chromo = histTxp['chr']
                        estart = histTxp['es']
                        eend = histTxp['ee']
                        if chromo not in utrDict:
                            utrDict[chromo] = IntervalTree()
                        utrDict[chromo].addi(estart,
                                             eend,
                                             histTxp['eid'])
                    histTxp = {}
                    histTxp ['chr'] = toks[0]
                    histTxp ['st'] = toks[6]
                    histTxp ['s'] = int(toks[3])
                    histTxp ['e'] = int(toks[4])
                    histTxp ['es'] = 0
                    histTxp ['ee'] = 0
                    histTxp ['eid'] = ""
                elif toks[2] == "exon":
                    start = int(toks[3])
                    end = int(toks[4])
                    if end-start < 5:
                        continue
                    #check if txp and exon has same strand
                    if toks[6] != histTxp['st']:
                        printError('strand diff error')
                    #check if exon is within txp boundary
                    if not inBet(histTxp['s'], histTxp['e'], start):
                        printError('Txp Left boundary breach')
                    if not inBet(histTxp['s'], histTxp['e'], end):
                        printError('Txp Right boundary breach')

                    #analyze for for pos strand
                    if toks[6] == '+':
                        if start < histTxp['es'] or start < histTxp['ee']:
                            printError('Schema breach for start exon')
                        if end < histTxp['es'] or end < histTxp['ee']:
                            printError('Schema breach for end exon')
                        histTxp['es'] = start
                        histTxp['ee'] = end
                        grab = False
                        for elem in toks[-1].split():
                            if grab:
                                histTxp['eid'] = elem[1:-2]
                                break
                            if elem == "exon_id":
                                grab = True
                    elif toks[6] == '-':
                        if ((start > histTxp['es'] or start > histTxp['ee'])
                        and histTxp['es']) != 0:
                            printError('Schema breach for start exon "-"')
                        if ((end > histTxp['es'] or end > histTxp['ee'])
                        and histTxp['es']) != 0:
                            printError('Schema breach for end exon "-"')
                        histTxp['es'] = start
                        histTxp['ee'] = end
                        grab = False
                        for elem in toks[-1].split():
                            if grab:
                                histTxp['eid'] = elem[1:-2]
                                break
                            if elem == "exon_id":
                                grab = True
                                continue
                    else:
                        printError('wrong strand')
        pickle.dump( utrDict, open( pkl, "wb" ) )
    else:
        print "importing pickle"
        utrDict = pickle.load( open( pkl, "rb" ) )
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
            if chromo not in utrDict:
                continue
            pos = int(line.reference_start)
            iTree = utrDict[chromo]
            if len(iTree[pos-30:pos+30]):
                overlap += 1
                hist['f'] = True

        print "\n No Overlap count: " + str(noOverlap)
        print "Overlap count: " + str(overlap)

if __name__=="__main__":
    subsample()

