[![License](https://img.shields.io/github/license/ie3-institute/mobility_viz)](https://github.com/ie3-institute/mobility_viz/blob/main/LICENSE)

# Visualization of mobility results

Within the research project [NOVAgent](https://ie3.etit.tu-dortmund.de/research/third-party-projects/distribution-grid-planning-operation/novagent-efre/) - funded by the European Fund for Regional Development - the [ie3 institute](https://ie3.etit.tu-dortmund.de/) and its partners assess the impact of individual mobility onto the distribution grid loading.
This repository provides means to assess and visualize the obtained results with regard to individual mobility.

This repository is quite "draft-like" and not intended for ongoing support.

## Remarks
- Input data is assumed to be provided via PostgreSQL database.
- Uses Selenium to convert html pages to png. Thus, requires [Geckodriver](https://github.com/mozilla/geckodriver/releases/) to be in path.