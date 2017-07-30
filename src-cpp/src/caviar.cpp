#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <string>
#include <thread>
#include <mutex>
#include <vector>
#include <atomic>

#include "gff.h"

bool dumpMap(std::vector<uint64_t>& q,
             std::mutex& ioMutex,
             std::ofstream& wfile,
             size_t& nfeat,
             GffReader& reader,
             std::atomic<uint64_t>& totNum){
  while(totNum != 0 and totNum < q.size()+1){
    ioMutex.lock();
    std::cout << "\r\rRemaining: " << totNum <<" lines";
    uint64_t start = q[totNum];
    totNum -= 1;
    ioMutex.unlock();
    uint64_t end{start+30};

    for (size_t i=0; i < nfeat; ++i) {
      GffObj* f = reader.gflst[i];
      if (start > end) Gswap(start, end);
      for (int j=0;j<f->exons.Count();j++) {
        auto ex = f->exons[j];
        if (ex->overlap(start, end)){
          ioMutex.lock();
          wfile << f->getID() << '\t'
                << ex->getAttr(f->names, "exon_id") << std::endl;
          ioMutex.unlock();
          break;
        }
      }
    }
  }
}

int main(int argc, char* argv[]) {

    if (argc == 1 or argc > 5 or argc < 5) {
        std::cerr << "Usage: caviar [GTF] [pos] [out] [threads]\n";
        std::exit(1);
    }

    GffReader reader(argv[1]);
    reader.readAll(true);

    std::cerr << "GTF has " << reader.gflst.Count() << " features(txps)\n";

    size_t nfeat{reader.gflst.Count()}, numThreads{std::atoi(argv[4])};

    std::string line;
    std::ifstream posfile (argv[2]);
    std::ofstream wfile (argv[3]);
    std::mutex ioMutex;
    std::vector<std::thread> threads;
    std::atomic<uint64_t> totNum{0};
    std::vector<uint64_t> queue;

    if (posfile.is_open() and wfile.is_open()){
      while ( getline (posfile, line) ){
        queue.push_back(std::stoi(line, nullptr, 10));
      }
    }

    totNum = queue.size();
    std::cout<<"total " << totNum << " lines" <<std::endl;

    for (int i = 0; i < numThreads; ++i) {
      // NOTE: we *must* capture i by value here, b/c it can (sometimes, does)
      // change value before the lambda below is evaluated --- crazy!
      auto threadFun = [&, i]() -> void {
        dumpMap(queue, ioMutex, wfile,
                nfeat, reader, totNum);
      };
      threads.emplace_back(threadFun);
    }

    for (int i = 0; i < numThreads; ++i) {
      threads[i].join();
    }


    posfile.close();
    wfile.close();
    std::cout << "\nExit Success";
    return 0;
}
