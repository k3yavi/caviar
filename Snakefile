import sys
###########################################
#Snakefile to compare and run the analysis
###########################################

#-------------------------------------------------
#Initial variable
#-------------------------------------------------
pwd = os.getcwd()

#Binary
starBin = "/mnt/scratch5/avi/alevin/bin/STAR-2.5.3a/bin/Linux_x86_64/STAR"

#Reference
txome = "/mnt/scratch5/avi/alevin/data/human/txptome/rsem.txp.fa"
genome = "/mnt/scratch5/avi/alevin/data/human/genome/whole/GRCh38.primary_assembly.genome.fa"
gtf = "/mnt/scratch5/avi/alevin/data/human/gtf/gencode.v26.primary_assembly.annotation.gtf"
exons_gtf = "/mnt/scratch5/avi/alevin/data/human/gtf/prim_exons.gtf"

#reads
barcodesFile = "/mnt/scratch5/avi/caviar/data/pbmc4k_S1_L001_I1_001.fastq.gz"
readsFile = "/mnt/scratch5/avi/caviar/data/pbmc4k_S1_L001_R2_001.fastq.gz"

#-------------------------------------------------
#Star Specific variable
#-------------------------------------------------
overhang = 97
thread = 15

#index
genomeIndexPath = "{}/starData/index/genome".format(pwd)
txomeIndexPath = "{}/starData/index/txome".format(pwd)

#outputPath
txomeOutPath = "{}/starData/txome/".format(pwd)
genomeOutPath = "{}/starData/genome/".format(pwd)

rule index_genome:
    run:
        shell('echo "Running with sjdbOverhang {overhang}"')
        shell("mkdir -p {genomeIndexPath}")
        shell("{starBin} --runThreadN {thread} --runMode genomeGenerate --genomeDir {genomeIndexPath} --outFileNamePrefix {genomeIndexPath} --genomeFastaFiles {genome} --limitGenomeGenerateRAM 57993269973 --genomeChrBinNbits 12 --sjdbGTFfile {gtf} --sjdbOverhang {overhang}")

rule index_txome:
    run:
        shell("mkdir -p {txomeIndexPath}")
        shell("{starBin} --runThreadN {thread} --runMode genomeGenerate --genomeDir {txomeIndexPath} --outFileNamePrefix {txomeIndexPath} --genomeFastaFiles {txome} --limitGenomeGenerateRAM 57993269973 --genomeChrBinNbits 12")

rule align_gentrome:
    run:
        shell("mkdir -p {genomeOutPath}")
        shell("{starBin} --runThreadN {thread} --genomeDir {genomeIndexPath} --readFilesIn {readsFile} --outFileNamePrefix {genomeOutPath} --outSAMtype BAM Unsorted --quantMode TranscriptomeSAM  GeneCounts --quantTranscriptomeBan Singleend --readFilesCommand gunzip -c")

#rule align_genome:
#    run:
#        shell("mkdir -p {genomeOutPath}")
#        shell("{starBin} --runThreadN {thread} --genomeDir {genomeIndexPath} --readFilesIn {readsFile} --outFileNamePrefix {genomeOutPath} --outSAMtype BAM Unsorted")

rule align_txome:
    run:
        shell("mkdir -p {txomeOutPath}")
        shell("{starBin} --runThreadN {thread} --genomeDir {txomeIndexPath} –-outFilterMultimapNmax 200 -–outFilterMismatchNmax 99999 –-outFilterMismatchNoverLmax 0.2 -–alignIntronMin 1000 –-alignIntronMax 0 –-limitOutSAMoneReadBytes 1000000 --outSAMtype BAM Unsorted --readFilesIn {readsFile} --outFileNamePrefix {txomeOutPath} --readFilesCommand gunzip -c")

#Given gtf and bam it count number of reads coming from genomic feature, inc by 1 if any alignment of read is overlapping
#python countSAMbyfeature.py --gtf ../../alevin/data/mohu/gtf/mohu.gtf  --bam ../testing/subBam/d_genome.bam --pkl ../testing/pkl/gtf_gene.pkl --feature gene

#Given gtf abd bam it counts number of reads coming from 3' exon using txp as feature, inc by 1 if any alignment overlaps
#python countSAMbyExon.py --gtf ../../alevin/data/mohu/gtf/mohu.gtf  --bam ../testing/subBam/d_genome.bam --pkl ../testing/pkl/gtf.pkl
