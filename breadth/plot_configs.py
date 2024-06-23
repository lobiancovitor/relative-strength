import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
import mplfinance as mpf


def configure_plot(ax, percent_formatter=None):
    ax.spines["left"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.minorticks_on()

    ax.grid(which="major", color="gray", linestyle="-", linewidth=0.5, alpha=0.5)
    ax.grid(which="minor", color="gray", linestyle=":", linewidth=0.5, alpha=0.4)

    ax.xaxis.set_major_locator(plt.MaxNLocator(nbins=10))
    ax.yaxis.set_major_locator(plt.MaxNLocator(nbins=7))

    if percent_formatter:
        ax.yaxis.set_major_formatter(FuncFormatter(percent_formatter))


def plot_percent_above_ma(data, len):
    
    sma_200 = data.rolling(window=200).mean()
    above_sma_200 = (data > sma_200).sum(axis=1)
    percent_above_sma_200 = (above_sma_200 / len) * 100

    sma_50_of_percent_above_200 = percent_above_sma_200.rolling(window=50).mean()
    
    
    def percent_formatter(x, pos):
        return f"{x:.0f}%"

    egrid = (21, 29)
    fig = mpf.figure(style="ibd", figsize=(15, 9))
    ax1 = plt.subplot2grid(egrid, (1, 0), colspan=26, rowspan=16)

    configure_plot(ax1, percent_formatter)

    ax1.axhline(y=70, color="green", linestyle="--", linewidth=1)
    ax1.axhline(y=25, color="red", linestyle="--", linewidth=1)

    ax1.plot(percent_above_sma_200[-450:], label="$BRA200R", linewidth=1.5)
    ax1.plot(
        sma_50_of_percent_above_200[-450:], label="MA(50)", linestyle="-", linewidth=1.5
    )

    ax1.set_title("IBOV Percent of Stocks Above 200 Day Moving Average (EOD)")
    ax1.legend(loc="upper left")

    plt.savefig('output/$BRA200R.png', bbox_inches='tight')


def plot_mc_clellan_summation_index(summation_index_last_450, moving_average_20):
    egrid = (21, 29)
    fig = mpf.figure(style="ibd", figsize=(15, 9))
    ax1 = plt.subplot2grid(egrid, (1, 0), colspan=26, rowspan=16)

    configure_plot(ax1)

    ax1.plot(summation_index_last_450, label="$BRSI", linewidth=1.5)
    ax1.plot(moving_average_20, label="MA(20)", linestyle="-", linewidth=1.5)

    ax1.set_title("IBOV McClellan Summation Index (Ratio Adjusted) (EOD)")
    ax1.legend(loc="upper left")

    plt.savefig('output/$BRSI.png', bbox_inches='tight')

def plot_cumulative_net_new_highs(cumulative_net_new_highs, sma_20):
    egrid = (21, 29)
    fig = mpf.figure(style="ibd", figsize=(15, 9))
    ax1 = plt.subplot2grid(egrid, (1, 0), colspan=26, rowspan=16)

    configure_plot(ax1)

    ax1.plot(cumulative_net_new_highs[-450:], label="$BRHL Cumulative", linewidth=1.5)
    ax1.plot(sma_20[-450:], label="MA(20)", linestyle='-', linewidth=1.5)

    ax1.set_title("IBOV Cumulative New Highs-New Lows (EOD)")
    ax1.legend(loc='upper left')

    plt.savefig('output/$BRHL.png', bbox_inches='tight')
