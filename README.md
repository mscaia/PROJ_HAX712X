<h1 align="center">CycleVision3</h1>

## 🌐 Project Website  
Visit our interactive site for visualizations and insights: [CycleVision3 - Interactive Bike Traffic Analysis](https://mscaia.github.io/PROJ_HAX712X/)

## 📖 Project Overview 
This project aims to analyze bike traffic in Montpellier, focusing on the investigation of bike-sharing rides and cyclist/pedestrian counts. We will leverage various datasets to visualize and predict bike traffic patterns, creating an interactive website to showcase our findings.

## 👥 Autors list

- [**ARMAND Charlotte**](https://github.com/CharlotteARMAND)
- [**CONDAMY Fabian**](https://github.com/FabianCondamy)
- [**SCAIA Matteo**](https://github.com/mscaia)
- [**STETSUN Kateryna**](https://github.com/KatyaStetsun)

## 🚀 Getting Started  

Before beginning development and data analysis, you need to set up the working environment by installing all necessary dependencies. Follow these steps to quickly set up and run the project:

### 1. **Clone the Repository**  
First, clone the project repository:  
```bash
git clone https://github.com/mscaia/PROJ_HAX712X.git
cd PROJ_HAX712X
```

### 2. **Set Up the Environment**  
Create and activate a virtual environment:  
```bash
conda create --name Cycle3 python=3.9.18
conda activate Cycle3
pip install -r requirements.txt
```

### 3. **Run the Scripts**  
Example commands to use the project features:  
- **Download Data**:  
  ```bash
  python ./src/donnée.py
  ```  
- **View Data Analysis Results**:  
  ```bash
  python ./Cycle3/analyse_donnee/statistique.py
  ```  
- **Visualize Maps**:  
  ```bash
  python ./Cycle3/map/carte.py
  ```  

For more details on visualization and advanced usage, refer to the [full documentation](https://mscaia.github.io/PROJ_HAX712X/docu.html#guide-de-lutilisateur).

## 🛠️ Code Snippet to Build the Website

Here are the steps to set up and deploy a Quarto-based website like the one we've created:

### 1. **Install Quarto**

Download and install Quarto from [quarto.org/download](https://quarto.org/download). Ensure that Quarto is added to your system's environment variables.

### 2. **Create a New Project**

Open your terminal and execute the following commands:

```bash
mkdir docs
cd docs
quarto create-project project_name --type website
```

### 3. **Add Content**

- Place `.qmd` files in the `docs/` folder to enrich your website's content.  
- Edit the `_quarto.yml` file to customize the site's structure and settings.

### 4. **Local Preview**

To preview the site locally, run the following command in the `./docs/` directory:

```bash
quarto preview
```

### 5. **Deploy to GitHub Pages**

1. Go to the **GitHub Pages** section in your repository's settings.  
2. Under the **Build and Deployment** settings, select *Deploy from a branch*.  
3. Choose the `main` branch and the `/docs` folder as the source.  

Next, in the `./docs/` directory, run:

```bash
quarto render
```

Your site will be deployed on the next push to the `main` branch.

## 🔒 License

This project is licensed under the terms specified in the file [LICENCE](https://github.com/mscaia/PROJ_HAX712X/blob/main/LICENCE). Please refer to the file for more details.
