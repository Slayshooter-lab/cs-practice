import sys
from stats import read_valid, average_by_city, warmest_city


def main():
    lines = sys.stdin.read().splitlines()
    lines = [line for line in lines if line.strip()]
    records = read_valid(lines)

    print(len(records))
    print(len(lines) - len(records))

    if records:
        best_city = warmest_city(records)
        avg_dict = average_by_city(records)
        print(f"{avg_dict[best_city]:.1f}")


if __name__ == "__main__":
    main()