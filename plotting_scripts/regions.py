import os
import copy
import pickle
import argparse
import skimage.io
import numpy as np
import pandas as pd
from scipy.stats import ttest_ind_from_stats
import adv

 
class Atlas:

    # Class variables shared by all instances
    files = {
        "distance"    : "/media/athena-admin/FastSSD1/Athena/atlas/ABA_25um_distance_to_surface.tif",
        "annotations" : "/media/athena-admin/FastSSD1/Athena/atlas/ABA_25um_annotation.tif",
        "table"       : "atlas.tab"
    }


    def pprint(self, s):
        print("(atlas) %s" % s)


    def get_atlas(self, path):
        a = skimage.io.imread(path, plugin='tifffile').T
        return a


    def get_cropped_atlas(self, path, sample3D):
        """
        Assumes that sample is cropped in the Z-direction
        """
        a_ = self.get_atlas(path)
        a = np.zeros(np.shape(sample3D))
        a[:,:,:] = a_[:, :, 0:np.shape(sample3D)[2]]
        return a


    def map_fine_to_coarse_levels(self):

        fw = open("regions_level1.dat", 'w')
        fw.write("%15s %15s %15s\n" % ("Original ID", "Coarse-level ID", "Coarse-level name"))

        for i in range(len(self.regions["fine_level"])):

            p = copy.deepcopy(self.regions["parents"][i])
            l = copy.deepcopy(self.regions["fine_level"][i])

            self.regions["fine2coarse_level"][i] = copy.deepcopy(l)
            self.regions["fine2coarse_names"][i] = self.regions["fine_names"][i]

            self.pprint("\n")
            self.pprint("New item:")
            self.pprint("l: %d  p: %d" % (l, p))

            while (p != -1) and (p != 997):

                idx_ = np.where( self.regions["fine_level"]==p )
                assert(len(idx_)==1)
                idx = idx_[0][0]

                p_new = copy.deepcopy( self.regions["parents"][idx] )

                if p_new == 997:
                    p = p_new
                else:
                    l = copy.deepcopy(p)
                    p = p_new

                self.pprint("l: %d  p: %d" % (l, p))

                idx_ = np.where( self.regions["fine_level"] == l )
                assert(len(idx_)==1)
                idx = idx_[0][0]
                self.regions["fine2coarse_level"][i] = copy.deepcopy(l)
                self.regions["fine2coarse_names"][i] = copy.deepcopy(self.regions["fine_names"][idx])


            self.pprint("finished while loop. grouped[i]=%d" % self.regions["fine2coarse_level"][i])

            fw.write("%15d %15d %s\n" % (self.regions["fine_level"][i], self.regions["fine2coarse_level"][i], self.regions["fine2coarse_names"][i]))
        fw.close()


    # Instance variables unique to each instance
    # self.x
    def __init__(self, sample3D):
        """
            Members:
            * self.files
            * self.regions -- dict
            * self.atlas_annotations -- cropped atlas with annotated region IDs
            * self.Nfine -- number of unique fine regions
            * self.Ncoarse -- number of unique coarse regions
            * self.pickle -- path to backup pickle file
            * self.pickle_maps - path to backup file for fine->coarse mapping
        """

        self.pprint("Instantiating atlas...")

        self.regions = {
            "parents"           : [None],
            "fine_level"        : [None],
            "fine_volumes"      : [None],
            "fine2coarse_level" : [None],
            "fine2coarse_names" : [None],
            "unique_coarse_level" : [None], 
            "unique_coarse_vols" : [None],
            "unique_coarse_names" : [None] 
        }

        self.pickle = "atlas_info.pickle"
        self.pickle_maps = "atlas_fine2coarse_map.pickle"

        table = pd.read_csv(self.files["table"], header=None, sep='\t', lineterminator='\n')

        self.Nfine = len( table.loc[:,0] )

        self.regions["parents"]         = copy.deepcopy(table.loc[:,1])
        self.regions["fine_level"]      = copy.deepcopy(table.loc[:,0])
        self.regions["fine_names"]      = copy.deepcopy(table.loc[:,3])
        self.regions["fine_volumes"]      = np.zeros( self.Nfine )
        self.regions["fine2coarse_level"] = np.zeros( self.Nfine )
        self.regions["fine2coarse_names"] =  [None] * self.Nfine

        self.atlas_annotations = self.get_cropped_atlas(self.files["annotations"], sample3D)

        # Compute volume of fine regions
        if os.path.exists(self.pickle):
            with open(self.pickle, 'rb') as handle:
                backup = pickle.load(handle)
                self.regions = copy.deepcopy(backup)
            self.pprint("Loaded pickle.")

        else:
            self.pprint("Computing volume per region...")

            for i,ID in enumerate(self.regions["fine_level"]):
                idx = np.where(self.atlas_annotations==ID)
                self.regions["fine_volumes"][i] = np.shape(idx)[1]

            with open(self.pickle, 'wb') as handle:
                pickle.dump(self.regions, handle, protocol=pickle.HIGHEST_PROTOCOL)
            self.pprint("Dumped pickle.")


        # Find mapping of fine -> coarse regions
        if os.path.exists(self.pickle_maps):
            with open(self.pickle_maps, 'rb') as handle:
                backup = pickle.load(handle)
                self.regions["fine2coarse_level"][:] = backup["fine2coarse_level"][:]
                self.regions["fine2coarse_names"][:] = backup["fine2coarse_names"][:]
            self.pprint("Loaded pickle_maps.")

        else:
            self.pprint("Computing fine-to-coarse region mapping...")
            self.map_fine_to_coarse_levels()

            with open(self.pickle_maps, 'wb') as handle:
                pickle.dump(self.regions, handle, protocol=pickle.HIGHEST_PROTOCOL)
            self.pprint("Dumped pickle_maps.")



        # First selection of coarse regions        
        self.Ncoarse = len( np.unique(self.regions["fine2coarse_level"]) )
        self.regions["unique_coarse_level"] = np.unique(self.regions["fine2coarse_level"])

        # Volume of coarse regions
        self.regions["unique_coarse_vols"] = np.zeros( self.Ncoarse )
        self.regions["unique_coarse_names"] = [None] * self.Ncoarse
        for i,ID in enumerate(self.regions['unique_coarse_level']):
            idx = np.where( self.regions["fine2coarse_level"] == ID )
            self.regions["unique_coarse_vols"][i] = np.sum( self.regions["fine_volumes"][idx] )
            self.regions["unique_coarse_names"][i] = self.regions["fine2coarse_names"][idx[0][0]]


        # Ignore regions with 0 volume
        idx  = self.regions["unique_coarse_vols"]>0
        tmpv = self.regions["unique_coarse_vols"][idx]
        tmpl = self.regions["unique_coarse_level"][idx]
        self.Ncoarse = len(tmpv)
        self.regions["unique_coarse_vols"] = np.zeros( self.Ncoarse )
        self.regions["unique_coarse_vols"][:] = copy.deepcopy(tmpv[:])
        self.regions["unique_coarse_level"] = np.zeros( self.Ncoarse )
        self.regions["unique_coarse_level"][:] = copy.deepcopy(tmpl[:])

        tmpn = copy.deepcopy(self.regions["unique_coarse_names"])
        self.regions["unique_coarse_names"] = [None] * self.Ncoarse
        k = 0
        for i,ID in enumerate(idx):
            if ID == True:
                self.regions["unique_coarse_names"][k] = tmpn[i]
                k = k+1

        self.pprint("Nfine=%d  Ncoarse=%d" % (self.Nfine, self.Ncoarse))



class Cohort:

    """
    An instance would be a list of samples
      of the same group.

        self.files
        self.vol
        self.mean
        self.std
        self.densities
    """

    def pprint(self, s):
        print("(cohort) %s" % s)


    def __init__(self, files, atlas):

        Nfine    = atlas.Nfine
        Ncoarse  = atlas.Ncoarse
        Nsamples = len(files)

        self.files= [None] * Nsamples
        """
             vol, mean, std are over the unique COARSE regions
        """
        self.vol  = np.zeros( (Ncoarse, Nsamples) )
        self.densities = np.zeros( (Ncoarse, Nsamples) )
        self.mean = np.zeros( Ncoarse )
        self.std  = np.zeros( Ncoarse )

        for i in range(Nsamples):
            self.files[i] = files[i]


        # Loop over samples of a cohort

        # volume of cells in each fine region:
        # ***
        cell_volumes_fine   = np.zeros( (Nfine, Nsamples) )


        for ii,cdir in enumerate(self.files):

            backup = "%s/volume_per_coarse_region.dat" % cdir
            if os.path.exists(backup):
                self.pprint("Loading cell volumes in coarse regions from file.")
                tmp_ = np.loadtxt(backup, skiprows=1)
                self.vol[:, ii] = tmp_[:,1]

            else:
                self.pprint("Processing directory: %s" % cdir)


                # Volume of cells in each fine region
                self.pprint("Computing vol. of cells per fine region...")
                cells = adv.nrrd_data("%s/transformed_cells_eroded.nrrd" % cdir)
                for i,ID in enumerate(atlas.regions["fine_level"]):
                    print(ii, i)
                    idx = np.where(atlas.atlas_annotations==ID)
                    cell_volumes_fine[i, ii] += np.sum( cells[idx] )


                # Volume of cells in each coarse region: merge fine into coarse
                self.pprint("Computing vol. of cells per coarse region...")
                for i,ID in enumerate(atlas.regions["unique_coarse_level"]):
                    idx = np.where( atlas.regions["fine2coarse_level"] == ID )
                    self.vol[i, ii] += np.sum( cell_volumes_fine[idx, ii] )


                # Export total cell volume per corse region in file
                self.pprint("Exporting coarse region volumes.")
                fw = open("%s/volume_per_coarse_region.dat" % cdir, 'w')
                fw.write("%15s %15s\n" % ("Coarse ID", "total cell vol."))
                for i,ID in enumerate(atlas.regions["unique_coarse_level"]):
                    fw.write("%d %g\n" % (ID, self.vol[i,ii]))
                fw.close()


            # Cell densities in coarse regions
            with np.errstate(divide='warn', invalid='warn'):
                d = self.vol[:,ii] / atlas.regions["unique_coarse_vols"][:]
                d[np.isnan(d)] = -1
                self.densities[:,ii] = d[:]


        # Compute averages over samples
        self.mean[:] = np.mean(self.vol, axis=1)
        self.std[:]  = np.std( self.vol, axis=1)



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-pd', type=str, nargs='+', required=True, help="aligned directory for Placebo ")
    parser.add_argument('-ld', type=str, nargs='+', required=True, help="aligned directory for LowDose ")
    parser.add_argument('-hd', type=str, nargs='+', required=True, help="aligned directory for HighDose")
    args = parser.parse_args()

    # Read sample shape and instantiate atlas
    cells_ = skimage.io.imread("%s/voxelized_R15.tif" % (args.pd[0]), plugin='tifffile').T
    atlas = Atlas(cells_)


    # Compute cohort-wise stats
    print("Instantiating cohorts...")
    cohort_P = Cohort(args.pd, atlas)
    cohort_L = Cohort(args.ld, atlas)
    cohort_H = Cohort(args.hd, atlas)

    if 0:
        print("\ncohort_P")
        for i in range(atlas.Ncoarse):
            print(i, cohort_P.densities[i,:], cohort_P.vol[i,:])

        print("\ncohort_L")
        for i in range(atlas.Ncoarse):
            print(i, cohort_L.densities[i,:], cohort_L.vol[i,:])

        print("\ncohort_H")
        for i in range(atlas.Ncoarse):
            print(i, cohort_H.densities[i,:], cohort_H.vol[i,:])


    # Compute pvalues
    # two-sided t-test pvalue
    ttest_l = ttest_ind_from_stats(mean1=cohort_L.mean, std1=cohort_L.std, nobs1=3, mean2=cohort_P.mean, std2=cohort_P.std, nobs2=3)
    ttest_h = ttest_ind_from_stats(mean1=cohort_H.mean, std1=cohort_H.std, nobs1=3, mean2=cohort_P.mean, std2=cohort_P.std, nobs2=3)


    # Find non-nan pvalues
    condition = ((ttest_l.pvalue>0)*(ttest_l.pvalue<1)) == 1
    lstatistic = np.where( condition , ttest_l.statistic, 0)
    lpvalues   = np.where( condition , ttest_l.pvalue,    0)

    condition = ((ttest_h.pvalue>0)*(ttest_h.pvalue<1)) == 1
    hstatistic = np.where( condition , ttest_h.statistic, 0)
    hpvalues   = np.where( condition , ttest_h.pvalue,    0)


    # Split effect
    leffect = np.where(lstatistic>0, +lpvalues, 0)
    leffect = np.where(lstatistic<0, -lpvalues, leffect)
    heffect = np.where(hstatistic>0, +hpvalues, 0)
    heffect = np.where(hstatistic<0, -hpvalues, heffect)


    # Export CSV file

    fw = open("pvalues_L1_regions.csv", 'w')

    fw.write("%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\n " % ("Region ID", "Region name", "Region volume", "dens P1", "dens P2", "dens P3", "vol P1", "vol P2", "vol P3","avg_P",  "dens LD1", "dens LD2", "dens LD3", "vol LD1", "vol LD2", "vol LD3", "avg_LD",  "dens HD1", "dens HD2", "dens HD3", "vol HD1", "vol HD2", "vol HD3", "avg HD",  "pv LD", "pv HD") )

    for i in range(atlas.Ncoarse):
        fw.write("%g, %s, %g, %g, %g, %g, %g, %g, %g, %g, %g, %g, %g, %g, %g, %g, %g, %g, %g, %g, %g, %g, %g, %g, %g, %g\n " % (atlas.regions["unique_coarse_level"][i], atlas.regions["unique_coarse_names"][i].replace(',', ''), atlas.regions["unique_coarse_vols"][i], cohort_P.densities[i,0], cohort_P.densities[i,1], cohort_P.densities[i,2], cohort_P.vol[i,0], cohort_P.vol[i,1], cohort_P.vol[i,2], cohort_P.mean[i],   cohort_L.densities[i,0], cohort_L.densities[i,1], cohort_L.densities[i,2], cohort_L.vol[i,0], cohort_L.vol[i,1], cohort_L.vol[i,2], cohort_L.mean[i],    cohort_H.densities[i,0], cohort_H.densities[i,1], cohort_H.densities[i,2], cohort_H.vol[i,0], cohort_H.vol[i,1], cohort_H.vol[i,2], cohort_H.mean[i],    leffect[i],  heffect[i] ) )

    fw.close()


