import sys
import math
import numpy as np

PI = 3.14159265358979323
SOLAR_MASS = 4 * PI * PI
DAYS_PER_YEAR = 365.24

# Original body definitions
bodies_data = {
    "sun": (
        np.array([0.0, 0.0, 0.0]),
        np.array([0.0, 0.0, 0.0]),
        SOLAR_MASS,
    ),
    "jupiter": (
        np.array([4.84143144246472090e00, -1.16032004402742839e00, -1.03622044471123109e-01]),
        np.array([1.66007664274403694e-03 * DAYS_PER_YEAR,
                  7.69901118419740425e-03 * DAYS_PER_YEAR,
                  -6.90460016972063023e-05 * DAYS_PER_YEAR]),
        9.54791938424326609e-04 * SOLAR_MASS,
    ),
    "saturn": (
        np.array([8.34336671824457987e00, 4.12479856412430479e00, -4.03523417114321381e-01]),
        np.array([-2.76742510726862411e-03 * DAYS_PER_YEAR,
                  4.99852801234917238e-03 * DAYS_PER_YEAR,
                  2.30417297573763929e-05 * DAYS_PER_YEAR]),
        2.85885980666130812e-04 * SOLAR_MASS,
    ),
    "uranus": (
        np.array([1.28943695621391310e01, -1.51111514016986312e01, -2.23307578892655734e-01]),
        np.array([2.96460137564761618e-03 * DAYS_PER_YEAR,
                  2.37847173959480950e-03 * DAYS_PER_YEAR,
                  -2.96589568540237556e-05 * DAYS_PER_YEAR]),
        4.36624404335156298e-05 * SOLAR_MASS,
    ),
    "neptune": (
        np.array([1.53796971148509165e01, -2.59193146099879641e01, 1.79258772950371181e-01]),
        np.array([2.68067772490389322e-03 * DAYS_PER_YEAR,
                  1.62824170038242295e-03 * DAYS_PER_YEAR,
                  -9.51592254519715870e-05 * DAYS_PER_YEAR]),
        5.15138902046611451e-05 * SOLAR_MASS,
    ),
}

# Extract arrays of positions, velocities, and masses
names = list(bodies_data.keys())
N_BODIES = len(names)

positions = np.array([bodies_data[name][0] for name in names], dtype=np.float64)  # shape (N,3)
velocities = np.array([bodies_data[name][1] for name in names], dtype=np.float64) # shape (N,3)
masses = np.array([bodies_data[name][2] for name in names], dtype=np.float64)      # shape (N,)

def advance(dt, positions, velocities, masses):
    # Compute all pairwise differences
    i_idx, j_idx = np.triu_indices(N_BODIES, k=1)  # pairs (i<j)
    diff = positions[i_idx] - positions[j_idx]  # (M, 3), M = N*(N-1)/2

    dist_sq = np.sum(diff**2, axis=1)
    dist = np.sqrt(dist_sq)

    # Magnitude of the force component
    mag = dt / (dist_sq * dist)

    # Update velocities
    # Each pair affects both i and j
    mass_j = masses[j_idx]
    mass_i = masses[i_idx]

    # Velocity changes for i due to j
    vel_change_i = (diff * (mass_j * mag)[:, None])
    # Velocity changes for j due to i (note sign inversion of diff)
    vel_change_j = (-diff * (mass_i * mag)[:, None])

    # Accumulate changes:
    # We add changes to velocities in a summed manner using np.add.at because multiple pairs involve the same body.
    np.add.at(velocities, i_idx, -vel_change_i)
    np.add.at(velocities, j_idx, -vel_change_j)

    # Advance positions
    positions += dt * velocities


def report_energy(positions, velocities, masses):
    # Kinetic energy
    e = 0.5 * np.sum(masses * np.sum(velocities**2, axis=1))
    
    # Potential energy
    i_idx, j_idx = np.triu_indices(N_BODIES, k=1)
    diff = positions[i_idx] - positions[j_idx]
    dist = np.sqrt(np.sum(diff**2, axis=1))
    e -= np.sum((masses[i_idx] * masses[j_idx]) / dist)
    
    print(f"{e:.9f}")


def offset_momentum(ref_name, positions, velocities, masses):
    # Find reference body index
    ref_idx = names.index(ref_name)
    
    # Total momentum
    px = np.sum(velocities[:,0] * masses)
    py = np.sum(velocities[:,1] * masses)
    pz = np.sum(velocities[:,2] * masses)
    
    # Adjust reference velocity to offset total momentum
    velocities[ref_idx,0] = -px / SOLAR_MASS
    velocities[ref_idx,1] = -py / SOLAR_MASS
    velocities[ref_idx,2] = -pz / SOLAR_MASS


def main(n, ref="sun"):
    offset_momentum(ref, positions, velocities, masses)
    report_energy(positions, velocities, masses)
    for _ in range(n):
        advance(0.01, positions, velocities, masses)
    report_energy(positions, velocities, masses)


if __name__ == "__main__":
    main(int(sys.argv[1]))
