// The Computer Language Benchmarks Game
// https://salsa.debian.org/benchmarksgame-team/benchmarksgame/
//
// contributed by the Rust Project Developers
// contributed by TeXitoi
// Remove borrow checker hacks
//
// This code is adapted to be run as a Python module using PyO3



use pyo3::prelude::*;
use std::f64::consts::PI;

const SOLAR_MASS: f64 = 4.0 * PI * PI;
const YEAR: f64 = 365.24;
const N_BODIES: usize = 5;
const ADVANCE_DT: f64 = 0.01;

#[derive(Clone)]
struct Planet {
    x: f64,
    y: f64,
    z: f64,
    vx: f64,
    vy: f64,
    vz: f64,
    mass_ratio: f64,
    mass: f64,
    mass_half: f64,
}

macro_rules! planet {
    ($x:expr, $y:expr, $z:expr, $vx:expr, $vy:expr, $vz:expr, $mass_ratio:expr) => {{
        Planet {
            x: $x,
            y: $y,
            z: $z,
            vx: $vx,
            vy: $vy,
            vz: $vz,
            mass_ratio: $mass_ratio,
            mass: $mass_ratio * SOLAR_MASS,
            mass_half: $mass_ratio * SOLAR_MASS * 0.5,
        }
    }};
}

const BODIES: [Planet; N_BODIES] = [
    // Sun
    planet!(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0),
    // Jupiter
    planet!(
        4.8414314424647210e+00,
        -1.1603200440274283e+00,
        -1.0362204447112311e-01,
        1.6600766427440369e-03 * YEAR,
        7.6990111841974043e-03 * YEAR,
        -6.9046001697206302e-05 * YEAR,
        9.5479193842432660e-04
    ),
    // Saturn
    planet!(
        8.3433667182445799e+00,
        4.1247985641243048e+00,
        -4.0352341711432138e-01,
        -2.7674251072686241e-03 * YEAR,
        4.9985280123491724e-03 * YEAR,
        2.3041729757376393e-05 * YEAR,
        2.8588598066613081e-04
    ),
    // Uranus
    planet!(
        1.2894369562139131e+01,
        -1.5111151401698631e+01,
        -2.2330757889265573e-01,
        2.9646013756476162e-03 * YEAR,
        2.3784717395948095e-03 * YEAR,
        -2.9658956854023756e-05 * YEAR,
        4.3662440433515630e-05
    ),
    // Neptune
    planet!(
        1.5379697114850917e+01,
        -2.5919314609987964e+01,
        1.7925877295037118e-01,
        2.6806777249038932e-03 * YEAR,
        1.6282417003824229e-03 * YEAR,
        -9.5159225451971587e-05 * YEAR,
        5.1513890204661145e-05
    ),
];

fn offset_momentum(bodies: &mut [Planet; N_BODIES]) {
    let mut px = 0.0;
    let mut py = 0.0;
    let mut pz = 0.0;
    for bi in bodies.iter() {
        px -= bi.vx * bi.mass_ratio;
        py -= bi.vy * bi.mass_ratio;
        pz -= bi.vz * bi.mass_ratio;
    }
    let sun = &mut bodies[0];
    sun.vx = px;
    sun.vy = py;
    sun.vz = pz;
}

fn advance(bodies: &mut [Planet; N_BODIES], dt: f64) {
    for i in 0..(N_BODIES - 1) {
        let (bi_x, bi_y, bi_z, mut bi_vx, mut bi_vy, mut bi_vz, bi_mass) =
            (|p: &Planet| (p.x, p.y, p.z, p.vx, p.vy, p.vz, p.mass))(&bodies[i]);
        for j in (i + 1)..N_BODIES {
            let bj = &mut bodies[j];
            let dx = bi_x - bj.x;
            let dy = bi_y - bj.y;
            let dz = bi_z - bj.z;
            let distance_square = dx * dx + dy * dy + dz * dz;
            let mag = dt / (distance_square * distance_square.sqrt());

            let bj_mass_mag = bj.mass * mag;
            bi_vx -= dx * bj_mass_mag;
            bi_vy -= dy * bj_mass_mag;
            bi_vz -= dz * bj_mass_mag;

            let bi_mass_mag = bi_mass * mag;
            bj.vx += dx * bi_mass_mag;
            bj.vy += dy * bi_mass_mag;
            bj.vz += dz * bi_mass_mag;
        }
        let bi = &mut bodies[i];
        bi.vx = bi_vx;
        bi.vy = bi_vy;
        bi.vz = bi_vz;

        bi.x += bi_vx * dt;
        bi.y += bi_vy * dt;
        bi.z += bi_vz * dt;
    }
    let last = &mut bodies[N_BODIES - 1];
    last.x += last.vx * dt;
    last.y += last.vy * dt;
    last.z += last.vz * dt;
}

fn energy(bodies: &[Planet; N_BODIES]) -> f64 {
    let mut e = 0.0;
    let mut iter = bodies.iter();
    while let Some(bi) = iter.next() {
        e += (bi.vx * bi.vx + bi.vy * bi.vy + bi.vz * bi.vz) * bi.mass_half;
        for bj in iter.clone() {
            let dx = bi.x - bj.x;
            let dy = bi.y - bj.y;
            let dz = bi.z - bj.z;
            let dist = (dx * dx + dy * dy + dz * dz).sqrt();
            e -= bi.mass * bj.mass / dist;
        }
    }
    e
}

#[pyfunction]
fn run_nbody(n: i32){
    let mut bodies = BODIES;
    println!("Start of  Rust Code");
    offset_momentum(&mut bodies);
    println!("{:.9}", energy(&bodies));

    for _ in 0..n {
        advance(&mut bodies, ADVANCE_DT);
    }
    
    println!("{:.9}", energy(&bodies));
    println!("End of Rust Code");
}

#[pymodule]
fn rust_binding(m: &Bound<'_, PyModule>) -> PyResult<()> {

    m.add_function(wrap_pyfunction!(run_nbody, m)?)

}