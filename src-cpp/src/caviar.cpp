#include <iostream>
#include <cstdio>
#include <cstdlib>

#include "gff.h"

int main(int argc, char* argv[]) {

    if (argc == 1 or argc > 2) {
        std::cerr << "Usage: TestGFFParse input\n";
        std::exit(1);
    }

    GffReader reader(argv[1]);
    reader.readAll(true);

    std::cerr << "had count of " << reader.gflst.Count() << "\n";
    size_t nfeat = reader.gflst.Count();
    for (size_t i=0; i < nfeat; ++i) {
       GffObj* f = reader.gflst[i];

       if(f->exonOverlap(13453, 13454)){
         int idx = static_cast<int>(f->exonOverlapIdx(13453, 13454));
         GffExon* ex = f->exons[idx];

         std::cout << f->getID() << '\t' << f->getGeneID() << "\t"
                   << ex->getAttr(f->names, "exon_id") << std::endl;
       }
    }
    std::cout << "Exit Success";
    return 0;
}

