# [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), Niko Komin, June 2025

import pandas as pd
import numpy as np

######################################################################
#
# Global variables
# 
######################################################################


titleFontsize = 20

pop_US = pd.read_csv("data/USdemographics2025.csv")

population_de_raw = pd.read_csv("../01-Gen-X-im-Deutschen-Bundestag/15_bevoelkerungsvorausberechnung_daten.csv",
                                sep=";")

members_HoR = pd.read_csv("data/HouseOfReps.csv")

members_senate = pd.read_csv("data/HouseOfSenate.csv")
# conflating Dems and Dems(DFL)
members_senate.Party = members_senate.Party.replace('Democratic (DFL)[q]', 'Democratic')

members_congress = pd.concat([members_HoR[["Party","age"]],members_senate[["Party","age"]]])
members_congress.reset_index(inplace=True)



# party colors and names
# we're not gonna consider 'vacant' seats
party_colors = {'Democratic':'#0044c9',
                'Republican':'#e81b23',
                'Independent':'#949494'}

# colors for other groups
other_colors = {'Population':'#ffcc3c',
                'Population USA':'#d0a020',   
                'Population DE':'#ffcc3c',                
                'Senate':'#002768',
                'Representatives':'#002768',
                'Congress':'#002768',
                "Bundestag":'#B7958B',
                'Vacant':'#949494'}
party_colors_de = {'AfD':'#00A2DE',
                   'CDU/CSU':'#151518',                
                'SPD':'#e3000f',
                'Bündnis 90/Die Grünen' : '#409A3C',
                'Die Linke':'#be3075',
                'fraktionslos':'#949494'}

colors = party_colors | other_colors | party_colors_de

# bin width of 15 years is about one "generation" 
# (roughly silent gen, boomer, genX, millenials, genZ, genAlpha)
binWidth = 15
maxAge = 106

bins = np.arange(0,maxAge,binWidth) # age bins

# histogram of US population
popHist, popBins = np.histogram(pop_US.age,bins=bins,weights=pop_US.population)
popHist = popHist/popHist.sum() * 100 # normalizing

# auxiliary function for normalized histograms of chambers
def calcHistByChamber( chamber, data, bins, parties ):
    partyHists = {}
    partyBins = {}
    partyHists[chamber], partyBins[chamber] = np.histogram(data.age,bins=bins)
    partyHists[chamber] = partyHists[chamber]/partyHists[chamber].sum() * 100 # normalizing
    for party in parties:
        masked = data[ data.Party==party ]
        partyHists[party], partyBins[party] = np.histogram(masked["age"],bins=bins)
        partyHists[party] = partyHists[party]/partyHists[party].sum() * 100 # normalizing
    return partyHists


party_names_us = list(party_colors.keys())
party_names_de = list(party_colors_de.keys())


hor_byParty = calcHistByChamber( "Representatives", members_HoR, popBins, party_names_us )
sen_byParty = calcHistByChamber( "Senate", members_senate, popBins, party_names_us )
con_byParty = calcHistByChamber( "Congress", members_congress, popBins, party_names_us )

pop_DE = pd.DataFrame([population_de_raw.iloc[142],
                       population_de_raw.iloc[143]]).transpose().iloc[4:].reset_index()
pop_DE["age"] = np.arange(100)
pop_DE["population"] = pop_DE[142] + pop_DE[143] # sum of males and females
pop_DE.drop(["index",142,143],axis=1,inplace=True)

popHist_DE, popBins_DE = np.histogram(pop_DE.age,bins=bins,weights=pop_DE.population)
popHist_DE = popHist_DE/popHist_DE.sum() * 100 # normalizing

# histogram of Bundestag
members_Bundestag = pd.read_csv("../01-Gen-X-im-Deutschen-Bundestag/members_party_DOB.csv")
members_Bundestag["age"]=2026-members_Bundestag["DOB year"]


bun_byParty = calcHistByChamber( "Bundestag", members_Bundestag, popBins, party_names_de )

histograms_con = {"Population DE":popHist_DE,"Population USA":popHist}|con_byParty
histograms_sen = {"Population DE":popHist_DE,"Population USA":popHist}|sen_byParty
histograms_hor = {"Population DE":popHist_DE,"Population USA":popHist}|hor_byParty
histograms_bun = {"Population DE":popHist_DE,"Population USA":popHist}|bun_byParty
