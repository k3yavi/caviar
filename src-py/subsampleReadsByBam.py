import click
import pysam

@click.command()
@click.option('--bf',  help='path for bamfile')
@click.option('--rf',  help='path for readfile')
def subsample(bf, rf):
    readList = set([])
    bam = pysam.AlignmentFile(bf, 'rb')
    for line in bam:
        readList.add(line.qname.strip().split('_')[0])
    with open(rf) as rfile, open(bf[:-4]+'.fq', 'w') as wfile:
        for line in rfile:
            if line.strip().split(' ')[0].replace('@','') in readList:
                wfile.write(line)
                for _ in range(3):
                    line = rfile.next()
                    wfile.write(line)
    bam.close()

if __name__=="__main__":
    subsample()

