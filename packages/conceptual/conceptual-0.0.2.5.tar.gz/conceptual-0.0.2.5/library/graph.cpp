#include <conceptual/graph.hpp>

namespace conceptual::core {
  Node::Node(function<Mat(Space&, Node&)> generator) : generator(generator) { };

  void Node::addNode(string key, Node node) {
    this->edges.insert(std::pair<string,Node>(key,node));
  }

  Mat Node::eval(Space &space) {
    if (!this->result.has_value()) {
      this->result = this->generator(space, *this);
    }
    return this->result.value();
  };
}
