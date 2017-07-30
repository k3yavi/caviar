import click
import pysam

@click.command()
@click.option('--bf',  help='path for bamfile')
def subsample(bf):
    bam = pysam.AlignmentFile(bf, 'rb')
    wBam = pysam.AlignmentFile(bf[:-4]+'_unique.bam', 'wb', template=bam)
    for line in bam:
        if(line.get_tag('NH') == 1):
            wBam.write(line)
    bam.close()
    wBam.close()

if __name__=="__main__":
    subsample()

