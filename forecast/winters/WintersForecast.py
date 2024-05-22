

class WintersForecast:
    def __init__(self, series, data_size):
        self.series = series
        self.data_size = data_size

    def get(self, coefs, n=0, non_negative=True):
        alpha_, beta_, gamma_, r = coefs
        r = int(r)
        if r < 0:
            print(f"Coef r is lower than 0, r={r}")

        y = self.series  # empiric series
        N = self.data_size  # empiric series size
        F, S, C = {}, {}, {}  # model partials
        yf = {}  # modeled series

        # calculate initial partials
        F[r + 1] = 1.0 / r * sum([y[i] for i in range(1, r + 1)])
        S[r + 1] = -F[r + 1] + 1.0 / r * sum([y[i] for i in range(r + 1, 2 * r + 1)])
        for t in range(1, r + 1):
            C[t] = y[t] - F[r + 1]
        C[r + 1] = gamma_ * (y[r + 1] - F[r + 1]) + (1 - gamma_) * C[1]

        for t in range(r + 2, N + n + 1):
            if t > N:
                yf[t] = F[N] + S[N] * (t - N) + C[t - r]
            else:
                F[t] = alpha_ * (y[t] - C[t - r]) + (1 - alpha_) * (F[t - 1] + S[t - 1])
                S[t] = beta_ * (F[t] - F[t - 1]) + (1 - beta_) * S[t - 1]
                C[t] = gamma_ * (y[t] - F[t]) + (1 - gamma_) * C[t - r]
                yf[t] = F[t - 1] + S[t - 1] + C[t - r]
            if yf[t] < 0 and non_negative:
                yf[t] = 0
        return yf
