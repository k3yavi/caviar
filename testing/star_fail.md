╭─avi@newton /mnt/scratch5/avi/caviar/testing  ‹master*›
╰─$ grep ""D000684:779:H53GNBCXY:1:1101:3185:21538"" ./b_genome.bam
D000684:779:H53GNBCXY:1:1101:3185:21538 16      chr18   49490453        255     98M     *       0       0       CCTTAAGTTCAGCATTACTCTCTGCGTTTTTACGCATGTGCAGCAAAAATTCAGCACTCTTTTTGGGCCACCGACCTTGTGTCCAGCCCCATTGCTTG   .GAGG..G.AGAG<.GGG.AA...AGIGGA.<...<.GGGAGGGG<.<<.GGAGGGG<<<<A<..........<.AAGGG.G..GG<...GGGAAAGG      NH:i:1  HI:i:1  AS:i:94 nM:i:1

╭─avi@newton /mnt/scratch5/avi/caviar/testing  ‹master*›
╰─$ grep ""D000684:779:H53GNBCXY:1:1101:3185:21538"" ./b_gentrome.bam
D000684:779:H53GNBCXY:1:1101:3185:21538 0       ENST00000582935.1       180     255     98M     *       0       0       CAAGCAATGGGGCTGGACACAAGGTCGGTGGCCCAAAAAGAGTGCTGAATTTTTGCTGCACATGCGTAAAAACGCAGAGAGTAATGCTGAACTTAAGG   GGAAAGGG...<GG..G.GGGAA.<..........<A<<<<GGGGAGG.<<.<GGGGAGGG.<...<.AGGIGA...AA.GGG.<GAGA.G..GGAG.      NH:i:1  HI:i:1


╭─avi@newton /mnt/scratch5/avi/caviar/testing  ‹master*›
╰─$ grep -A1 "D000684:779:H53GNBCXY:1:1101:3185:21538" ./reads.fq
@D000684:779:H53GNBCXY:1:1101:3185:21538 2:N:0:AAATGTGC
CAAGCAATGGGGCTGGACACAAGGTCGGTGGCCCAAAAAGAGTGCTGAATTTTTGCTGCACATGCGTAAAAACGCAGAGAGTAATGCTGAACTTAAGG

╭─avi@newton /mnt/scratch5/avi/caviar/testing  ‹master*›
╰─$ grep "D000684:779:H53GNBCXY:1:1101:3185:21538" ./human.gtf
chr18   HAVANA  transcript      49490261        49490969        .       -       .       gene_id "ENSG00000265681.7"; transcript_id "ENST00000582935.1"; gene_type "protein_coding"; gene_name "RPL17"; transcript_type "retained_intron"; transcript_name "RPL17-013"; level 2; transcript_support_level "2"; havana_gene "OTTHUMG00000179680.6"; havana_transcript "OTTHMT00000448315.1";
chr18   HAVANA  exon    49490793        49490969        .       -       .       gene_id "ENSG00000265681.7"; transcript_id "ENST00000582935.1"; gene_type "protein_coding"; gene_nam$
 "RPL17"; transcript_type "retained_intron"; transcript_name "RPL17-013"; exon_number 1; exon_id "ENSE00002720209.1"; level 2; transcript_support_level "2"; havana_gene "OTTHUMG000$0179680.6"; havana_transcript "OTTHUMT00000448315.1";
chr18   HAVANA  exon    49490261        49490552        .       -       .       gene_id "ENSG00000265681.7"; transcript_id "ENST00000582935.1"; gene_type "protein_coding"; gene_nam$
 "RPL17"; transcript_type "retained_intron"; transcript_name "RPL17-013"; exon_number 2; exon_id "ENSE00002713657.1"; level 2; transcript_support_level "2"; havana_gene "OTTHUMG000$0179680.6"; havana_transcript "OTTHUMT00000448315.1";