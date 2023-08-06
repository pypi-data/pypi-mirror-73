## Introduction

+ This is an Open-Source Project intended to aid the developers in the Healthcare Industry.
+ This package helps you to get country-wise covid data which contains 15 important fields for statistical analysis.
+ With increased severity of COVID-19, data plays a very critical role in determining the trend and patterns.
+ The data is live and get updated every now and then. 

## How To Use

+ Import using `from wcovid19.wcd import WorldCovidData as wcd`
+ Get ICD Code's Description using : 

```
wcd.getCovidData("Mexico")
wcd.getCovidData("Dominican Republic")
wcd.getCovidData("Saint Pierre Miquelon")
```

+ Finally, it looks like this :

```
from wcovid19.wcd import WorldCovidData as wcd
wcd.getCovidData("<Country_Name>")
```

+ Returns a Map of the above mentioned fields.

> Note : All the imports/dependencies are automatically installed.

## Bugs & Issues

+ If you find a Bug or have an Idea, please feel free to drop a mail @ sakethaux1111@gmail.com!
