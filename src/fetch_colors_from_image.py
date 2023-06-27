from math import sqrt
import random
import sys
import colorsys
import requests
import io

try:
    import Image
except ImportError:
    from PIL import Image

class Point:
    def __init__(self, coordinates):
        self.coordinates = coordinates

class Cluster:
    def __init__(self, center, points):
        self.center = center
        self.points = points

class KMeans:
    def __init__(self, k_clusters, min_difference = 1):
        self.k_clusters = k_clusters
        self.min_difference = min_difference

    def calculating_euclidean_distance(self, a, b):
        # Calculating Euclidean distance between two rgb points
        addition = 0
        for i in range(len(a.coordinates)):
            addition += (a.coordinates[i] - b.coordinates[i]) ** 2
        return sqrt(addition)

    def calculate_center(self, rgb_points):
        # Calculating the new center rgb point and using that as reference for further processing
        values = [0.0 for i in range(len(rgb_points[0].coordinates))]
        for p in rgb_points:
            for i in range(len(p.coordinates)):
                values[i] += p.coordinates[i]
            coords = []
            for v in values:
                coords.append(v / len(rgb_points))
        return Point(coords)

    def populating_k_clusters_list_with_rgbpoints_based_on_distance(self, clusters, rgb_points):
        # Clusters: List of k lists having randomly selected rgb points from rgb_points list
        # rgb_points: List of rgb points
        # Depending on the euclidean distances between rgb point and randomly selected rgb point, "clusters_list" is populated and returned with those specific rgb points accordingly
        clusters_list = [[] for i in range(self.k_clusters)]
        for rgb_point in rgb_points:
            min_distance = float('inf')
            for i in range(self.k_clusters):
                temp_distance = self.calculating_euclidean_distance(rgb_point, clusters[i].center)
                if temp_distance < min_distance:
                    min_distance = temp_distance
                    index = i
            clusters_list[index].append(rgb_point)
        return clusters_list

    def process(self, rgb_points):
        # Initiliazing clusters list with k random points taken from rgb_points list parameter
        clusters = []
        for rgb_point in random.sample(rgb_points, self.k_clusters):
            clusters.append(Cluster(center=rgb_point, points=[rgb_point]))

        # Repeat the following process until the calculated difference becomes less than the constant defined difference
        while True:
            # Populating the clusters list with rgb points
            clusters_list = self.populating_k_clusters_list_with_rgbpoints_based_on_distance(clusters, rgb_points)
            difference = 0
            for i in range(self.k_clusters):
                if len(clusters_list[i]) == 0:
                    continue
                old_cluster = clusters[i]   # Storing the current selected cluster as an old cluster
                center = self.calculate_center(clusters_list[i])    # Calculating center rgb point by taking mean of all the rgb points within a cluster out of total k clusters
                new_cluster = Cluster(center, clusters_list[i])     # Using this center rgb point as the new point of calculation, instead of the initially selected random rgb value, thereby using this as the new cluster
                clusters[i] = new_cluster   # Using the new cluster as the current cluster
                difference = max(difference, self.calculating_euclidean_distance(old_cluster.center, new_cluster.center))
            if difference < self.min_difference:
                break
        return clusters

def create_and_fetch_rgb_points(image_path):
    # Configuring Image
    api_key = '9498e7d162a2714ada74b4257dce08a4dbafb36e'
    headers = {'Authorization': f'Token {api_key}'}
    response = requests.get(image_path, headers=headers)
    if response.status_code == 200:
        image_file = io.BytesIO(response.content)
        image = Image.open(image_file)
        image.thumbnail((200, 400))
        image = image.convert("RGB")
        width, height = image.size
        # Populating & Returning "rgb_points" list which has RGB tuples present depending on each tuple's count, each of which is of type "Point" (r_value, g_value, b_value)
        rgb_points = []
        for count, rgb_value in image.getcolors(width * height):
            for i in range(count):
                rgb_points.append(Point(rgb_value))
        image.close()
        return rgb_points
    else:
        print("Failed to retrieve image. Error:", response.text)

def rgb_to_hex(rgb):
    return '#%s' % ''.join(('%02x' % p for p in rgb))

def fetch_k_colors(image_path, k_colors):
    rgb_points = create_and_fetch_rgb_points(image_path)    # Fetching RGB values from the image
    kmeans_object = KMeans(k_clusters = k_colors)    # Initiliazing KMeans Object with value for k_clusters
    clusters = kmeans_object.process(rgb_points)     # Invoking process function with rgb_points as input
    clusters.sort(key=lambda c: len(c.points), reverse = True)
    rgbs = [map(int, c.center.coordinates) for c in clusters]
    return list(map(rgb_to_hex, rgbs))

def sort_colors_by_lightness(color):
    rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
    hsl = colorsys.rgb_to_hls(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255)
    return hsl[1]

def main():
    k_colors = 4
    username = 'MohitKambli'
    filename = sys.argv[1]
    remote_path = f'/home/{username}/mysite/Images/{filename}'  # Replace with the remote path where you want to upload the file
    url = f'https://www.pythonanywhere.com/api/v0/user/{username}/files/path{remote_path}'
    colors = fetch_k_colors(url, k_colors)
    sorted_colors = sorted(colors, key=sort_colors_by_lightness)
    print(sorted_colors)
    return sorted_colors

main()