import sys
import math
import numpy as np
import numba

from numba import njit

PI = 3.14159265358979323
SOLAR_MASS = 4 * PI * PI
DAYS_PER_YEAR = 365.24

bodies_data = {
    'sun': ([0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            SOLAR_MASS),

    'jupiter': ([4.84143144246472090e+00,
                 -1.16032004402742839e+00,
                 -1.03622044471123109e-01],
                [1.66007664274403694e-03 * DAYS_PER_YEAR,
                 7.69901118419740425e-03 * DAYS_PER_YEAR,
                 -6.90460016972063023e-05 * DAYS_PER_YEAR],
                9.54791938424326609e-04 * SOLAR_MASS),

    'saturn': ([8.34336671824457987e+00,
                4.12479856412430479e+00,
                -4.03523417114321381e-01],
               [-2.76742510726862411e-03 * DAYS_PER_YEAR,
                4.99852801234917238e-03 * DAYS_PER_YEAR,
                2.30417297573763929e-05 * DAYS_PER_YEAR],
               2.85885980666130812e-04 * SOLAR_MASS),

    'uranus': ([1.28943695621391310e+01,
                -1.51111514016986312e+01,
                -2.23307578892655734e-01],
               [2.96460137564761618e-03 * DAYS_PER_YEAR,
                2.37847173959480950e-03 * DAYS_PER_YEAR,
                -2.96589568540237556e-05 * DAYS_PER_YEAR],
               4.36624404335156298e-05 * SOLAR_MASS),

    'neptune': ([1.53796971148509165e+01,
                 -2.59193146099879641e+01,
                 1.79258772950371181e-01],
                [2.68067772490389322e-03 * DAYS_PER_YEAR,
                 1.62824170038242295e-03 * DAYS_PER_YEAR,
                 -9.51592254519715870e-05 * DAYS_PER_YEAR],
                5.15138902046611451e-05 * SOLAR_MASS)
}

names = list(bodies_data.keys())
N_BODIES = len(names)

pos = np.zeros((N_BODIES, 3), dtype=np.float64)
vel = np.zeros((N_BODIES, 3), dtype=np.float64)
mass = np.zeros(N_BODIES, dtype=np.float64)

for i, name in enumerate(names):
    p, v, m = bodies_data[name]
    pos[i] = p
    vel[i] = v
    mass[i] = m


@njit(cache=False)
def advance(dt, pos, vel, mass):
    n = mass.shape[0]
    for i in range(n):
        for j in range(i+1, n):
            dx = pos[i, 0] - pos[j, 0]
            dy = pos[i, 1] - pos[j, 1]
            dz = pos[i, 2] - pos[j, 2]

            d_squared = dx*dx + dy*dy + dz*dz
            distance = math.sqrt(d_squared)
            mag = dt / (d_squared * distance)

            m2_mag = mass[j] * mag
            vel[i, 0] -= dx * m2_mag
            vel[i, 1] -= dy * m2_mag
            vel[i, 2] -= dz * m2_mag

            m1_mag = mass[i] * mag
            vel[j, 0] += dx * m1_mag
            vel[j, 1] += dy * m1_mag
            vel[j, 2] += dz * m1_mag

    # Update positions
    for i in range(n):
        pos[i, 0] += dt * vel[i, 0]
        pos[i, 1] += dt * vel[i, 1]
        pos[i, 2] += dt * vel[i, 2]


@njit(cache=False)
def report_energy(pos, vel, mass):
    e = 0.0
    n = mass.shape[0]
    for i in range(n):
        vx, vy, vz = vel[i, 0], vel[i, 1], vel[i, 2]
        e += 0.5 * mass[i] * (vx*vx + vy*vy + vz*vz)
        for j in range(i+1, n):
            dx = pos[i, 0] - pos[j, 0]
            dy = pos[i, 1] - pos[j, 1]
            dz = pos[i, 2] - pos[j, 2]
            distance = math.sqrt(dx*dx + dy*dy + dz*dz)
            e -= (mass[i] * mass[j]) / distance
    return e


@njit(cache=False)
def offset_momentum(ref_idx, pos, vel, mass):
    px = 0.0
    py = 0.0
    pz = 0.0
    n = mass.shape[0]
    for i in range(n):
        px -= vel[i, 0] * mass[i]
        py -= vel[i, 1] * mass[i]
        pz -= vel[i, 2] * mass[i]
    vel[ref_idx, 0] = px / SOLAR_MASS
    vel[ref_idx, 1] = py / SOLAR_MASS
    vel[ref_idx, 2] = pz / SOLAR_MASS


def main(n, ref='sun'):
    ref_idx = names.index(ref)
    offset_momentum(ref_idx, pos, vel, mass)
    print(f"{report_energy(pos, vel, mass):.9f}")
    for _ in range(n):
        advance(0.01, pos, vel, mass)
    print(f"{report_energy(pos, vel, mass):.9f}")


if __name__ == '__main__':
    main(int(sys.argv[1]))
