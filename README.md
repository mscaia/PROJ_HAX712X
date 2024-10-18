# CycleVision3 - PROJ_HAX712X: Bikes and Bike-Sharing in Montpellier

## Project Overview
This project aims to analyze bike traffic in Montpellier, focusing on the investigation of bike-sharing rides and cyclist/pedestrian counts. We will leverage various datasets to visualize and predict bike traffic patterns, creating an interactive website to showcase our findings.

## Objectives
- Analyze bike traffic through various datasets, including:
  - **VéloMagg**: Bike-sharing rides from Montpellier Méditerranée Métropole.
  - **Cyclist and Pedestrian Counting**: Data from bike and pedestrian counters.
  - **Open Street Map Data**: Geographic data for visualization.

- Create interactive visualizations, including:
  - An interactive traffic map predicting the next day's bike traffic.
  - Visual representations of bike traffic over different time periods (last month, last year, all years).

## Team Members

We are a group of four working collaboratively on this project. Here is the list of our team members:

1. **ARMAND Charlotte** - Graph, Map, (Vidéo)
2. **CONDAMY Fabian** - Site WEB
3. **SCAIA Matteo** - Map, Graphs, (Vidéo)
4. **STETSUN Kateryna** - Testing, Documentation

## Gantt diagram
```mermaid
gantt
    title Group Project Retro Planning
    dateFormat  YYYY-MM-DD
    axisFormat  %d-%m
    excludes weekends

    section Getting Started
    Brainstorming : done, 2024-09-27, 7d
    Creating GitHub enviroment : crit, 2024-09-27, 1d
    Task Distribution : done, 2024-10-06, 3d
    Initial Research :active, 2024-10-09, 7d
    Datasets loading : done, 2024-10-11, 2d
    Documentation Draft : active, 2024-10-15, 5d

    Mid-term Snapshot :milestone, 2024-10-25, 1d

    section Critical Tasks
    Data Gathering & Processing :2024-10-28, 7d
    Code Structure Design :2024-11-02, 4d
    Interactive Map Feature :2024-11-06, 10d
    Traffic Prediction Algorithm :2024-11-16, 7d
    Backend Integration :2024-11-23, 7d

    section Documentation
    Docstrings :2024-11-30, 5d
    API Documentation :2024-12-05, 3d
    README Preparation :2024-12-08, 2d

    section Testing
    Unit Tests :2024-11-25, 5d
    Continuous Integration Setup :2024-11-30, 3d
    Full Testing :2024-12-03, 4d

    section Delivery
    Finalize GitHub Repo :2024-12-09, 1d
    Slide Deck Prep :2024-12-09, 2d
    Presentation Rehearsal :2024-12-12, 1d
    Oral Presentation :milestone, 2024-12-13, 1d


## Project Structure
PROJ_HAX712X/
│
├── my_module_name/             # Main code directory
│   ├── __init__.py             # Module initializer
│   ├── main.py                  # Main script
│   └── ...                      # Other Python modules
│
├── slides/                      # Directory for presentation slides
│   ├── presentation.qmd         # Quarto presentation
│
├── roadmap/                     # Directory for project planning
│   ├── README.qmd               # Project outline and planning details
│
├── .gitignore                   # Git ignore file
├── README.md                    # Project README
└── requirements.txt             # Python dependencies

## Datasets
- **Bike-sharing rides**: [https://data.montpellier3m.fr/dataset/courses-des-velos-velomagg-de-montpellier-mediterranee-metropole]
- **Cyclist and pedestrian counting**: [https://data.montpellier3m.fr/dataset/comptages-velo-et-pieton-issus-des-compteurs-de-velo]
- **Open Street Map**: [https://www.openstreetmap.org/]

## Technologies Used
- **Programming Language**: Python
- **Frameworks/Libraries**: [Pandas, Matplotlib, Folium ....]
- **Documentation**: Sphinx/Quarto for documentation and website generation.

## Getting Started
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/mscaia/PROJ_HAX712X.git
   cd PROJ_HAX712X
