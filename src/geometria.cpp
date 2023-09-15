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

class Projectile {
public:
    Projectile(float x, float y) : x(x), y(y) {}

    void move(float dx, float dy) {
        x += dx;
        y += dy;
    }

    float getX() const { return x; }
    float getY() const { return y; }

private:
    float x, y;
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

    void addProjectile(float x, float y) {
        projectiles.push_back(std::unique_ptr<Projectile>(new Projectile(x, y)));
    }

    void moveProjectiles(float dx, float dy) {
        for (auto &projectile : projectiles) {
            projectile->move(dx, dy);
        }
    }

    bool projectileCollidesWithMeteor(float collisionDistance) {
        for (int i = meteors.size() - 1; i >= 0; --i) {
            for (int j = projectiles.size() - 1; j >= 0; --j) {
                float dx = std::abs(projectiles[j]->getX() - meteors[i]->getX());
                float dy = std::abs(projectiles[j]->getY() - meteors[i]->getY());
                if (dx < collisionDistance + meteors[i]->getSize() / 2 && dy < collisionDistance + meteors[i]->getSize() / 2) {
                    meteors.erase(meteors.begin() + i);
                    projectiles.erase(projectiles.begin() + j);
                    return true;
                }
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

    int getProjectileCount() const {
        return static_cast<int>(projectiles.size());
    }

    const Projectile& getProjectile(std::size_t index) const {
        if (index < projectiles.size()) {
            return *projectiles[index];
        } else {
            throw std::out_of_range("Invalid index");
        }
    }

    std::vector<int> syncMeteors() {
        std::vector<int> toRemove;
        for (std::size_t i = 0; i < meteors.size(); ++i) {  
            if (meteors[i]->getY() > 400) {
                toRemove.push_back(static_cast<int>(i)); 
            }
        }
        return toRemove;
    }

    std::vector<int> syncProjectiles() {
        std::vector<int> toRemove;
        for (std::size_t i = 0; i < projectiles.size(); ++i) {
            if (projectiles[i]->getY() < 0) {
                toRemove.push_back(static_cast<int>(i)); 
            }
        }
        return toRemove;
    }

    
private:
    std::vector<std::unique_ptr<Meteor>> meteors;
    std::vector<std::unique_ptr<Projectile>> projectiles;
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

    py::class_<Projectile>(m, "Projectile")
        .def(py::init<float, float>())
        .def("move", &Projectile::move)
        .def("getX", &Projectile::getX)
        .def("getY", &Projectile::getY);

    py::class_<Game>(m, "Game")
        .def(py::init<>())
        .def("addMeteor", &Game::addMeteor)
        .def("moveMeteors", &Game::moveMeteors)
        .def("destroyMeteor", &Game::destroyMeteor)
        .def("addProjectile", &Game::addProjectile)
        .def("moveProjectiles", &Game::moveProjectiles)
        .def("projectileCollidesWithMeteor", &Game::projectileCollidesWithMeteor)
        .def("getMeteorCount", &Game::getMeteorCount)
        .def("getMeteor", &Game::getMeteor)
        .def("getProjectileCount", &Game::getProjectileCount)
        .def("getProjectile", &Game::getProjectile)
        .def("syncMeteors", &Game::syncMeteors)
        .def("syncProjectiles", &Game::syncProjectiles);
}
