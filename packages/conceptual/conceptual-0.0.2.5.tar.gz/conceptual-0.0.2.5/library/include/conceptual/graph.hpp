#pragma once
#include <map>
#include <opencv2/core/mat.hpp>
#include <string>
#include <optional>

#include <conceptual/space.hpp>

namespace conceptual::core {
  using std::map;
  using std::string;
  using std::optional;
  using std::function;
  using cv::Mat;

  class Node {
    map<string,Node> edges;
    std::optional<Mat> result;
    function<Mat(Space&, Node&)> generator;
  public:
    Node(function<Mat(Space&, Node&)> generator);
    void addNode(string key, Node node);
    Mat eval(Space &space);
  };
}
