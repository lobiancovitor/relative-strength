from breadth.plot_configs import (
    plot_percent_above_ma,
    plot_mc_clellan_summation_index,
    plot_cumulative_net_new_highs,
)


def breadth(data, len):
    plot_percent_above_ma(data, len)
    plot_mc_clellan_summation_index(data)
    plot_cumulative_net_new_highs(data)
