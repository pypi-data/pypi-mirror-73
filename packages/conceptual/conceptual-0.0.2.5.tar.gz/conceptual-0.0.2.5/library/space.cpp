#include <conceptual/space.hpp>

namespace conceptual::core {
  Identifier::Identifier(string name, string id, int dt)
    : name(name), id(id), dt(dt) { }

  bool operator==(const Identifier &lhs, const Identifier& rhs) {
    return lhs.name == rhs.name;
  }
}
