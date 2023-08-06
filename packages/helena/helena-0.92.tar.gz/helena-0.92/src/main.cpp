#include <pybind11/pybind11.h>
#include<pybind11/numpy.h>

//#include <boost/config.hpp>
//#include <boost/mpl/assert.hpp>
//#include <boost/mpl/int.hpp>
//
//#include <boost/geometry.hpp>
//#include <boost/geometry/core/access.hpp>
//#include <boost/geometry/core/assert.hpp>
//#include <boost/geometry/core/coordinate_type.hpp>
//#include <boost/geometry/core/coordinate_system.hpp>
//#include <boost/geometry/core/coordinate_dimension.hpp>

#include <iostream>

#include "globimap.hpp"

/**Definition of the namespaces*/
namespace py = pybind11;
//namespace bg = boost::geometry;

/** Definition of the Globimaps class */
typedef GloBiMap<bool> globimap_t;

/**
 * This template is a tool to call a function f(i,j,value) for each entry of a 2D matrix self.
 * @tparam func The type of the function `f`.
 * @param mat the `data` to process.
 * @param f the function called for every element within the matrix.
 */
template<typename func>
void map_matrix(py::array_t<double> mat, func f){
    auto ref = mat.unchecked<2>();

    if (mat.request().ndim != 2)
        throw(std::runtime_error("2D array expected"));

    for (int x=0; x < ref.shape(0); x++)
        for(int y=0; y < ref.shape(1); y++)
            f(x,y,ref(x,y));
}

/**
 * Wrap 2D C++ array (given as pointer) to a numpy object.
 * @param data the data to convert from c++ to a numpy array.
 * @param h height of the array.
 * @param w width of the array.
 * @return the `data` as numpy array.
 */
auto wrap2D(std::vector<double>* data, size_t h, size_t w) {
    std::unique_ptr<std::vector<double> > seq_ptr = std::make_unique<std::vector<double>>((*data)); // Unique ptr does not leak if for some reason py::capsule would throw.
    auto capsule = py::capsule(seq_ptr.get(), [](void *p) { std::unique_ptr<std::vector<double> >(reinterpret_cast<std::vector<double> *>(p)); });
    seq_ptr.release();

    return py::array_t<double>({ h, w }, data->data(), capsule);
}

/**
 * Interface module for the python code.
 *
 * This module provides several functions for the use of Globimaps in Python.
 */
PYBIND11_MODULE(globimap, m) {
    m.doc() = R"pbdoc(
        Global Binary Map - GloBiMap
        -----------------------

        .. currentmodule:: globimap

        .. autosummary::
           :toctree: _generate

           configure
           summery
           gut
           get
           clear
           map
           enforce
           rasterize
           correct
    )pbdoc";

    py::class_<globimap_t>(m, "globimap")
            .def(py::init<>())
            .def("configure", +[](globimap_t &self, size_t k, size_t m)  {  self.configure(k,m);}, R"pbdoc(
                Configure the GloBiMap filter.

                Parameters
                ----------
                k : int
                    The number of hash functions.
                m : int
                    The length of the filter as the exponent of an exponentiation with the power of two.

            )pbdoc")

            .def("summary", +[](globimap_t &self) { return self.summary();}, R"pbdoc(
                Summarize specific filter characteristics, such as the fraction of zero or the number of ones.
                )pbdoc")

            .def("put", +[](globimap_t &self, uint32_t x, uint32_t y) { self.put({x,y});}, R"pbdoc(
                Set a pixel at the GloBiMap filter at x,y.

                Parameters
                ----------
                x: int
                    Position in x direction.
                y: int
                    Position in y direction.
                )pbdoc")

            .def("get", +[](globimap_t &self, uint32_t x, uint32_t y) { return self.get({x,y});}, R"pbdoc(
                Get a pixel (as a bool) from position x,y.

                Parameters
                ----------
                x: int
                    Position in x direction.
                y: int
                    Position in y direction.
                )pbdoc")

            .def("clear", +[](globimap_t &self){self.clear();}, R"pbdoc(
                The filter will be reset, so all values within the GloBiMap filter will set to zero.
                )pbdoc")

            .def("map", +[](globimap_t &self, py::array_t<double> mat, int o0, int o1) {

                auto f = [&](int x, int y, double v){
                    if (v != 0 && v!= 1)
                        throw(std::runtime_error("data is not binary."));
                    if (v == 1)
                        self.put({static_cast<uint32_t>(o0+x),static_cast<uint32_t>(o1+y)});
                };

                map_matrix(mat, f);
            }, R"pbdoc(
                Maps a  2D array of input data into the GloBiMap filter

                Parameters
                ----------
                mat : array_like
                    Elements to add to the filter.
                o0 : int
                    Lower bound of the data location in the infinite space.
                o1 : int
                    Upper bound of the data location in the infinite space.
                )pbdoc")

            .def("enforce", +[](globimap_t &self, py::array_t<double> mat, int o0, int o1){

                auto f = [&](int x, int y, double v){
                    if (v==0 && self.get({static_cast<uint32_t>(o0+x),static_cast<uint32_t>(o1+y)})) // this is a false positive
                        self.add_error({static_cast<uint32_t>(o0+x),static_cast<uint32_t>(o1+y)});
                };

                map_matrix(mat, f);
            }, R"pbdoc(
                Adds error correction information for the region map with these parameters would affect.

                Parameters
                ----------
                mat : array_like
                    Elements to add to the filter.
                o0 : int
                    Lower bound of the data location in the infinite space.
                o1 : int
                    Upper bound of the data location in the infinite space.
                )pbdoc")

            .def("rasterize", +[](globimap_t& self, size_t x, size_t y, size_t s0, size_t s1){
                std::vector<double>* v = &self.rasterize(x,y,s0,s1);
                return wrap2D(v, s0, s1);
            }, R"pbdoc(
                rasterize region from x,y with width s0 and height s1 and get a 2D numpy matrix back.

                Parameters
                ----------
                x : int
                    Position in x direction.
                x: int
                    Position in y direction.
                s0 : int
                    Height of the array.
                s1 : int
                    Width of the array.
                )pbdoc")

            .def("correct", +[](globimap_t& self, size_t x, size_t y, size_t s0, size_t s1) {
                std::vector<double>* v = &self.apply_correction(x, y, s0, s1);
                return wrap2D(v, s0, s1);;
            }, R"pbdoc(
                Apply correction (on local data cache, use rasterize before! There is no check you did it!)

                Parameters
                ----------
                x : int
                    Position in x direction.
                x: int
                    Position in y direction.
                s0 : int
                    Height of the array.
                s1 : int
                    Width of the array.
                )pbdoc");
// HACK: VERSION_INFO throws an error within the windows compiler so I replaced it with this hack.
// TODO: Do it on the right way:
/* right way
#ifdef VERSION_INFO
        m.attr("__version__") = VERSION_INFO;
#else
        m.attr("__version__") = "dev";
#endif
*/
#ifdef _WIN32
         m.attr("__version__") = "0.92"; // Change this number by hand
#elif  VERSION_INFO
        m.attr("__version__") = VERSION_INFO;
#else
        m.attr("__version__") = "dev";
#endif
}
