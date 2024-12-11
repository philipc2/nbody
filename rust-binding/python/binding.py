import rust_binding
import sys


def main(n, ref="sun"):
    print("Python Before Rust Call")

    rust_binding.run_nbody(n)

    print("Python After Rust Call")


if __name__ == "__main__":
    main(int(sys.argv[1]))
