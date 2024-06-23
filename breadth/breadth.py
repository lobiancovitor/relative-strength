from breadth.plot_configs import plot_percent_above_ma


# def percent_above_ma(data):
#     sma_200 = data.rolling(window=200).mean()
#     above_sma_200 = (data > sma_200).sum(axis=1)
#     percent_above_sma_200 = (above_sma_200 / len(data)) * 100

#     sma_50_of_percent_above_200 = percent_above_sma_200.rolling(window=50).mean()

#     plot_percent_above_ma(percent_above_sma_200, sma_50_of_percent_above_200)


def mc_clellan_summation_index(summation_index_last_450, moving_average_20):
    pass


def cumulative_net_new_highs(cumulative_net_new_highs, sma_20):
    pass


def breadth(data, len):
    plot_percent_above_ma(data, len)
