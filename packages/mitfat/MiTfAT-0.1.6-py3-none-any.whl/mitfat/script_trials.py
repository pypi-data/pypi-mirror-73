import click
@click.command()
@click.argument('filename', default='info_file_UN1_26.txt')
@click.argument('data_folder', default='datasets_trials')

def main(filename, data_folder):
    from mitfat.file_io import read_data
    import os
    import numpy as np
    from pathlib import Path
    import matplotlib.pyplot as plt

    from mitfat.bplots import plot_trial_cluster_seq, plot_line
    #%% look at the sample_info_file.txt for info on how to setup the info.file
    # comment the next for lines if you do not want to use sample dataset
    dir_path = os.path.dirname(os.path.realpath(__file__))
    info_file_name = filename
    info_file_name = Path(dir_path, info_file_name)
    print(info_file_name)

    #%% read the data based on the info in info_file_name
    ###########################################################################
    list_fmri_objects = read_data(info_file_name)  # load all trials into a list of datasets
    ###########################################################################
    # now read dataset as if no trials exists, just to find the voxels with maximum overall amplitude
    with open(info_file_name) as f:
        content = f.readlines()
    content = [x.strip() for x in content]

    list_file_new = []
    for line in content:
        if not line.startswith('FIRST_TRIAL_TIME') and \
            not line.startswith('TRIAL_LENGTH') and \
            not line.startswith('TIME_STEP'):
                list_file_new.append(line)
    info_file_name_no_trials = Path(info_file_name.parent, info_file_name.stem + '_no_trials.txt')
    with open(info_file_name_no_trials, 'w') as f:
        for item in list_file_new:
            f.write("%s\n" % item)
    list_fmri_overall = read_data(info_file_name_no_trials)
    dataset_overall = list_fmri_overall[0]
    X_train = np.mean(dataset_overall.data, axis=0)
    Ntop = 20
    indices_Ntop = X_train.argsort()[-Ntop:][::-1]
    filename = info_file_name_no_trials.stem + '_top_'+str(Ntop)+'_voxels_indices'
    np.save(filename, indices_Ntop)
    ###########################################################################


    #%% choosing top N voxels (in terms of mean value of signal)
    for Nt in np.arange(10)+1:
        print('------------>', Nt)
        list_my_data_mean = []
        list_my_data_mean_normalised = []


        for idx in np.arange(len(list_fmri_objects)-Nt+1):


            if Nt == 1:
                dataset = list_fmri_objects[idx]
                my_data = dataset.data[:, indices_Ntop]
            elif Nt == 2:
                dataset = list_fmri_objects[idx]
                my_data1 = dataset.data[:, indices_Ntop]
                dataset = list_fmri_objects[idx+1]
                my_data2 = dataset.data[:, indices_Ntop]
                my_data = np.concatenate((my_data1, my_data2))
            elif Nt == 3:
                dataset = list_fmri_objects[idx]
                my_data1 = dataset.data[:, indices_Ntop]
                dataset = list_fmri_objects[idx+1]
                my_data2 = dataset.data[:, indices_Ntop]
                dataset = list_fmri_objects[idx+2]
                my_data3 = dataset.data[:, indices_Ntop]
                my_data = np.concatenate((my_data1, my_data2, my_data3))
            else:
                list_temp = []
                for cc4 in np.arange(Nt):
                    dataset = list_fmri_objects[idx+cc4]
                    my_data_temp = dataset.data[:, indices_Ntop]
                    list_temp.append(my_data_temp)
                #
                my_data = list_temp[0]
                for cc3 in np.arange(len(list_temp)-1):
                    my_data = np.concatenate((my_data, list_temp[cc3+1]))

            dir_save = Path(Path(__file__).resolve().parent, 'outputs')
            title_str = dataset.experiment_name
            dir_save = Path(dir_save, title_str, 'clusters_'+str(Nt).zfill(2)+'_trials')

            dataset.dir_save = dir_save
            dir_save.mkdir(exist_ok=True, parents=True)

            my_data_mean = np.mean(my_data, axis=1)
            list_my_data_mean.append(my_data_mean)

            my_data_mean_normalised = my_data_mean/np.mean(my_data_mean)
            list_my_data_mean_normalised.append(my_data_mean_normalised)

        array_data_mean = np.array(list_my_data_mean).T
        array_data_mean_normalised = np.array(list_my_data_mean_normalised).T
#
        #%% plot clustering of the overall data
        list_cluster_NO = [2,3,4,5]
        for cluster_NO in list_cluster_NO:
            from mitfat.clustering import cluster_raw

            cluster_labels_trials, cluster_centroid_trials = cluster_raw(array_data_mean,
                                                                         cluster_NO)
            cluster_labels_trials_norm, cluster_centroid_trials_norm = cluster_raw(
                array_data_mean_normalised, cluster_NO)


            #%% plot

            my_title = title_str + '_normalised_clusters_'+str(cluster_NO)
            plot_trial_cluster_seq(cluster_centroid_trials_norm.T,
                                   cluster_labels_trials_norm,
                                   my_title, dir_save, Cluster_num=cluster_NO)

            my_title = title_str + '_raw_clsuters_'+str(cluster_NO)
            plot_trial_cluster_seq(cluster_centroid_trials.T,
                                   cluster_labels_trials,
                                   my_title, dir_save, Cluster_num=cluster_NO)

        #%% plot mean of all trials
        mean_all_trials_raw = np.mean(list_my_data_mean, axis=0)
        mean_all_trials_normalised = np.mean(list_my_data_mean_normalised, axis=0)
        fig, ax = plot_line(mean_all_trials_raw,
                            np.arange(mean_all_trials_raw.size)+1,
                            title_str='Mean of top ' + str(Ntop) + ' voxels',
                            color='green',)
        filesave = Path(dir_save, '01_OVERALL_MEAN_RAW.png')
        fig.savefig(filesave)
        fig, ax = plot_line(mean_all_trials_normalised,
                            np.arange(mean_all_trials_raw.size)+1,
                            title_str='Mean of top ' + str(Ntop) + ' voxels',
                            color='blue',)
        filesave = Path(dir_save, '02_OVERALL_MEAN_NORMALISED.png')
        fig.savefig(filesave)
    plt.close('all')

# %% __main__
if __name__ == "__main__":

    main()