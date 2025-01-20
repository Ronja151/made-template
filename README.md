# The impact of Amazon deforestation on Brazil’s carbon footprint
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.12-orange)
<div style="overflow: auto;">
  <img src="https://images.unsplash.com/photo-1622541076378-2c98c5d7ab64?q=80&w=2264&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" align="right" width="300" style="margin: 15px;">
  The relevance of forests for reducing climate change
 is significant, as they act as carbon reservoirs and
 absorb CO2 from the atmosphere. Tropical rainforests
 in particular, such as the Amazon, are highly effective
 and can absorb significantly more CO2 than native
 forests. The Amazon is the largest tropical rainforest
 in the world and plays a central role in the global
 carbon cycle. Around 60 % of the Amazon region is
 located in Brazil, making the country a key player in
 the fight against climate change. At the same time,
 the Amazon is massively threatened by deforestation
 and degradation, which has a significant impact on
 the global carbon footprint.
 The aim of this project is to analyse the impact of
 deforestation in the Amazon region on Brazilian CO2
 emissions. To this end, deforestation and emissions
 data from 2004 to 2019 will be analysed to determine
 the correlation between the destruction of rainforest
 areas and the increase in CO2 emissions from land
 use change. The aim of this analysis is to illustrate the
 central importance of the Amazon region for global
 climate stability and to emphasise the relevance of
 its protection.
</div>
 

 ## Question
 How does the deforestation of the Amazon rainforest
 affect CO2 emissions in Brazil?

 ## Datasources

<!-- Describe each datasources you plan to use in a section. Use the prefic "DatasourceX" where X is the id of the datasource. -->

### Datasource1: Brazilian Amazon Rainforest Degradation
* Metadata URL: https://www.kaggle.com/datasets/mbogernetto/brazilian-amazon-rainforest-degradation
* Data URL: https://www.kaggle.com/datasets/mbogernetto/brazilian-amazon-rainforest-degradation?select=def_area_2004_2019.csv
* Data Type: CSV

The dataset contains the deforestation area (km²) by year and state of the Amazon rainforest in Brazil, from 2004 to 2019. 

### Datasource2: CO₂ and Greenhouse Gas Emissions
* Metadata URL: https://github.com/owid/co2-data/blob/master/README.md
* Data URL: https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv
* Data Type: CSV

The dataset contains CO₂ emissions data worldwide and by country, including emissions from various sectors such as land use, from 1751 to 2022.

## Project Work
Your data engineering project will run alongside lectures during the semester. We will ask you to regularly submit project work as milestones, so you can reasonably pace your work. All project work submissions **must** be placed in the `project` folder.

### Exporting a Jupyter Notebook
Jupyter Notebooks can be exported using `nbconvert` (`pip install nbconvert`). For example, to export the example notebook to HTML: `jupyter nbconvert --to html examples/final-report-example.ipynb --embed-images --output final-report.html`


## Exercises
During the semester you will need to complete exercises using [Jayvee](https://github.com/jvalue/jayvee). You **must** place your submission in the `exercises` folder in your repository and name them according to their number from one to five: `exercise<number from 1-5>.jv`.

In regular intervals, exercises will be given as homework to complete during the semester. Details and deadlines will be discussed in the lecture, also see the [course schedule](https://made.uni1.de/).

### Exercise Feedback
We provide automated exercise feedback using a GitHub action (that is defined in `.github/workflows/exercise-feedback.yml`). 

To view your exercise feedback, navigate to Actions → Exercise Feedback in your repository.

The exercise feedback is executed whenever you make a change in files in the `exercise` folder and push your local changes to the repository on GitHub. To see the feedback, open the latest GitHub Action run, open the `exercise-feedback` job and `Exercise Feedback` step. You should see command line output that contains output like this:

```sh
Found exercises/exercise1.jv, executing model...
Found output file airports.sqlite, grading...
Grading Exercise 1
	Overall points 17 of 17
	---
	By category:
		Shape: 4 of 4
		Types: 13 of 13
```
