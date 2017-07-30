import click
import pysam

@click.command()
@click.option('--bf',  help='path for bamfile')
@click.option('--rf',  help='path for readfile')
def subsample(bf, rf):
    readList = set([])
    with open(rf) as f:
        for line in f:
            readList.add(line.strip())
    bam = pysam.AlignmentFile(bf, 'rb')
    wbam = pysam.AlignmentFile(bf[:-4]+'_mod.bam', 'wb', template=bam)
    for line in bam:
        if line.qname in readList:
            wbam.write(line)
    bam.close()
    wbam.close()

if __name__=="__main__":
    subsample()

