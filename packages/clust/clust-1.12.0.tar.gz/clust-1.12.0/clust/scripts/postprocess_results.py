import numpy as np
import clust.scripts.datastructures as ds
import sklearn.metrics.pairwise as skdists
import clust.scripts.numeric as nu
import clust.scripts.statistical as st
import sys
from clust.scripts.mnplots import mnplotsdistancethreshold


def reorderClusters(B, X, GDM, returnOrderIndices = False):
    Bloc = np.array(B)
    Xloc = ds.listofarrays2arrayofarrays(X)

    Bloc = Bloc[:, np.any(Bloc, axis=0)]  # Only keep non-empty clusters

    B_ordered = np.zeros(Bloc.shape, dtype=bool)
    K = Bloc.shape[1]  # Number of clusters
    L = Xloc.shape[0]  # Number of datasets

    if K == 0:
        return Bloc

    # Find Cmeans and distances between clusters
    Cmeans = np.array([None] * L, dtype=object)
    D = np.full([K, K, L], np.inf)  # KxKxL  (initialised with inf values)
    for l in range(L):
        Cmeans[l] = np.zeros([K, Xloc[l].shape[1]], dtype=float)  # (K) x (X[l] samples)
        for k in range(K):
            Cmeans[l][k] = np.mean(Xloc[l][Bloc[GDM[:, l], k], :], axis=0)

        # For empty clusters, the distances are inf (as filled in the initialisation of D),
        # For non-empty clusters, the distances are calculated by skdists.euclidean_distances between cmeans
        I_not_empty_c = ~np.array([np.any(np.isnan(cm)) for cm in Cmeans[l]])  # Indices of clusters with nans (empty)
        I_not_empty_c = np.where(I_not_empty_c)[0]  # From boolean indices to integer indices
        non_empty_c_dists = skdists.euclidean_distances(Cmeans[l][I_not_empty_c])  # K_not_empty x K_not_empty
        for nec in range(len(I_not_empty_c)):
            D[I_not_empty_c[nec], I_not_empty_c, l] = non_empty_c_dists[nec]
        #D[:, :, l] = skdists.euclidean_distances(Cmeans[l])  # KxK
    D = np.median(D, axis=2)  # KxK

    # Set first cluster as first, then find closest by closest
    B_ordered[:, 0] = Bloc[:, 0]
    I = np.zeros(K, dtype=int)
    I[0] = 0
    clustersDone = np.zeros(K, dtype=bool)
    clustersDone[0] = True
    for k in range(1,K):
        relevantD = D[I[k-1], ~clustersDone]
        clustersLeft = np.nonzero(~clustersDone)[0]
        nextCluster = np.argmin(relevantD)
        nextCluster = clustersLeft[nextCluster]
        B_ordered[:, k] = Bloc[:, nextCluster]
        I[k] = nextCluster
        clustersDone[nextCluster] = True

    if returnOrderIndices:
        return (B_ordered, I)
    else:
        return B_ordered


def correcterrors_withinworse(B, X, GDM, falsepositivestrimmed=0.01):
    Bloc = np.array(B)
    Xloc = ds.listofarrays2arrayofarrays(X)

    [Ng, K] = Bloc.shape  # Ng genes and K clusters
    L = Xloc.shape[0]  # L datasets

    # Find clusters' means (Cmeans), absolute shifter clusters genes (SCG),
    # and the emperical CDF functions for them (cdfs)
    Cmeans = np.array([None] * L, dtype=object)
    SCG = np.array([None] * L, dtype=object)
    for l in range(L):
        Cmeans[l] = np.zeros([K, Xloc[l].shape[1]])  # K clusters x D dimensions
        SCG[l] = np.zeros([np.sum(np.sum(Bloc[GDM[:, l], :], axis=0)), Xloc[l].shape[1]])  # M* genes x D dimensions ...
        # (M* are all # genes in any cluster)

        gi = 0
        for k in range(K):
            Cmeans[l][k] = np.median(Xloc[l][Bloc[GDM[:, l], k], :], axis=0)
            csize = np.sum(Bloc[GDM[:, l], k])
            tmpSCG = nu.subtractaxis(Xloc[l][Bloc[GDM[:, l], k], :], Cmeans[l][k], axis=0)
            SCG[l][gi:(gi+csize),:] = np.abs(tmpSCG)
            gi += csize
        SCG[l] = SCG[l][np.any(SCG[l], axis=1)]  # Remove all zeros genes (rows of SCG[l])
        SCG[l] = np.sort(SCG[l], axis=0)
        if falsepositivestrimmed > 0:
            trimmed = int(falsepositivestrimmed * SCG[l].shape[0])
            if trimmed > 0:
                SCG[l] = SCG[l][0:-trimmed]  # trim the lowest (trimmed) rows in SCG

    # Helping function
    def iswithinworse(ref, x):
        return x <= np.max(ref)

    # Find who belongs
    belongs = np.ones([Ng, K, L], dtype=bool)  # Ng genes x K clusters x L datasets
    for l in range(L):
        for k in range(K):
            for d in range(Xloc[l].shape[1]):
                tmpX = np.abs(Xloc[l][:, d] - Cmeans[l][k, d])
                belongs[GDM[:, l], k, l] &= iswithinworse(SCG[l][:, d], tmpX)

    # Include in clusters genes which belongs everywhere
    B_out = np.all(belongs, axis=2)

    # Genes included in two clusters, include them in the closest in terms of its worst distance to any of the clusters
    # (guarrantee that the worst belongingness of a gene to a cluster is optimised)
    f = np.nonzero(np.sum(B_out, axis=1) > 1)[0]
    for fi in f:
        ficlusts = np.nonzero(B_out[fi])[0]  # Clusters competing over gene fi
        fidatasets = np.nonzero(GDM[fi])[0]  # Datasets that have gene fi
        localdists = np.zeros([len(ficlusts), len(fidatasets)])  # (Clusts competing) x (datasets that have fi)
        for l in range(len(fidatasets)):
            ll = fidatasets[l]  # Actual dataset index
            fi_ll = np.sum(GDM[:fi, ll])  # Index of fi in this Xloc[ll]
            localdists[:, l] = nu.dist_matrices(Cmeans[ll][ficlusts], Xloc[ll][fi_ll]).reshape([len(ficlusts)])
        localdists = np.max(localdists, axis=1)  # (Clusts competing) x 1
        ficlosest = np.argmin(localdists)  # Closest cluster
        B_out[fi] = False
        B_out[fi, ficlusts[ficlosest]] = True

    return B_out


def correcterrors_weighted_fixed_fpr(B, X, GDM, clustdists=None, falsepositivestrimmed=0.01, smallestClusterSize=11):
    Bloc = np.array(B)
    Xloc = ds.listofarrays2arrayofarrays(X)

    [Ng, K] = Bloc.shape  # Ng genes and K clusters
    L = Xloc.shape[0]  # L datasets

    # Normalise clustdists to provide weights. If not provided, make it unity for all
    if clustdists is None:
        clustdistsnorm = np.ones(K)
    else:
        clustweights = np.min(clustdists) / clustdists

    # Find clusters' means (Cmeans), absolute shifted clusters genes (SCG),
    # and the emperical CDF functions for them (cdfs)
    Cmeans = np.array([None] * L, dtype=object)
    SCG = np.array([None] * L, dtype=object)
    for l in range(L):
        Cmeans[l] = np.zeros([K, Xloc[l].shape[1]])  # K clusters x D dimensions
        SCG[l] = np.zeros([np.sum(np.sum(Bloc[GDM[:, l], :], axis=0)), Xloc[l].shape[1]])  # M* genes x D dimensions ...
        # (M* are all # genes in any cluster)

        gi = 0
        for k in range(K):
            Cmeans[l][k] = np.median(Xloc[l][Bloc[GDM[:, l], k], :], axis=0)
            csize = np.sum(Bloc[GDM[:, l], k])
            tmpSCG = nu.subtractaxis(Xloc[l][Bloc[GDM[:, l], k], :], Cmeans[l][k], axis=0)
            # MAIN ADDITION (SCG is weighted by clustweights, max clustweight is unity, and it is the best)
            tmpSCG = tmpSCG * clustweights[k]
            SCG[l][gi:(gi + csize), :] = np.abs(tmpSCG)
            gi += csize
        SCG[l] = SCG[l][np.any(SCG[l], axis=1)]  # Remove all zeros genes (rows of SCG[l])
        SCG[l] = np.sort(SCG[l], axis=0)
        if falsepositivestrimmed > 0:
            trimmed = int(falsepositivestrimmed * SCG[l].shape[0])
            if trimmed > 0:
                SCG[l] = SCG[l][0:-trimmed]  # trim the lowest (trimmed) rows in SCG

    # Helping function
    def iswithinworse(ref, x):
        return x <= np.max(ref)

    # Find who belongs
    belongs = np.ones([Ng, K, L], dtype=bool)  # Ng genes x K clusters x L datasets
    for l in range(L):
        for k in range(K):
            for d in range(Xloc[l].shape[1]):
                tmpX = np.abs(Xloc[l][:, d] - Cmeans[l][k, d])
                belongs[GDM[:, l], k, l] &= iswithinworse(SCG[l][:, d], tmpX)

    # Include in clusters genes which belongs everywhere
    B_out = np.all(belongs, axis=2)

    # Solve genes included in two clusters:
    solution = 2
    if solution == 1:
        # Genes included in two clusters, include them in the closest in terms of its worst distance to any of the clusters
        # (guarrantee that the worst belongingness of a gene to a cluster is optimised)
        f = np.nonzero(np.sum(B_out, axis=1) > 1)[0]
        for fi in f:
            ficlusts = np.nonzero(B_out[fi])[0]  # Clusters competing over gene fi
            fidatasets = np.nonzero(GDM[fi])[0]  # Datasets that have gene fi
            localdists = np.zeros([len(ficlusts), len(fidatasets)])  # (Clusts competing) x (datasets that have fi)
            for l in range(len(fidatasets)):
                ll = fidatasets[l]  # Actual dataset index
                fi_ll = np.sum(GDM[:fi, ll])  # Index of fi in this Xloc[ll]
                localdists[:, l] = nu.dist_matrices(Cmeans[ll][ficlusts], Xloc[ll][fi_ll]).reshape([len(ficlusts)])
            localdists = np.max(localdists, axis=1)  # (Clusts competing) x 1
            ficlosest = np.argmin(localdists)  # Closest cluster
            B_out[fi] = False
            B_out[fi, ficlusts[ficlosest]] = True
    elif solution == 2:
        # Genes included in two clusters, include them in the earlier cluster (smallest k)
        f = np.nonzero(np.sum(B_out, axis=1) > 1)[0]
        for fi in f:
            ficlusts = np.nonzero(B_out[fi])[0]  # Clusters competing over gene fi
            ficlosest = np.argmin(ficlusts)  # earliest cluster (smallest k)
            B_out[fi] = False
            B_out[fi, ficlusts[ficlosest]] = True



    # Remove clusters smaller than minimum cluster size
    ClusterSizes = np.sum(B_out, axis=0)
    B_out = B_out[:, ClusterSizes >= smallestClusterSize]

    return B_out


def correcterrors_weighted_outliers(B, X, GDM, clustdists=None, stds=3, smallestClusterSize=11):
    Bloc = np.array(B)
    Xloc = ds.listofarrays2arrayofarrays(X)

    [Ng, K] = Bloc.shape  # Ng genes and K clusters
    L = Xloc.shape[0]  # L datasets

    # Normalise clustdists to provide weights. If not provided, make it unity for all
    if clustdists is None:
        clustweights = np.ones(K)
    else:
        clustweights = np.min(clustdists) / clustdists

    # Find clusters' means (Cmeans), absolute shifted clusters genes (SCG),
    # and the emperical CDF functions for them (cdfs)
    Cmeans = np.array([None] * L, dtype=object)
    SCG = np.array([None] * L, dtype=object)
    for l in range(L):
        Cmeans[l] = np.zeros([K, Xloc[l].shape[1]])  # K clusters x D dimensions
        SCG[l] = np.zeros([np.sum(np.sum(Bloc[GDM[:, l], :], axis=0)), Xloc[l].shape[1]])  # M* genes x D dimensions ...
        # (M* are all # genes in any cluster)

        gi = 0
        for k in range(K):
            Cmeans[l][k] = np.median(Xloc[l][Bloc[GDM[:, l], k], :], axis=0)
            csize = np.sum(Bloc[GDM[:, l], k])
            tmpSCG = nu.subtractaxis(Xloc[l][Bloc[GDM[:, l], k], :], Cmeans[l][k], axis=0)
            # MAIN ADDITION (SCG is weighted by clustweights, max clustweight is unity, and it is the best)
            tmpSCG = tmpSCG * clustweights[k]
            SCG[l][gi:(gi + csize), :] = np.abs(tmpSCG)
            gi += csize
        SCG[l] = SCG[l][np.any(SCG[l], axis=1)]  # Remove all zeros genes (rows of SCG[l])
        SCG[l] = np.sort(SCG[l], axis=0)
        SCGmeans = np.mean(SCG[l], axis=0)
        SCGstds = np.std(SCG[l], axis=0)
        SCGouts = nu.divideaxis(nu.subtractaxis(SCG[l], SCGmeans, axis=0), SCGstds, axis=0)  # No. of stds away
        SCGouts = SCGouts > stds  # TRUE for outliers and FALSE for others (bool: M* genex x D dimensions)
        SCG[l][SCGouts] = 0.0  # Set the outlier values to zeros so they do not affect decisions later on

    # Helping function
    def iswithinworse(ref, x):
        return x <= np.max(ref)

    # Find who belongs
    belongs = np.ones([Ng, K, L], dtype=bool)  # Ng genes x K clusters x L datasets
    for l in range(L):
        for k in range(K):
            for d in range(Xloc[l].shape[1]):
                tmpX = np.abs(Xloc[l][:, d] - Cmeans[l][k, d])
                belongs[GDM[:, l], k, l] &= iswithinworse(SCG[l][:, d], tmpX)

    # Include in clusters genes which belongs everywhere
    B_out = np.all(belongs, axis=2)

    # Solve genes included in two clusters:
    solution = 2
    if solution == 1:
        # Genes included in two clusters, include them in the closest in terms of its worst distance to any of the clusters
        # (guarrantee that the worst belongingness of a gene to a cluster is optimised)
        f = np.nonzero(np.sum(B_out, axis=1) > 1)[0]
        for fi in f:
            ficlusts = np.nonzero(B_out[fi])[0]  # Clusters competing over gene fi
            fidatasets = np.nonzero(GDM[fi])[0]  # Datasets that have gene fi
            localdists = np.zeros([len(ficlusts), len(fidatasets)])  # (Clusts competing) x (datasets that have fi)
            for l in range(len(fidatasets)):
                ll = fidatasets[l]  # Actual dataset index
                fi_ll = np.sum(GDM[:fi, ll])  # Index of fi in this Xloc[ll]
                localdists[:, l] = nu.dist_matrices(Cmeans[ll][ficlusts], Xloc[ll][fi_ll]).reshape([len(ficlusts)])
            localdists = np.max(localdists, axis=1)  # (Clusts competing) x 1
            ficlosest = np.argmin(localdists)  # Closest cluster
            B_out[fi] = False
            B_out[fi, ficlusts[ficlosest]] = True
    elif solution == 2:
        # Genes included in two clusters, include them in the earlier cluster (smallest k)
        f = np.nonzero(np.sum(B_out, axis=1) > 1)[0]
        for fi in f:
            ficlusts = np.nonzero(B_out[fi])[0]  # Clusters competing over gene fi
            ficlosest = np.argmin(ficlusts)  # earliest cluster (smallest k)
            B_out[fi] = False
            B_out[fi, ficlusts[ficlosest]] = True



    # Remove clusters smaller than minimum cluster size
    ClusterSizes = np.sum(B_out, axis=0)
    B_out = B_out[:, ClusterSizes >= smallestClusterSize]

    return B_out


'''This version uses weighted mean and std of SCG rather than giving weights to the errors themselves'''
def correcterrors_weighted_outliers2(B, X, GDM, clustdists=None, stds=3, smallestClusterSize=11):
    Bloc = np.array(B)
    Xloc = ds.listofarrays2arrayofarrays(X)

    [Ng, K] = Bloc.shape  # Ng genes and K clusters
    L = Xloc.shape[0]  # L datasets

    # Normalise clustdists to provide weights. If not provided, make it unity for all
    if clustdists is None:
        clustweights = np.ones(K)
    else:
        clustweights = np.min(clustdists) / clustdists

    # Find clusters' means (Cmeans), absolute shifted clusters genes (SCG),
    # and the emperical CDF functions for them (cdfs)
    Cmeans = np.array([None] * L, dtype=object)
    SCG = np.array([None] * L, dtype=object)
    for l in range(L):
        Cmeans[l] = np.zeros([K, Xloc[l].shape[1]])  # K clusters x D dimensions
        SCG[l] = np.zeros([np.sum(np.sum(Bloc[GDM[:, l], :], axis=0)), Xloc[l].shape[1]])  # M* genes x D dimensions ...
        w = np.zeros(np.sum(np.sum(Bloc[GDM[:, l], :], axis=0)))  # M* genes
        # (M* are all # genes in any cluster)

        gi = 0
        for k in range(K):
            Cmeans[l][k] = np.median(Xloc[l][Bloc[GDM[:, l], k], :], axis=0)
            csize = np.sum(Bloc[GDM[:, l], k])
            tmpSCG = nu.subtractaxis(Xloc[l][Bloc[GDM[:, l], k], :], Cmeans[l][k], axis=0)
            SCG[l][gi:(gi + csize), :] = np.abs(tmpSCG)
            # Added this in this version
            w[gi:(gi + csize)] = clustweights[k]
            gi += csize
        SCG[l] = SCG[l][np.any(SCG[l], axis=1)]  # Remove all zeros genes (rows of SCG[l])
        SCG[l] = np.sort(SCG[l], axis=0)
        SCGmeans = np.average(SCG[l], weights=w, axis=0)
        SCGstds = st.weighted_std_axis(SCG[l], weights=w, axix=0)
        SCGouts = nu.divideaxis(nu.subtractaxis(SCG[l], SCGmeans, axis=0), SCGstds, axis=0)  # No. of stds away
        SCGouts = SCGouts > stds  # TRUE for outliers and FALSE for others (bool: M* genex x D dimensions)
        SCG[l][SCGouts] = 0.0  # Set the outlier values to zeros so they do not affect decisions later on

    # Helping function
    def iswithinworse(ref, x):
        return x <= np.max(ref)

    # Find who belongs
    belongs = np.ones([Ng, K, L], dtype=bool)  # Ng genes x K clusters x L datasets
    for l in range(L):
        for k in range(K):
            for d in range(Xloc[l].shape[1]):
                tmpX = np.abs(Xloc[l][:, d] - Cmeans[l][k, d])
                belongs[GDM[:, l], k, l] &= iswithinworse(SCG[l][:, d], tmpX)

    # Include in clusters genes which belongs everywhere
    B_out = np.all(belongs, axis=2)

    # Solve genes included in two clusters:
    solution = 2
    if solution == 1:
        # Genes included in two clusters, include them in the closest in terms of its worst distance to any of the clusters
        # (guarrantee that the worst belongingness of a gene to a cluster is optimised)
        f = np.nonzero(np.sum(B_out, axis=1) > 1)[0]
        for fi in f:
            ficlusts = np.nonzero(B_out[fi])[0]  # Clusters competing over gene fi
            fidatasets = np.nonzero(GDM[fi])[0]  # Datasets that have gene fi
            localdists = np.zeros([len(ficlusts), len(fidatasets)])  # (Clusts competing) x (datasets that have fi)
            for l in range(len(fidatasets)):
                ll = fidatasets[l]  # Actual dataset index
                fi_ll = np.sum(GDM[:fi, ll])  # Index of fi in this Xloc[ll]
                localdists[:, l] = nu.dist_matrices(Cmeans[ll][ficlusts], Xloc[ll][fi_ll]).reshape([len(ficlusts)])
            localdists = np.max(localdists, axis=1)  # (Clusts competing) x 1
            ficlosest = np.argmin(localdists)  # Closest cluster
            B_out[fi] = False
            B_out[fi, ficlusts[ficlosest]] = True
    elif solution == 2:
        # Genes included in two clusters, include them in the earlier cluster (smallest k)
        f = np.nonzero(np.sum(B_out, axis=1) > 1)[0]
        for fi in f:
            ficlusts = np.nonzero(B_out[fi])[0]  # Clusters competing over gene fi
            ficlosest = np.argmin(ficlusts)  # earliest cluster (smallest k)
            B_out[fi] = False
            B_out[fi, ficlusts[ficlosest]] = True



    # Remove clusters smaller than minimum cluster size
    ClusterSizes = np.sum(B_out, axis=0)
    B_out = B_out[:, ClusterSizes >= smallestClusterSize]

    return B_out


def optimise_tukey_sqrtSCG(B, X, GDM, clustdists=None, smallestClusterSize=11, tails=1, Q3s=2):
    Bloc = np.array(B)
    Xloc = ds.listofarrays2arrayofarrays(X)

    [Ng, K] = Bloc.shape  # Ng genes and K clusters
    L = Xloc.shape[0]  # L datasets

    # Normalise clustdists to provide weights. If not provided, make it unity for all
    if clustdists is None:
        clustdistsloc = np.ones(K)
    else:
        clustdistsloc = [c for c in clustdists]

    # Find clusters' means (Cmeans), absolute shifted clusters genes (SCG),
    # and the emperical CDF functions for them (cdfs)
    Cmeans = np.array([None] * L, dtype=object)
    SCG = np.array([None] * L, dtype=object)

    Cgood = mnplotsdistancethreshold(clustdistsloc, method='largestgap')
    for l in range(L):
        Cmeans[l] = np.zeros([K, Xloc[l].shape[1]])  # K clusters x D dimensions
        SCG[l] = np.zeros([np.sum(np.sum(Bloc[GDM[:, l], :], axis=0)), Xloc[l].shape[1]])  # M* genes x D dimensions ...
        w = np.zeros(np.sum(np.sum(Bloc[GDM[:, l], :], axis=0)))  # M* genes
        # (M* are all # genes in any cluster)

        gi = 0
        for k in range(K):
            if k in Cgood:
                Cmeans[l][k] = np.median(Xloc[l][Bloc[GDM[:, l], k], :], axis=0)
                csize = np.sum(Bloc[GDM[:, l], k])
                tmpSCG = nu.subtractaxis(Xloc[l][Bloc[GDM[:, l], k], :], Cmeans[l][k], axis=0)
                SCG[l][gi:(gi + csize), :] = np.abs(tmpSCG)
                gi += csize
            else:
                Cmeans[l][k] = np.empty(Xloc[l].shape[1])
                Cmeans[l][k][:] = np.nan
        SCG[l] = SCG[l][np.any(SCG[l], axis=1)]  # Remove all zeros genes (rows of SCG[l])

        if ds.numel(SCG[l] > 0):
            if tails == 1:
                Q3 = np.percentile(SCG[l], q=75, axis=0)
                thresh = Q3s * Q3
                SCGouts = SCG[l] > np.array([thresh for ii in range(0, SCG[l].shape[0])])
                SCG[l][SCGouts] = 0.0  # Set the outlier values to zeros so they do not affect decisions later on
            elif tails == 2:
                Q1 = np.percentile(np.sqrt(SCG[l]), q=25, axis=0)
                Q3 = np.percentile(np.sqrt(SCG[l]), q=75, axis=0)
                IQR = np.subtract(Q3, Q1)
                thresh = np.add(Q3, 1.5 * IQR)
                SCGouts = np.sqrt(SCG[l]) > np.array([thresh for ii in range(0, SCG[l].shape[0])])
                SCG[l][SCGouts] = 0.0  # Set the outlier values to zeros so they do not affect decisions later on
            else:
                raise ValueError('Invalid number of tails. It should be either 1 or 2.')
        else:
            SCG[l] = np.zeros((1, SCG[l].shape[1]))

    # Clusters mins and maxes (NEW)
    Cmins = np.array([None] * L, dtype=object)
    Cmaxes = np.array([None] * L, dtype=object)
    for l in range(L):
        Cmins[l] = np.zeros([K, Xloc[l].shape[1]])  # K clusters x D dimensions
        Cmaxes[l] = np.zeros([K, Xloc[l].shape[1]])  # K clusters x D dimensions
        for k in range(K):
            Cmins[l][k] = Cmeans[l][k] - np.max(SCG[l], axis=0)
            Cmaxes[l][k] = Cmeans[l][k] + np.max(SCG[l], axis=0)

    # Resolve overlaps between clusters (NEW)
    for k1 in range(K):
        for k2 in range(K):
            # Compare the pair of clusters only once, and don't compare a cluster with itself. This if statement
            # guarantees that k2 will always be a later cluster than k1.
            if (k1 >= k2):
                continue
            # Value of the smallest overlap between the ranges of the clusters k1 and k2, and ...
            # the dataset (l) and the dimension (d), at which this overlap is found
            # t_smallest overlap is the type of the overlap, (-1, 0, 1, or 2). Type (-1) means that the entire (min
            # to max) range of one cluster is within the range of the other cluster. This is the worse overlap.
            # Type (0) means that the max of (k1) is within the range of (min to max) of (k2), and type (1) is the other
            # way around. Type (2) means there is no overlap. This is the best and finding one of it breaks the loop
            v_smallestoverlap = 0
            l_smallestoverlap = -1
            d_smallestoverlap = -1
            t_smallestoverlap = -1  # Overlap type, read above
            for l in range(L):
                Nd = len(Cmins[l][k1])  # Dimensions in this dataset
                for d in range(Nd):
                    x1 = Cmaxes[l][k1][d]
                    x2 = Cmaxes[l][k2][d]
                    n1 = Cmins[l][k1][d]
                    n2 = Cmins[l][k2][d]
                    if (x1 > n2 and x1 <= x2):
                        if (n1 < n2):
                            ov = x1 - n2
                            if (t_smallestoverlap == -1 or ov < v_smallestoverlap):
                                t_smallestoverlap = 0
                                v_smallestoverlap = ov
                                l_smallestoverlap = l
                                d_smallestoverlap = d
                    elif (x2 > n1 and x2 <= x1):
                        if (n2 < n1):
                            ov = x2 - n1
                            if (t_smallestoverlap == -1 or ov < v_smallestoverlap):
                                t_smallestoverlap = 1
                                v_smallestoverlap = ov
                                l_smallestoverlap = l
                                d_smallestoverlap = d
                    else:
                        t_smallestoverlap = 2
                        continue  # Absolutely no overlap at this point, so k1 and k2 are distinct, so continue
                if (t_smallestoverlap == 2):
                    continue  # Absolutely no overlap at some point, so k1 and k2 are distinct, so continue

            # Sort out the overlap if exists between k1 and k2
            if (t_smallestoverlap == -1):
                # Here one of the two clusters always swallows the other one. So effectively remove the later one (k2).
                # Cluster removal is by making its minimum larger than its maximum at a single point (at l=0, d=0),
                # so effectively no gene will ever be mapped to it!
                Cmins[0][k2][0] = 1
                Cmaxes[0][k2][0] = 0
            elif (t_smallestoverlap == 0):
                Cmins[l_smallestoverlap][k2][d_smallestoverlap] = \
                    Cmaxes[l_smallestoverlap][k1][d_smallestoverlap] + sys.float_info.epsilon
            elif (t_smallestoverlap == 1):
                Cmaxes[l_smallestoverlap][k2][d_smallestoverlap] = \
                    Cmins[l_smallestoverlap][k1][d_smallestoverlap] - sys.float_info.epsilon

    # Find who belongs (NEW)
    belongs = np.ones([Ng, K, L], dtype=bool)  # Ng genes x K clusters x L datasets
    for l in range(L):
        for k in range(K):
            tmp1 = nu.largerthanaxis(Xloc[l], Cmins[l][k], axis=0, orequal=True)
            tmp2 = nu.lessthanaxis(Xloc[l], Cmaxes[l][k], axis=0, orequal=True)
            belongs[GDM[:, l], k, l] = np.all(np.logical_and(tmp1, tmp2), axis=1)


    # # Helping function (OLD - to be removed)
    # def iswithinworse(ref, x):
    #     return x <= np.max(ref)
    #
    # # Find who belongs (OLD - to be removed)
    # belongs = np.ones([Ng, K, L], dtype=bool)  # Ng genes x K clusters x L datasets
    # for l in range(L):
    #     for k in range(K):
    #         for d in range(Xloc[l].shape[1]):
    #             tmpX = np.abs(Xloc[l][:, d] - Cmeans[l][k, d])
    #             belongs[GDM[:, l], k, l] &= iswithinworse(SCG[l][:, d], tmpX)

    # Include in clusters genes which belongs everywhere (OLD - to be removed)
    B_out = np.all(belongs, axis=2)

    # Solve genes included in two clusters (OLD - should not be needed now - TO BE REMOVED)
    solution = 2
    if solution == 1:
        # Genes included in two clusters, include them in the closest in terms of its worst distance to any of the clusters
        # (guarrantee that the worst belongingness of a gene to a cluster is optimised)
        f = np.nonzero(np.sum(B_out, axis=1) > 1)[0]
        for fi in f:
            ficlusts = np.nonzero(B_out[fi])[0]  # Clusters competing over gene fi
            fidatasets = np.nonzero(GDM[fi])[0]  # Datasets that have gene fi
            localdists = np.zeros([len(ficlusts), len(fidatasets)])  # (Clusts competing) x (datasets that have fi)
            for l in range(len(fidatasets)):
                ll = fidatasets[l]  # Actual dataset index
                fi_ll = np.sum(GDM[:fi, ll])  # Index of fi in this Xloc[ll]
                localdists[:, l] = nu.dist_matrices(Cmeans[ll][ficlusts], Xloc[ll][fi_ll]).reshape([len(ficlusts)])
            localdists = np.max(localdists, axis=1)  # (Clusts competing) x 1
            ficlosest = np.argmin(localdists)  # Closest cluster
            B_out[fi] = False
            B_out[fi, ficlusts[ficlosest]] = True
    elif solution == 2:
        # Genes included in two clusters, include them in the earlier cluster (smallest k)
        f = np.nonzero(np.sum(B_out, axis=1) > 1)[0]
        for fi in f:
            ficlusts = np.nonzero(B_out[fi])[0]  # Clusters competing over gene fi
            ficlosest = np.argmin(ficlusts)  # earliest cluster (smallest k)
            B_out[fi] = False
            B_out[fi, ficlusts[ficlosest]] = True



    # Remove clusters smaller than minimum cluster size
    ClusterSizes = np.sum(B_out, axis=0)
    B_out = B_out[:, ClusterSizes >= smallestClusterSize]

    return B_out