#include "xmol/io/pdb/PdbReader.h"
#include "xmol/io/pdb/PdbRecord.h"
#include "xmol/io/PdbInputFile.h"
#include <fstream>

using namespace xmol::io;
using namespace xmol::io::pdb;

PdbInputFile::PdbInputFile(std::string filename, Dialect dialect, bool read_now)
    : m_filename(std::move(filename)), m_dialect(dialect) {
  if (read_now) {
    read();
  }
}

PdbInputFile& PdbInputFile::read() {
  AlteredPdbRecords alteredPdbRecords(StandardPdbRecords::instance());
  switch (m_dialect) {
  case (Dialect::AMBER_99):
    alteredPdbRecords.alter_record(pdb::RecordName("ATOM"), pdb::FieldName("serial"), {7, 12});
    break;
  case (Dialect::STANDARD_V3):
    break;
  }

  std::ifstream in(m_filename);
  if (!in){
    throw PdbReadError("Can't read `"+m_filename+"`");
  }
  m_frames = PdbReader(in).read_frames(alteredPdbRecords);

  m_n_frames = m_frames.size();
  if (!m_frames.empty()) {
    m_n_atoms = m_frames[0].n_atoms();
  }
  return *this;
}

size_t PdbInputFile::n_frames() const { return m_n_frames; }
size_t PdbInputFile::n_atoms() const { return m_n_atoms; }
void PdbInputFile::read_coordinates(size_t index, proxy::CoordSpan& coordinates) {
  assert(!m_frames.empty());
  assert(m_current_frame == index);

  Frame& frame = m_frames[index];
  if (coordinates.size() != frame.n_atoms()) {
    throw PdbReadError("Wrong of atoms in " + std::to_string(index) + " frame in `" + m_filename + "`. Expected " +
                       std::to_string(coordinates.size()));
  }
  coordinates._eigen() = frame.coords()._eigen();
}
void PdbInputFile::advance(size_t shift) {
  m_current_frame += shift;
  if (m_current_frame >= n_frames()) {
    m_frames.clear();
    m_current_frame = 0;
    return;
  }
  if (m_frames.empty()) {
    read();
  }
}
xmol::geom::UnitCell PdbInputFile::read_unit_cell(size_t index, const xmol::geom::UnitCell& cell) {
  return m_frames[index].cell;
}
