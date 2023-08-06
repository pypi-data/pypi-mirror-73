VERSION=4.1.2
DIR="/home/$(whoami)/var"
mkdir -p $DIR

## Download
OPENCV_WEB="https://github.com/opencv"
OPENCV_TAR="$DIR/opencv.tar.gz"
if [ ! -f $OPENCV_TAR ]; then
            wget "$OPENCV_WEB/opencv/archive/$VERSION.tar.gz" -O "$DIR/opencv.tar.gz"
fi
CONTRIB_TAR="$DIR/contrib.tar.gz"
if [ ! -f $CONTRIB_TAR ]; then
            wget "$OPENCV_WEB/opencv_contrib/archive/$VERSION.tar.gz" -O "$DIR/contrib.tar.gz"
fi

## Extract
if [ ! -d $DIR/opencv-$VERSION ] && [ -f $OPENCV_TAR ]; then
            cd $DIR && tar -xvf "opencv.tar.gz"
fi
if [ ! -d $DIR/opencv_contrib-$VERSION ] && [ -f $CONTRIB_TAR ]; then
            cd $DIR && tar -xvf "contrib.tar.gz"
fi

INSTALL_DIR="/usr/local"
CUDA_DIR="/usr/local/cuda"

BUILD_DIR="$DIR/opencv-$VERSION/build"

mkdir -p $BUILD_DIR

cd $BUILD_DIR && cmake \
        -D CMAKE_BUILD_TYPE=RELEASE \
        -D CMAKE_INSTALL_PREFIX=$INSTALL_DIR \
        -D WITH_CUDA=OFF \
        -D WITH_TBB=ON \
        -D WITH_V4L=ON \
        -D WITH_QT=ON \
        -D WITH_OPENGL=ON \
        -D CUDA_TOOLKIT_ROOT_DIR=$CUDA_DIR \
        -D OPENCV_ENABLE_NONFREE=ON \
        -D BUILD_JAVA=OFF \
        -D BUILD_EXAMPLES=OFF \
        -D CUDA_NVCC_FLAGS="--expt-relaxed-constexpr" \
        -D OPENCV_EXTRA_MODULES_PATH="../../opencv_contrib-$VERSION/modules" \
        ..

cd $BUILD_DIR && make -j4 && sudo make -j4 install

