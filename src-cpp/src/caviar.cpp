#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <string>

#include "gff.h"

int main(int argc, char* argv[]) {

    if (argc == 1 or argc > 4 or argc < 4) {
        std::cerr << "Usage: caviar [GTF] [pos] [out]\n";
        std::exit(1);
    }

    GffReader reader(argv[1]);
    reader.readAll(true);

    std::cerr << "had count of " << reader.gflst.Count() << "\n";

    size_t nfeat = reader.gflst.Count();

    uint64_t start, end, count{0};
    std::string line;
    std::ifstream posfile (argv[2]);
    std::ofstream wfile (argv[3]);

    if (posfile.is_open() and wfile.is_open()){
      while ( getline (posfile, line) ){
        count += 1;
        start = std::stoi(line, nullptr, 10) << '\n';
        end = start + 30;

        for (size_t i=0; i < nfeat; ++i) {
          GffObj* f = reader.gflst[i];
          if(f->exonOverlap(start, end)){
            int idx = static_cast<int>(f->exonOverlapIdx(start, end));
            GffExon* ex = f->exons[idx];
            wfile << f->getID() << '\t'
                      << ex->getAttr(f->names, "exon_id") << std::endl;
          }
        }

        if(count % 10000 == 0){
          std::cout << "\r Done: " << count <<" lines";
        }
      }
    }
    posfile.close();
    wfile.close();
    std::cout << "Exit Success";
    return 0;
}

