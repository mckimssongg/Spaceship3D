#include <pybind11/pybind11.h>
#include <cmath>

class Meteor {
public:
    Meteor(float x, float y, float z): x(x), y(y), z(z) {}

    void move(float dx, float dy, float dz) {
        x += dx;
        y += dy;
        z += dz;
    }

    float getX() const { return x; }
    float getY() const { return y; }
    float getZ() const { return z; }

private:
    float x, y, z;
};

class Spaceship {
public:
    Spaceship(float x, float y, float z): x(x), y(y), z(z) {}

    void move(float dx, float dy, float dz) {
        x += dx;
        y += dy;
        z += dz;
    }

    float getX() const { return x; }
    float getY() const { return y; }
    float getZ() const { return z; }

    bool collidesWithMeteor(const Meteor& meteor, float collisionDistance) const {
        float dx = std::abs(x - meteor.getX());
        float dy = std::abs(y - meteor.getY());
        return (dx < collisionDistance) && (dy < collisionDistance);
    }

private:
    float x, y, z;
};

namespace py = pybind11;

PYBIND11_MODULE(geometria, m) {
    py::class_<Spaceship>(m, "Spaceship")
        .def(py::init<float, float, float>())
        .def("move", &Spaceship::move)
        .def("getX", &Spaceship::getX)
        .def("getY", &Spaceship::getY)
        .def("getZ", &Spaceship::getZ)
        .def("collidesWithMeteor", &Spaceship::collidesWithMeteor);

    py::class_<Meteor>(m, "Meteor")
        .def(py::init<float, float, float>())
        .def("move", &Meteor::move)
        .def("getX", &Meteor::getX)
        .def("getY", &Meteor::getY)
        .def("getZ", &Meteor::getZ);
}
