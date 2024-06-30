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

    plt.savefig("market/$BRA200R.png", bbox_inches="tight")


def plot_mc_clellan_summation_index(data):
    advances = (data.pct_change() > 0).sum(axis=1)
    declines = (data.pct_change() < 0).sum(axis=1)

    adv_dec_diff = advances - declines

    # RANA normalizes the indicator by showing net advances as a percentage of advances plus declines

    ana = (
        adv_dec_diff / (advances + declines)
    )  # StockCharts.com calculates Net Advances as a percentage of advances plus declines

    ema_19_adj = ana.ewm(span=19, adjust=False).mean()
    ema_39_adj = ana.ewm(span=39, adjust=False).mean()

    adjusted_mc_clellan_oscillator = (
        ema_19_adj - ema_39_adj
    ) * 1000  # Obtain whole numbers and eliminate decimals

    adjusted_mc_clellan_oscillator = adjusted_mc_clellan_oscillator.dropna()

    summation_index = adjusted_mc_clellan_oscillator.copy()
    summation_index.iloc[0] = adjusted_mc_clellan_oscillator.iloc[0]

    for i in range(1, len(summation_index)):
        summation_index.iloc[i] = (
            summation_index.iloc[i - 1] + adjusted_mc_clellan_oscillator.iloc[i]
        )

    summation_index_last_450 = summation_index.iloc[-450:]

    moving_average_20 = summation_index.rolling(window=20).mean()

    moving_average_20 = moving_average_20.iloc[-450:]

    egrid = (21, 29)
    fig = mpf.figure(style="ibd", figsize=(15, 9))
    ax1 = plt.subplot2grid(egrid, (1, 0), colspan=26, rowspan=16)

    configure_plot(ax1)

    ax1.plot(summation_index_last_450, label="$BRSI", linewidth=1.5)
    ax1.plot(moving_average_20, label="MA(20)", linestyle="-", linewidth=1.5)

    ax1.set_title("IBOV McClellan Summation Index (Ratio Adjusted) (EOD)")
    ax1.legend(loc="upper left")

    plt.savefig("market/$BRSI.png", bbox_inches="tight")


def plot_cumulative_net_new_highs(data):
    window = 252
    new_highs = data.rolling(window=window).max()
    new_lows = data.rolling(window=window).min()

    margin = 0.01
    new_highs_52wk = data >= new_highs * (1 - margin)
    new_lows_52wk = data <= new_lows * (1 + margin)

    net_new_highs = new_highs_52wk.sum(axis=1) - new_lows_52wk.sum(axis=1)

    cumulative_net_new_highs = net_new_highs.cumsum()

    sma_20 = cumulative_net_new_highs.rolling(window=20).mean()

    egrid = (21, 29)
    fig = mpf.figure(style="ibd", figsize=(15, 9))
    ax1 = plt.subplot2grid(egrid, (1, 0), colspan=26, rowspan=16)

    configure_plot(ax1)

    ax1.plot(cumulative_net_new_highs[-900:], label="$BRHL Cumulative", linewidth=1.5)
    ax1.plot(sma_20[-900:], label="MA(20)", linestyle="-", linewidth=1.5)

    ax1.set_title("IBOV Cumulative New Highs-New Lows (EOD)")
    ax1.legend(loc="upper left")

    plt.savefig("market/$BRHL.png", bbox_inches="tight")
