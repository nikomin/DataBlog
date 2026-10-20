# Age groups and representation

Collection of exercises on webscraping, text parsing, data analysis and visualisation.

## 1. Age structure of the German Parliament


*June 2025*

- Jupyter notebook report: [Gen X macht in Deutschland Politik.ipynb](https://github.com/nikomin/agegroupsAndRepresentation/blob/main/01-Gen-X-im-Deutschen-Bundestag/Gen%20X%20macht%20die%20Politik.ipynb)
- [official website of the Bundestag](https://www.bundestag.de/abgeordnete) lists all current members with name, party membership, and a link to a page a respective biography
- biographies are texts in free form given by the member
- biographies contain the year of birth, most in the form "Geboren am XX. MONTH YEAR in PLACE"
- scraped data in May 2025.
- population data by "Statistisches Bundesamt" (data [here](https://service.destatis.de/bevoelkerungspyramide/))
- values for 2022 and later are predicted,
- we will use the entries from 2021, which are stored in row `142`(male) and `143` (female).

## 2. Age structure of US congress before 2026-midterms


*October 2026*

- folder `02-age\ groups\ in\ US\ chambers`
- Jupyter notebook report: [Amerika ist jünger als Deutschland, seine Volksvertreter sind älter](https://github.com/nikomin/agegroupsAndRepresentation/blob/main/02-age%20groups%20in%20US%20chambers/Amerika%20ist%20j%C3%BCnger%20als%20Deutschland%2C%20seine%20Volksvertreter%20sind%20%C3%A4lter.ipynb)
- data for reproduction in sub-folder `02-age groups in US chambers/data`
- data sources, preparation, and analysis in `01-dataPrep.ipynb` and `02-analysis.ipynb`


---

*[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), Niko Komin, June 2025*
