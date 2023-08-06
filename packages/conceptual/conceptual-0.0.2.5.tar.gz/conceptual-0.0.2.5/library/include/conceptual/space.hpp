#pragma once
#include <map>
#include <string>
#include <optional>
#include <functional>
#include <vector>

#include <opencv2/core.hpp>
#include <tuple>

namespace conceptual::core {
  using std::map;
  using std::string;
  using std::optional;
  using std::function;
  using std::tuple;
  using std::vector;
  using cv::Mat;

  class Point {
    vector<tuple<string,float,float>> dimensions;
  };

  class Field {
    Mat mat;
    optional<Point> point;
  public:
    Field(Mat mat);
    Point collapse();
  };

  class Identifier {
  public:
    const string name;
    const string id;
    const int dt;
    Identifier(string name, string id = "", int dt = 0);
  };
  bool operator==(const Identifier &lhs, const Identifier& rhs);

  using FieldCache = map<Identifier, Field>;


  class Cache {
    map<Identifier,Field> cache;
  public:
    void insert(string name, Field field);
    Cache step();
  };

  class Space {
    map<string,Point> representations;

    map<string,function<FieldCache(void)>> generatorss;
    map<string,function<Field(void)>> generators;
    map<string,function<Field(Field)>> gens;
    map<string,function<Field(Field, Field)>> gens7;
    map<string,function<Field(vector<Field>)>> gens5;
  };
}
