import click
import sys

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
@click.option('--out',  help='path for out file')
def subsample(gtf, out):
    #works with sorted by sequential txp-exon GTF only
    histTxp = {'eid':"\n"}
    count = 0
    with open(gtf) as f, open(out, 'w') as of:
        for line in f:
            count += 1
            if count % 100000 == 0:
                print "\r Done " + str(count) + " lines",
                sys.stdout.flush()
            if line[0] == "#":
                continue;
            toks = line.strip().split("\t")
            if toks[2] == "transcript":
                of.write(histTxp["eid"]+"\n")
                histTxp = {}
                histTxp ['st'] = toks[6]
                histTxp ['s'] = int(toks[3])
                histTxp ['e'] = int(toks[4])
                histTxp ['es'] = 0
                histTxp ['ee'] = 0
                histTxp ['eid'] = ""
            elif toks[2] == "exon":
                start = int(toks[3])
                end = int(toks[4])
                #check if txp and exon has same starnd
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
                    if(histTxp['es'] == 0 and histTxp['ee'] == 0 and
                       histTxp['eid'] == ""):
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
                    if start > histTxp['es'] or start > histTxp['ee']:
                        printError('Schema breach for start exon "-"')
                    if end > histTxp['es'] or end > histTxp['ee']:
                        printError('Schema breach for end exon "-"')
                else:
                    printError('wrong strand')


if __name__=="__main__":
    subsample()

