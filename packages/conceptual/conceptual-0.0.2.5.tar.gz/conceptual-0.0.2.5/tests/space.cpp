#include "conceptual/space.hpp"
#include <conceptual/core.hpp>
#include "gtest/gtest.h"

TEST(Space, identifier_equality) {
  conceptual::core::Identifier i("dim1");
  conceptual::core::Identifier i2("dim1");
  EXPECT_EQ (i,  i2);
}
