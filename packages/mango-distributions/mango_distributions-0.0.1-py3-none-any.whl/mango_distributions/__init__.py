from scipy.stats import norm, poisson, binom


def draw_random_numbers(n_samples, dist,
                        mean=None, sd=None,
                        shape=None,
                        prob=None, trials=None):
    """Draw random numbers from a given distribution.
    # Args:
        n_samples: number of samples to draw
        dist: which distribution to draw from
              (Normal, Poisson or Binomial)

    # Additional Args:
        mean: mean (for Normal)
        sd: standard deviation (for Normal)
        shape: shape (for Poisson)
        prob: probability of success (for Binom)
        trials: number of trials (for Binom)

    # Returns:
        array of random numbers, drawn from a given distribution
    """
    if dist == 'Normal':
        samples = norm.rvs(size=n_samples, loc=mean, scale=sd)
    if dist == 'Poisson':
        samples = poisson.rvs(mu=shape, size=n_samples)
    if dist == 'Binomial':
        samples = binom.rvs(size=n_samples, p=prob, n=trials)
    return samples


class Distribution:
    def __init__(self, n_samples, dist,
                 mean=None, sd=None,
                 shape=None,
                 prob=None, trials=None):
        """Distribution parameters"""
        self.n_samples = n_samples
        self.dist = dist
        self.mean = mean
        self.sd = sd
        self.shape = shape
        self.prob = prob
        self.trials = trials
        self.sample = None

    def draw(self):
        """Draw random numbers from a given distribution.

        # Args:
            self.n_samples: number of samples to draw
            self.dist: which distribution to draw from
                      (Normal, Poisson or Binomial)

        # Additional Args:
            self.mean: mean (for Normal)
            self.sd: standard deviation (for Normal)
            self.shape: shape (for Poisson)
            self.prob: probability of success (for Binom)
            self.trials: number of trials (for Binom)

        # Returns:
            array of random numbers, drawn from a given distribution
        """
        if self.dist == 'Normal':
            self.sample = norm.rvs(size=self.n_samples,
                                   loc=self.mean, scale=self.sd)
        if self.dist == 'Poisson':
            self.sample = poisson.rvs(mu=self.shape, size=self.n_samples)
        if self.dist == 'Binomial':
            self.sample = binom.rvs(size=self.n_samples,
                                    p=self.prob, n=self.trials)
        return self.sample

    def summarise(self):
        """Print summary statistics of sample.

        # Args:
          self.sample: sample created using the draw function

        # Prints:
          min, max, mean and standard deviation
        """
        p_min = min(self.sample)
        p_max = max(self.sample)
        p_mean = self.sample.mean()
        p_sd = self.sample.std()
        print(f'Min: {round(p_min, 2)}')
        print(f'Max: {round(p_max, 2)}')
        print(f'Mean: {round(p_mean, 2)}')
        print(f'SD: {round(p_sd, 2)}')
