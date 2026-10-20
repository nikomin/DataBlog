# [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), Niko Komin, June 2025

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime
import tabulate
import matplotlib.ticker as ticker

titleFontsize = 20

######################################################################
#
# Plot functions
#
######################################################################
def plotMembers(title, yAxisLabel, data, party_names, party_colors, figsize=(12,4)):
    """Plots every member's age sorted by party affiliation."""
    sns.set_style("darkgrid")
    fig, ax = plt.subplots(figsize=figsize)
    sns.stripplot(x="Party", y="age",
                  data=data,
                  hue="Party", hue_order=party_names, palette=sns.color_palette(party_colors.values()),
                  order=party_names)
    ax.set_ylim(0,90) # show same age range as our "generations" later on.
    ax.yaxis.set_major_locator(ticker.MultipleLocator(15)) # tick age labels every 15 years

    # axis labels and title
    plt.xlabel('')
    plt.ylabel(yAxisLabel)
    plt.suptitle(title , fontsize=titleFontsize-8)
    plt.show()


def plotHistoryComparison(popHist,
                          histogram, bins,
                          title, color, position, ax, showpop=True):
    """Plot histogram, optionally on top of the `popHist`."""
    ylabels = bins[:-1]
    ylabelsWords = ['Gen Alpha', 'Gen Z', 'Millenials', 'Gen X', 'Baby Boomer', 'Stumme Generation','Größte Generation']
    ylabelPositions = np.arange(len(ylabels))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    if showpop:
        # general population
        ax.barh(ylabelPositions, -popHist, color='lightgrey')
        ax.barh(ylabelPositions, popHist, color='lightgrey')
    # party
    ax.barh(ylabelPositions, -histogram, color=color,alpha=0.5, label=title)
    ax.barh(ylabelPositions, histogram, color=color,alpha=0.5)

    # title and labels
    ax.set_title(f'{title}')
    ax.set_xlabel("")
    ax.tick_params(bottom=False)
    ax.set_xticklabels([])
    ax.set_xlim([-65,65])
    
    # put y-axis labels only left of the first and right of the last chart
    ax.set_yticks(ylabelPositions)
    ax.tick_params(left=False, right=False)
    if position=='first':
        ax.set_ylabel("Altersgruppe")
        ax.set_yticklabels([f"{a}–{a+ bins[1]-bins[0] - 1}" for a in ylabels])
    elif position=='last':
        ax.yaxis.tick_right()
        ax.tick_params(right=False)
        ax.set_yticklabels(ylabelsWords)
    else:
        ax.set_yticklabels([])#ylabels)
        
    # write percentage in the middle
    for cohort in ylabelPositions:
        cohortPercentage = np.round(histogram[cohort])
        annotation = str(int(cohortPercentage))+"%" if cohortPercentage > 0 else ""
        ax.annotate(annotation,(0,cohort),
                    ha="center",va="center",fontweight="bold",color="black",size="large")



def plotRowOfHistogramComparisons(keyOfBackground,
                                  keysToPlot,
                                  histograms,
                                  bins,
                                  colors,
                                  title,
                                  figsize=(19,3)):
    """Plots a row of histograms with the first histogram repeated in grey in the background of all histograms."""
    numberCols = len(keysToPlot)

    plt.style.use('default')
    fig, axs = plt.subplots(nrows=1, ncols=numberCols, figsize=figsize)
    fig.suptitle(title, fontsize=titleFontsize)

    figNo = 0

    # write labels on the outside only
    for key in keysToPlot:
        if figNo==0:
            position='first'
            compare=False
        elif figNo==numberCols-1:
            position='last'
            compare=True
        else:
            position=None
            compare=True

        plotHistoryComparison(histograms[keyOfBackground],histograms[key], bins, key,
                              colors[key],position, axs[figNo], showpop=compare)
        figNo = figNo + 1

    plt.tight_layout()
    
def violinplotsOfFractions(data,order,colors,title,figsize=(10, 6)):
    """Plots violinplots of all fractions in a given order overlain with the quantiles."""
    fig, ax = plt.subplots(figsize=figsize)
    sns.violinplot(
        data=data,
        x="Party",
        y="age",
        order=order,
        hue="Party",
        palette=colors,
        legend=False,
        inner=None,
        ax=ax
    )

    quantiles = data.groupby("Party")["age"].quantile(
        [0.25, 0.50, 0.75]
    ).unstack()
        
    quantiles.dropna(inplace=True)

    for q, label in [
        (0.25, "25th percentile"),
        (0.50, "Median"),
        (0.75, "75th percentile")
    ]:
        ax.plot(
            range(len(order)),
            [quantiles.loc[p, q] for p in order],
            marker="o",
            linestyle="-",
            color={"25th percentile": "gray",
                   "Median": "black",
                   "75th percentile": "dimgray"}[label],
            label=label
        )

    ax.set_xlabel("Partei")
    ax.set_ylabel("Alter")
    ax.legend()
    ax.set_title(title)
    plt.tight_layout()
