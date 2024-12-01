LIDAR Point Cloud Processing
This project is developed for the Automation Team of the BGU Racing Team as part of the Ben-Gurion University Racing Hiring process
The code processes LIDAR point cloud data to identify cone-like objects on a race track, aiding in autonomous vehicle navigation.

Overview
The program automates the analysis of 3D LIDAR data to detect and visualize cones on the race track. The workflow includes:

1.PFA Filtering: Filters points based on the Probability of False Alarm to improve data quality.
2.Ground Removal: Eliminates ground points using a Z-coordinate threshold.
3.Clustering: Groups nearby points into clusters using the DBSCAN clustering algorithm.
4.Cone Identification: Identifies cone-like clusters based on geometric properties.
5.3D Visualization: Displays the processed data, highlighting detected cones.

The approach aims to streamline the identification of key objects from raw LIDAR data, making it easier to feed into downstream navigation algorithms.

Installation and Run Instructions
Prerequisites
Operating System: Windows 10/11 (used during development)
Python Version: Python 3.8 or later
Required Python Libraries
Install the necessary dependencies using pip:

bash
Copy code
pip install numpy pandas matplotlib scikit-learn
Step-by-Step Instructions
Clone the repository or download the project:

bash
Copy code
git clone https://github.com/your-repo/bgu-racing-lidar.git
cd bgu-racing-lidar
Place the LIDAR CSV file (Frame_702_Refl_1.csv or your own data) in the Docs folder. The CSV file must include these columns:

x: X-coordinate of the point
y: Y-coordinate of the point
z: Z-coordinate of the point
Probability of False Alarm: A numerical value between 0 and 1 for each point
Run the main script:

bash
Copy code
python main.py
Follow the on-screen prompts to select the PFA filtering level and proceed with processing.

Explanation of Work and Approach
Approach
The program processes LIDAR data step by step:

PFA Filtering:

Filters out points with a high Probability of False Alarm.
Provides user control over the threshold to accommodate varying data quality.
Ground Removal:

Removes ground points based on a Z-coordinate threshold (default is 500 mm).
This isolates relevant points above the ground level.
Clustering:

Uses the DBSCAN algorithm to group nearby points into clusters based on spatial proximity.
Parameters like eps (maximum distance between points) and min_samples (minimum points per cluster) are adjustable.
Cone Identification:

Checks the dimensions of each cluster to determine if it matches the expected geometry of a cone.
Clusters with smaller x and y ranges but taller z ranges are identified as cones.
Visualization:

Creates a 3D scatter plot to display clusters, highlighting detected cones in red.
Operating System Used
The development and testing were performed on Windows 11. The code is designed to be cross-platform and should work on macOS or Linux with minor adjustments.

Running Example
Run the program:
css
Copy code
python main.py
Sample Output in the Console:
arduino
Copy code
Loading race track LIDAR data...
Clusters formed (excluding noise): 12
Cone-like cluster: ID=3, x_range=800, y_range=900, z_range=1200
Cones identified: 5
3D Visualization:
The 3D scatter plot will display the clustered point cloud.
Cones will be highlighted in red for easy identification.