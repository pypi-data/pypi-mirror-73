#!/usr/bin/env python3
# type: ignore
import sys

import setuptools

def main():
	if sys.version_info[:2] < (3, 7):
		raise SystemExit("glowworm requires at least Python 3.7.")
	setuptools.setup(
		name="glowworm",
		version="0.0.1",
		description="A super-simple Python ORM.",
		url="https://github.com/chrisgavin/glowworm/",
		packages=["glowworm"],
		python_requires=">=3.7",
		classifiers=[
			"Programming Language :: Python :: 3",
			"Programming Language :: Python :: 3.7",
			"Programming Language :: Python :: 3 :: Only",
		],
		install_requires=[
			"firebase-admin",
		],
		extras_require={
			"dev": [
				"flake8",
				"mypy",
				"pytest",
			],
		},
	)

if __name__ == "__main__":
	main()
