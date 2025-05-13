# PyPort Jupyter Notebooks

This directory contains Jupyter notebooks demonstrating how to use the PyPort library for interacting with the Port API.

## Available Notebooks

1. **[01_Basic_Usage.ipynb](01_Basic_Usage.ipynb)**: Basic usage of the PyPort library
   - Initializing the client
   - Getting blueprints and their details
   - Getting entities and their details
   - Getting actions
   - Visualizing entity distribution across blueprints

2. **[02_Blueprint_and_Entity_Management.ipynb](02_Blueprint_and_Entity_Management.ipynb)**: Blueprint and entity management
   - Creating blueprints with properties and required fields
   - Creating entities based on blueprints
   - Getting and displaying entities
   - Updating entities
   - Searching for entities
   - Visualizing entity data
   - Deleting entities and blueprints

3. **[03_Advanced_Operations_and_Utilities.ipynb](03_Advanced_Operations_and_Utilities.ipynb)**: Advanced operations and utilities
   - Using utility functions (snapshots, clearing blueprints)
   - Advanced search operations with complex queries
   - Error handling and retry configuration

## Running the Notebooks

### Prerequisites

1. **Python Environment**: Make sure you have Python 3.6+ installed.
2. **Jupyter**: Install Jupyter Notebook or JupyterLab:
   ```bash
   pip install jupyter
   ```
3. **PyPort**: Install the PyPort library:
   ```bash
   pip install pyport
   ```
4. **Additional Dependencies**: Install additional dependencies for visualization:
   ```bash
   pip install pandas matplotlib
   ```

### Setting Up API Credentials

Before running the notebooks, you need to set up your Port API credentials. You can do this in two ways:

1. **Environment Variables** (recommended):
   ```bash
   export PORT_CLIENT_ID=your-client-id
   export PORT_CLIENT_SECRET=your-client-secret
   ```

2. **Directly in the Notebook** (not recommended for shared notebooks):
   ```python
   client_id = "your-client-id"
   client_secret = "your-client-secret"
   ```

### Starting Jupyter

Start Jupyter Notebook or JupyterLab:

```bash
# For Jupyter Notebook
jupyter notebook

# For JupyterLab
jupyter lab
```

Then navigate to the notebooks directory and open the desired notebook.

## Notes

- These notebooks create test resources in your Port instance. They attempt to clean up these resources at the end, but if a notebook execution is interrupted, some resources might remain.
- Be careful when running these notebooks in a production environment, as they may modify your Port data.
- The notebooks include visualizations that help understand the data structure and relationships in your Port instance.
