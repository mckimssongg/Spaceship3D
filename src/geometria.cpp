#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <cmath>
#include <vector>
#include <memory>

class Meteor {
public:
    Meteor(float x, float y, float z, float size) : x(x), y(y), z(z), size(size) {}

    void move(float dx, float dy, float dz) {
        x += dx;
        y += dy;
        z += dz;
    }

    float getX() const { return x; }
    float getY() const { return y; }
    float getZ() const { return z; }
    float getSize() const { return size; }

private:
    float x, y, z, size;
};

class Spaceship {
public:
    Spaceship(float x, float y, float z) : x(x), y(y), z(z) {}

    void move(float dx, float dy, float dz) {
        x += dx;
        y += dy;
        z += dz;
    }

    float getX() const { return x; }
    float getY() const { return y; }
    float getZ() const { return z; }

    bool collidesWithMeteor(const Meteor &meteor, float collisionDistance) const {
        float dx = std::abs(x - meteor.getX());
        float dy = std::abs(y - meteor.getY());
        return (dx < collisionDistance + meteor.getSize() / 2) && (dy < collisionDistance + meteor.getSize() / 2);
    }

private:
    float x, y, z;
};

namespace py = pybind11;

class Game {
public:
    Game() {}

    void addMeteor(float x, float y, float z, float size) {
        meteors.push_back(std::unique_ptr<Meteor>(new Meteor(x, y, z, size)));
    }

    void moveMeteors(float dx, float dy, float dz) {
        for (auto &meteor : meteors) {
            meteor->move(dx, dy, dz);
        }
    }

    void destroyMeteor(std::size_t index) {
        if (index < meteors.size()) {
            meteors.erase(meteors.begin() + index);
        }
    }

    bool spaceshipCollidesWithMeteor(const Spaceship &spaceship, float collisionDistance) {
        for (int i = meteors.size() - 1; i >= 0; i--) {
            if (spaceship.collidesWithMeteor(*meteors[i], collisionDistance)) {
                destroyMeteor(i);
                return true;
            }
        }
        return false;
    }
    

    int getMeteorCount() const {
        return static_cast<int>(meteors.size());
    }

    const Meteor& getMeteor(std::size_t index) const {
        if (index < meteors.size()) {
            return *meteors[index];
        } else {
            throw std::out_of_range("Invalid index");
        }
    }

private:
    std::vector<std::unique_ptr<Meteor>> meteors;
};

PYBIND11_MODULE(geometria, m) {
    py::class_<Spaceship>(m, "Spaceship")
        .def(py::init<float, float, float>())
        .def("move", &Spaceship::move)
        .def("getX", &Spaceship::getX)
        .def("getY", &Spaceship::getY)
        .def("getZ", &Spaceship::getZ)
        .def("collidesWithMeteor", &Spaceship::collidesWithMeteor);

    py::class_<Meteor>(m, "Meteor")
        .def(py::init<float, float, float, float>())
        .def("move", &Meteor::move)
        .def("getX", &Meteor::getX)
        .def("getY", &Meteor::getY)
        .def("getZ", &Meteor::getZ)
        .def("getSize", &Meteor::getSize);

    py::class_<Game>(m, "Game")
        .def(py::init<>())
        .def("addMeteor", &Game::addMeteor)
        .def("moveMeteors", &Game::moveMeteors)
        .def("destroyMeteor", &Game::destroyMeteor)
        .def("spaceshipCollidesWithMeteor", &Game::spaceshipCollidesWithMeteor)
        .def("getMeteorCount", &Game::getMeteorCount)
        .def("getMeteor", &Game::getMeteor);
}
