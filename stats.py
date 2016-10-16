import matplotlib.pyplot as plt
from scipy.stats import norm

def create_hist(data):
    (mul, sigmal) = norm.fit(data[0])
    (muw, sigmaw) = norm.fit(data[1])
    plt.subplot(221)
    n, bins, patches = plt.hist(data[0], 10, facecolor='r')
    plt.xlabel('Length')
    plt.ylabel('count')
    plt.title(r'$\mathrm{Lenghts:}\ \mu=%.3f,\ \sigma=%.3f$' %(mul, sigmal))
    #plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
    plt.axis([5, 10, 0, 10])
    #plt.grid(True)
    plt.grid(True)
    
    # Width
    plt.subplot(222)
    n, bins, patches = plt.hist(data[1], 10, facecolor='b')
    plt.xlabel('Width')
    plt.ylabel('count')
    plt.title(r'$\mathrm{Widths:}\ \mu=%.3f,\ \sigma=%.3f$' % (muw, sigmaw))
    plt.axis([1, 5, 0, 10])
    plt.grid(True)
    
    plt.savefig("results/finalplot.png")
    plt.show()
    return
