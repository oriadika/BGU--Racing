LIDAR Point Cloud Processing
This project is developed for the Automation Team of the BGU Racing Team as part of the Ben-Gurion University Racing Hiring process
The code processes LIDAR point cloud data to identify cone-like objects on a race track, aiding in autonomous vehicle navigation.

Overview
This software processes 3D LIDAR data collected during race simulations. It performs the following tasks:

1.PFA Filtering: Filters data points based on the Probability of False Alarm.
2.Ground Removal: Removes ground points based on the Z-coordinate threshold.
3.Clustering: Groups nearby points into clusters using the DBSCAN algorithm.
4.Cone Identification: Detects cone-like clusters based on their geometric properties.
5.Visualization: Visualizes the 3D point cloud with cones highlighted.


Prerequisites
Before running the code, ensure you have the following installed:

Python 3.8 or later	
 Required Python packages:
 bash
 Copy code
  pip install numpy pandas matplotlib scikit-learn


How to Run
Clone the repository or copy the code to your local machine:

 bash
 Copy code
 git clone https://github.com/your-repo/bgu-racing-lidar.git
 cd bgu-racing-lidar
 Place your LIDAR data file in the Docs folder. The file should be in CSV format and contain the following columns:

x: X-coordinate of the point
y: Y-coordinate of the point
z: Z-coordinate of the point
Probability of False Alarm: False alarm probability for each point
Run the main script:

 bash
 Copy code
 python main.py
 Follow the on-screen prompts to select the PFA filtering level.


Expected Output
Console Logs:

Number of clusters formed.
Dimensions of identified cone-like clusters.
Total number of cones identified.
3D Visualization:

A 3D plot displaying the clustered point cloud, with cones highlighted in red.