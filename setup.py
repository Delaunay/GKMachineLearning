from setuptools import setup
import subprocess
import os
import shutil


def cook_environment():
    ueeditor = os.environ.get("UnrealEditor", None)
    if ueeditor is None:
        print("Cannot cook game")
        return

    # FIXME: find the root project
    platform = "Linux"
    args = [
        ueeditor,
        "Cartpole.uproject",
        "-run=cook",
        f"-targetplatform={platform}",
    ]
    subprocess.call(args)
    shutil.move("Saved/Sandboxes/Cooked-Linux", "Source/python/gkml/Cooked")


def find_package_data(root="Source/python/gkml/Cooked", data=None):
    first = False
    if data is None:
        data = []
        first = True

    for root, dirs, files in os.walk(root):
        for dir in dirs:
            find_package_data(os.path.join(root, dir), data)

        for file in files:
            if "Saved" in root:
                continue

            data.append(os.path.join(root, file))

    if first:
        data = list(set(data))
        rm = "Source/python/gkml/"
        for i in range(len(data)):
            data[i] = data[i][len(rm) :]

    return data


if __name__ == "__main__":

    setup(
        name="gkml",
        description="Gamekit Machine Learning utilities",
        license="BSD-3-Clause",
        author="Pierre Delaunay",
        author_email="pierre@delaunay.io",
        url="https://github.com/Delaunay/GKMachineLearning",
        packages=["gkml"],
        package_dir={"": "Source/python"},
        package_data={"gkml": find_package_data()},
        entry_points={
            "console_scripts": [
                "cartpole-train = gkml.train:main",
            ],
        },
    )
