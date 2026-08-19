from pathlib import Path
import sys

import matplotlib.pyplot as plt
import torch


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.sierpinski import generate_sierpinski_mask


def main():
    size = 1024
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    box_sizes = torch.tensor(
        [1, 2, 4, 8, 16, 32, 64, 128, 256, 512],
        device=device,
        dtype=torch.int64,
    )

    # Box counting uses the logical binary-address mask, not the centred PNG
    # raster, because the PNG adds visual spacing and shearing for display only.
    mask = generate_sierpinski_mask(size, device)

    occupied_counts = []
    for box_size in box_sizes:
        b = int(box_size.item())
        boxes = mask.reshape(size // b, b, size // b, b)
        occupied = boxes.any(dim=(1, 3))
        occupied_counts.append(occupied.sum())

    occupied_counts = torch.stack(occupied_counts).to(torch.float64)
    box_sizes_float = box_sizes.to(torch.float64)
    epsilon = box_sizes_float / size
    x_values = torch.log(1.0 / epsilon)
    y_values = torch.log(occupied_counts)

    x_mean = x_values.mean()
    y_mean = y_values.mean()
    slope = ((x_values - x_mean) * (y_values - y_mean)).sum() / (
        (x_values - x_mean) ** 2
    ).sum()
    intercept = y_mean - slope * x_mean

    fitted_y = slope * x_values + intercept
    theoretical_dimension = torch.log(
        torch.tensor(3.0, device=device, dtype=torch.float64)
    ) / torch.log(
        torch.tensor(2.0, device=device, dtype=torch.float64)
    )
    absolute_error = torch.abs(slope - theoretical_dimension)

    output_path = PROJECT_ROOT / "outputs" / "fractal_dimension.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"selected device: {device}")
    print(f"source grid size: {size}")
    print()
    print(f"{'box size':>8} {'epsilon':>12} {'occupied boxes':>16}")
    for b, eps, count in zip(box_sizes, epsilon, occupied_counts):
        print(f"{int(b.item()):8d} {float(eps.item()):12.6f} {int(count.item()):16d}")
    print()
    print(f"estimated box-counting dimension: {float(slope.item()):.6f}")
    print(f"theoretical dimension: {float(theoretical_dimension.item()):.6f}")
    print(f"absolute error: {float(absolute_error.item()):.6e}")

    x_cpu = x_values.cpu().numpy()
    y_cpu = y_values.cpu().numpy()
    fitted_cpu = fitted_y.cpu().numpy()

    plt.figure(figsize=(7, 5))
    plt.scatter(x_cpu, y_cpu, label="measured box counts")
    plt.plot(x_cpu, fitted_cpu, label=f"fit, dimension = {float(slope.item()):.6f}")
    plt.xlabel("log(1 / epsilon)")
    plt.ylabel("log(N)")
    plt.title("Box-Counting Dimension Analysis")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


if __name__ == "__main__":
    main()
