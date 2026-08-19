from pathlib import Path

import matplotlib.pyplot as plt
import torch


def main():
    size = 1024
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    coordinates = torch.arange(size, device=device, dtype=torch.int64)
    y, x = torch.meshgrid(coordinates, coordinates, indexing="ij")

    valid = x <= y
    binary_test = torch.bitwise_and(x, y - x) == 0
    selected = valid & binary_test

    pixel_x = 2 * x + (size - 1 - y)

    image = torch.zeros((size, 2 * size - 1), device=device, dtype=torch.uint8)
    image[y[selected], pixel_x[selected]] = 1

    selected_points = int(selected.sum().item())
    valid_points = int(valid.sum().item())
    selected_fraction = selected_points / valid_points

    output_path = Path(__file__).resolve().parents[1] / "outputs" / "sierpinski_binary.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    image_cpu = image.cpu().numpy()
    plt.imsave(output_path, image_cpu, cmap="gray", vmin=0, vmax=1)

    print(f"selected device: {device}")
    print(f"source grid size: {size}")
    print(f"output image shape: {tuple(image.shape)}")
    print(f"number of selected points: {selected_points}")
    print(f"fraction of valid triangular coordinates selected: {selected_fraction:.6f}")


if __name__ == "__main__":
    main()
