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
txome = "/mnt/scratch5/avi/alevin/data/mohu/txptome/rsem.transcripts.fa"
genome = "/mnt/scratch5/avi/alevin/data/mohu/genome/mohu.fa"
gtf = "/mnt/scratch5/avi/alevin/data/mohu/gtf/mohu.gtf"

#reads
barcodesFile = "/mnt/scratch5/avi/alevin/data/mohu/reads/10M_1.fq"
readsFile = "/mnt/scratch5/avi/alevin/data/mohu/reads/10M_2.fq"

#-------------------------------------------------
#Star Specific variable
#-------------------------------------------------
overhang = 59
threads = 25

#index
genomeIndexPath = "{}/starData/index/genome".format(pwd)
txomeIndexPath = "{}/starData/index/txome".format(pwd)

#outputPath
txomeOutPath = "{}/starData/txomeOut".format(pwd)
genomeOutPath = "{}/starData/genomeOut".format(pwd)

rule index_genome:
    run:
        shell('echo "Running with sjdbOverhang {overhang}"')
        shell("mkdir -p {genomeIndexPath}")
        shell("{starBin} --runThreadN {threads} --runMode genomeGenerate --genomeDir {genomeIndexPath} --genomeFastaFiles {genome} --limitGenomeGenerateRAM 57993269973 --genomeChrBinNbits 12 --sjdbGTFfile {gtf} --sjdbOverhang {overhang}")

rule index_txome:
    run:
        shell("mkdir -p {txomeIndexPath}")
        shell("{starBin} --runThreadN {threads} --runMode genomeGenerate --genomeDir {txomeIndexPath} --genomeFastaFiles {txome} --limitGenomeGenerateRAM 57993269973 --genomeChrBinNbits 12 --sjdbGTFfile {gtf} --sjdbOverhang {overhang}")

rule align_gentrome:
    run:
        shell("mkdir -p {genomeIndexPath}")
        shell("{starBin} --runThreadN {threads} --genomeDir {genomeIndexPath} --readFilesIn {readsFile} --outFileNamePrefix {genomeOutPath} --outSAMtype BAMUnosrted --quantMode TranscriptomeSAM  GeneCounts --quantTranscriptomeBan Singleend")


rule align_genome:
    run:
        shell("mkdir -p {genomeOutPath}")
        shell("{starBin} --runThreadN {threads} --genomeDir {genomeIndexPath} --readFilesIn {readsFile} --outFileNamePrefix {genomeOutPath} --outSAMtype BAMUnosrted")

rule align_txome:
    run:
        shell("mkdir -p {txomeOutPath}")
        shell("{starBin} --runThreadN {threads} --genomeDir {txomeIndexPath} –-outFilterMultimapNmax 200 -–outFilterMismatchNmax 99999 –-outFilterMismatchNoverLmax 0.2 -–alignIntronMin 1000 –-alignIntronMax 0 –-limitOutSAMoneReadBytes 1000000 --outSAMtype BAMUnosrted --readFilesIn {readsFile} --outFileNamePrefix {txomeOutPath}")
