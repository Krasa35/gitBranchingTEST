# Robot Path Planning Repository

This repository contains Python scripts for a robot path planning system. The system involves generating random obstacles, visualizing the environment, and finding a path from a starting location to a destination using Rapidly-exploring Random Trees (RRT).

[Additional README](RTB_toolbox/lib/README.md) is inside RTB_toolbox/lib folder.

[AI classes project documentation](Resources/report.pdf) state of art and method used.

[Presentation](https://youtu.be/i9UH8Y38aEk) of working scripts.

![GIF of presentation](Resources/SI_Projekt.gif)

## Table of Contents

- [Files](#files)
    -   [00_generate_data.py](#00_generate_datapy)
    -   [10_findpath_rrt.py](#10_findpath_rrtpy)
    -   [99_visualize.py](#99_visualizepy)   
- [Dependencies](#dependencies)
-   [Usage](#usage)
-   [Future Improvements](#future-improvements)
-   [Tips for contributing](#tips-for-contributing)
-   [Acknowledgments](#acknowledgments)

## Files

### 00_generate_data.py

This script generates random obstacle data and saves it to a CSV file (`restricted_area.csv`). It uses the `lib.callbacks` module for utility functions.

### 10_findPath_RRT.py

This script implements the RRT algorithm to find a path through the generated environment. It visualizes the process and saves the final path to a CSV file (`points.csv`). The `lib.callbacks` module is used for setup and utility functions.
-   Green sphere - start
-   Blue sphere - destination
-   Red areas - restricted areas
-   black spheres - currently generated new point is being checked if is best if yes, black sphere stays if not another one is generated. Black spheres that were not deleted are the points written to csv file and these are points that are sent to robot to visualise move

### 99_visualize.py

This script reads the generated obstacle and path data from CSV files, visualizes the environment, and moves a simulated robot along the generated path. It also utilizes the `lib.callbacks` module for setup.

 For more detailed explanation go to [Additional README](RTB_toolbox/lib/README.md)

## Dependencies

- `pandas`
- `numpy`
- `roboticstoolbox`
- `pybullet`

Install dependencies using:

```bash
pip install pandas numpy==1.24.3 roboticstoolbox-python pybullet
```

## Usage

1. Run `01_generate_data.py` to generate random obstacle data.
2. Execute `02_findPath_RRT.py` to find a path using the RRT algorithm.
3. Finally, run `03_visualise.py` to visualize the environment and simulate robot movement along the generated path.

Make sure to customize the parameters and file paths in the scripts according to your requirements.

##  Future Improvements

Project generates space for future improvements in at least 5 possible directions:
- [ ]   Adding improvement to RRT algorithm so path can be found in unfavourable situations when euclidean norm is not the best - e.g. `Resources/wall.csv` for example
- [ ]  Adding conditions of generating start, stop,  restricted area objects so they will not be generated in collision with each other (keep in mind that robot is always in (0, 0, 0) point for now)
- [ ]  Adding orientation finding algorithm for moving the robot in the most efficient way or most purpose needed way - e.g. holding object at specific angle
- [ ] Implementing more advanced methods of path finding algorithms like RRT*, PRM, FMT*, SH-FMT* also Artificial Potential Field. 
- [ ] Implementing path finding algorithm for every joint - or different conception for omiting collisions with restricted area spaces with body of the robot

##  Tips for contributing

Files are named so every new method/improvement from Future Improvement section can be named in convention 

`1x_yyyy.py - RRT algorithm`

`2x_yyyy.py - RRT* algorithm`, so that 

-   x - algorithm ID
-   y - new version/improvement
## Acknowledgments

- Special thanks to the contributors of the `spatialgeometry` and `roboticstoolbox` modules.
-   Thanks to developers of chat GPT which generated simple functions and comments for `lib/callbacks` module