#ifndef BGEN_VARIANT_H_
#define BGEN_VARIANT_H_

#include <cstdint>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
#include <iterator>

#include "genotypes.h"

namespace bgen {

class Variant {
  Genotypes geno;
  int minor_idx = -1;
public:
  Variant(std::ifstream & handle, std::uint64_t & varoffset, int layout, int compression, int expected_n);
  Variant() {};
  ~Variant() {
    if (minor_idx != -1) {
      delete[] dose;
    }
  }
  std::uint64_t next_variant_offset();
  int probs_per_sample();
  void dosages();
  float * minor_allele_dosage();
  float * probs_1d();
  bool phased();
  std::uint8_t * ploidy();
  std::string minor_allele;
  
  std::uint64_t offset;
  std::uint32_t n_samples;
  std::string varid;
  std::string rsid;
  std::string chrom;
  std::uint32_t pos;
  std::uint16_t n_alleles;
  std::vector<std::string> alleles;
  
  float * dose;
};

} // namespace bgen

#endif  // BGEN_VARIANT_H_
