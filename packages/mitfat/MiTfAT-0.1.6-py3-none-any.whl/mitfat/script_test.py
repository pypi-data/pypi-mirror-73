#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 13:58:02 2020

@author: vbokharaie
"""

import click
@click.command()
@click.argument('filename', default='sample_info_file.txt')
@click.argument('data_folder', default='datasets')
def main(filename, data_folder):
    """
    Just brought the test script in here to use click to handle input args.

    """

    # %% flags
    if_plot_basics = False  # plot normalised time-series, or raw if you do not normalise the data
    if_plot_lin_reg = False  # plots of linearised siganls, separately for each time-degment.
    if_plot_raw = False  #  plot raw time-series

    if_cluster = True  # if cluster and then dave plots for [2, ..., 9] clusters.
    if_cluster_hiararchical = False  # if hierarchical cluster and then save.

    if_detrend = False  # if detrend and save

    # %% have a copy of the config file in your current working directory
    #   for future references
    # this config file includes info on what data to load and from where
    from mitfat.file_io import print_info
    print_info('sample_info_file.txt')

    # %% there is a info_file and sample dataset accompanying the code
    # the rest of this example file is based on that dataset
#    import mitfat
    from mitfat.file_io import read_data
    from pathlib import Path
    import pkg_resources
    info_file = pkg_resources.resource_filename('mitfat', filename)
    print('*****', info_file)
    DATA_PATH = pkg_resources.resource_filename('mitfat', data_folder)
    list_dataset = read_data(info_file)
    dataset1 = list_dataset[0]
    print(dataset1.description)
    print('Your script is in here: ', Path(__file__).resolve().parent)
    dir_save = Path(Path(__file__).resolve().parent, 'outputs')
    title_str = dataset1.experiment_name
    dir_save = Path(dir_save, title_str)

    dataset1.dir_save = dir_save
    print('******************')
    print('Outputs saved in:', dir_save)
    print('******************')
    dir_save.mkdir(exist_ok=True, parents=True)

    # dataset1.dir_save = Path(Path(__file__).resolve().parent, 'outputs')
    # plot voxel 441
    dataset1.plot_voxel(voxel_num=441)
    dataset1.plot_voxel(list_voxel_num=[441,442,443])
    # Basic plots
    if if_plot_basics:
       dataset1.plot_basics()

    if if_plot_lin_reg:
       dataset1.plot_basics('lin_reg')

    if if_plot_raw:
       dataset1.plot_basics('raw')

    if if_cluster:
        ###
        X_train = dataset1.data_normalised
        X_train_label = 'RAW_Normalised'  # just used in plot titles and folder names
        print('-----------------------------------')
        print('Clustering ', X_train_label)
        for num_clusters in [2, 3, 4, 5,]:
            print(num_clusters, 'clusters')
            cluster_labels, cluster_centroid = \
                dataset1.cluster(X_train, num_clusters)
            dataset1.save_clusters(X_train, X_train_label,
                                    cluster_labels, cluster_centroid)
            dataset1.plot_clusters(X_train, X_train_label,
                                    cluster_labels, cluster_centroid)
        ###
        X_train = dataset1.data_mean
        X_train_label = 'Mean_Normalised'
        print('-----------------------------------')
        print('Clustering ', X_train_label)
        for num_clusters in [3, 4, 5, 6,]:
            print(num_clusters, 'clusters')
            cluster_labels, cluster_centroid = \
                dataset1.cluster(X_train, num_clusters)
            dataset1.save_clusters(X_train, X_train_label,
                                    cluster_labels, cluster_centroid)
            dataset1.plot_clusters(X_train, X_train_label,
                                    cluster_labels, cluster_centroid)
        ###
        X_train = dataset1.line_reg_slopes
        X_train_label = 'Lin_regression_slopes_per_segments'
        print('-----------------------------------')
        print('Clustering ', X_train_label)
        for num_clusters in [5, 6, 7, 8,]:
            print(num_clusters, 'clusters')
            cluster_labels, cluster_centroid = \
                dataset1.cluster(X_train, num_clusters)
            dataset1.save_clusters(X_train, X_train_label,
                                    cluster_labels, cluster_centroid)
            dataset1.plot_clusters(X_train, X_train_label,
                                    cluster_labels,
                                    cluster_centroid, if_slopes=True)
        ###
        X_train = dataset1.mean_segments
        X_train_label = 'Mean_Segments'
        print('-----------------------------------')
        print('Clustering ', X_train_label)
        for num_clusters in [2, 3, 4, 5,]:
            print(num_clusters, 'clusters')
            cluster_labels, cluster_centroid = dataset1.cluster(X_train, num_clusters)
            dataset1.save_clusters(X_train, X_train_label,
                                    cluster_labels, cluster_centroid)
            dataset1.plot_clusters(X_train, X_train_label,
                                    cluster_labels, cluster_centroid)

    if if_cluster_hiararchical:
        signal = 'raw'
        dataset1.cluster_hierarchial(signal, if_save_plot=True)

    if if_detrend:
        dataset1.detrend()

# %% __main__
if __name__ == "__main__":
    main()
