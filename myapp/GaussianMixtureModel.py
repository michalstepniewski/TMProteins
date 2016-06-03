import sklearn.mixture

gmm = sklearn.mixture.GMM()

# sample data
a = np.random.randn(1000)

# result
r = gmm.fit(a)
print("mean : %f, var : %f" % (r.means_[0, 0], r.covars_[0, 0]))

# Reference : http://scikit-learn.org/stable/modules/mixture.html#mixture
