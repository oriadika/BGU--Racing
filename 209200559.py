import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
import open3d as o3d
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


def apply_pfa_filtering(lidar_data):
    """
    Filters LIDAR data based on the Probability of False Alarm (PFA).

    Parameters:
        lidar_data (pd.DataFrame): Input point cloud data.

    Returns:
        pd.DataFrame: Data filtered by the selected PFA threshold.
    """
    pfa_strict = 0.01
    pfa_moderate = 0.05
    pfa_allowing = 0.1

    logging.info("Select PFA filtering level:")
    logging.info("1 - Strict (PFA ≤ 0.01)")
    logging.info("2 - Moderate (PFA ≤ 0.05)")
    logging.info("3 - Allowing (PFA ≤ 0.1)")
    logging.info("4 - Custom (Enter your threshold)")

    try:
        choice = int(input("Enter your choice (1-4): "))
        if choice == 1:
            selected_pfa = pfa_strict
            logging.info("Strict filtering selected (PFA ≤ 0.01).")
        elif choice == 2:
            selected_pfa = pfa_moderate
            logging.info("Moderate filtering selected (PFA ≤ 0.05).")
        elif choice == 3:
            selected_pfa = pfa_allowing
            logging.info("Allowing filtering selected (PFA ≤ 0.1).")
        elif choice == 4:
            selected_pfa = float(input("Enter custom PFA threshold (0-1): "))
            if not 0 <= selected_pfa <= 1:
                raise ValueError
            logging.info(f"Custom PFA filtering selected (PFA ≤ {selected_pfa}).")
        else:
            logging.warning("Invalid choice. Defaulting to Moderate filtering.")
            selected_pfa = pfa_moderate
    except ValueError:
        logging.warning("Invalid input. Defaulting to Moderate filtering.")
        selected_pfa = pfa_moderate

    filtered_data = lidar_data[lidar_data['Probability of False Alarm'] <= selected_pfa].copy()
    return filtered_data


def remove_ground_points(lidar_data, ground_z_threshold=500):
    """
    Removes ground points from the point cloud based on a z-coordinate threshold.

    Parameters:
        lidar_data (pd.DataFrame): Input point cloud data.
        ground_z_threshold (float): Minimum z-value for non-ground points.

    Returns:
        pd.DataFrame: Data without ground points.
    """
    non_ground_data = lidar_data[lidar_data['z'] > ground_z_threshold].copy()
    return non_ground_data


def cluster_point_cloud(lidar_data, eps=500, min_samples=5):
    """
    Clusters the point cloud data using DBSCAN.

    Parameters:
        lidar_data (pd.DataFrame): Input point cloud data.
        eps (float): Maximum distance between points in a cluster.
        min_samples (int): Minimum number of points to form a cluster.

    Returns:
        pd.DataFrame: Data with cluster labels.
    """
    lidar_data = lidar_data.copy()
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    lidar_data.loc[:, 'cluster'] = dbscan.fit_predict(lidar_data[['x', 'y', 'z']].values)
    logging.info(f"Clusters formed (excluding noise): {lidar_data['cluster'].nunique() - 1}")
    return lidar_data


def identify_cones_in_clusters(lidar_data, x_thresh=1500, y_thresh=1500, z_thresh=500):
    """
    Identifies cone-like objects based on cluster geometry.

    Parameters:
        lidar_data (pd.DataFrame): Clustered point cloud data.
        x_thresh (float): Maximum x-range for cones.
        y_thresh (float): Maximum y-range for cones.
        z_thresh (float): Minimum z-range for cones.

    Returns:
        pd.DataFrame: Data with an 'is_cone' column indicating cones.
    """
    lidar_data = lidar_data.copy()
    lidar_data.loc[:, 'is_cone'] = False

    for cluster_id in lidar_data['cluster'].unique():
        if cluster_id == -1:
            continue

        cluster_points = lidar_data[lidar_data['cluster'] == cluster_id].copy()
        x_range = cluster_points['x'].max() - cluster_points['x'].min()
        y_range = cluster_points['y'].max() - cluster_points['y'].min()
        z_range = cluster_points['z'].max() - cluster_points['z'].min()

        if x_range < x_thresh and y_range < y_thresh and z_range > z_thresh:
            lidar_data.loc[lidar_data['cluster'] == cluster_id, 'is_cone'] = True
            logging.info(f"Cone-like cluster: ID={cluster_id}, x_range={x_range}, y_range={y_range}, z_range={z_range}")

    logging.info(f"Cones identified: {lidar_data['is_cone'].sum()}")
    return lidar_data


def visualize_point_cloud(lidar_data, title="3D Point Cloud with Clusters"):
    """
    Visualizes the clustered point cloud with cones highlighted.

    Parameters:
        lidar_data (pd.DataFrame): Clustered point cloud data.
        title (str): Plot title.
    """
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    unique_clusters = lidar_data['cluster'].unique()
    colors = plt.cm.rainbow(np.linspace(0, 1, len(unique_clusters)))

    for cluster_id, color in zip(unique_clusters, colors):
        cluster_data = lidar_data[lidar_data['cluster'] == cluster_id]
        cluster_color = 'red' if cluster_data['is_cone'].any() else color
        ax.scatter(cluster_data['x'], cluster_data['y'], cluster_data['z'],
                   s=5, alpha=0.6, c=[cluster_color], label=f"Cluster {cluster_id}")

    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    ax.set_zlabel("Z-axis")
    plt.title(title)
    plt.legend()
    plt.show()



def main():
    """
    Main function for the BGU Racing Team LIDAR data processor.
    """
    try:
        logging.info("Loading race track LIDAR data...\n")
        lidar_data = pd.read_csv('Docs/Frame_702_Refl_1.csv')
    except FileNotFoundError:
        logging.error("Error: Data file not found. Please check the file path.")
        return

    if lidar_data.isnull().any().any():
        logging.warning("Missing values detected in the data. Dropping missing rows.")
        lidar_data = lidar_data.dropna(subset=['x', 'y', 'z', 'Probability of False Alarm'])

    logging.info("Step 1: Filtering data based on PFA...\n")
    filtered_data = apply_pfa_filtering(lidar_data)

    logging.info("Step 2: Removing ground points...\n")
    non_ground_data = remove_ground_points(filtered_data)

    logging.info("Step 3: Clustering point cloud data...\n")
    clustered_data = cluster_point_cloud(non_ground_data, eps=700, min_samples=5)

    logging.info("Step 4: Identifying cone-like objects...\n")
    processed_data = identify_cones_in_clusters(clustered_data, x_thresh=1500, y_thresh=1500, z_thresh=500)

    logging.info("Step 5: Visualizing results...\n")
    visualize_point_cloud(processed_data)


    logging.info("### Point Cloud Processing Complete ###")


if __name__ == "__main__":
    main()
