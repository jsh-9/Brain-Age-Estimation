<div id="top"></div>

<br />
<div align="center">

<h3 align="center">ECNN</h3>

  <p align="center">
    Brain Age Estimation based on Brain MRI by Ensemble of Deep Networks
  </p>
</div>


<!-- ABOUT THE PROJECT -->
## About The Project

Here is an implementation of ECNN model for the estimation brain age  based on MRI images. 
For more detail about the project please use [this link](https://ieeexplore.ieee.org/document/9377399) to access the paper.
![Piplines](./image/ECNN.png?raw=true "Title")

## Requirement installation
```sh
conda env create -f environment.yml
```
## Dataset
To train the proposed CNN networks, the Brain-Age Healthy Control (BAHC) dataset was used. This dataset contains 2001 Healthy individuals with a male/female ratio of 1016/985 with an average age of 18.12 ± 36.95 years. The age range of participants in this dataset is from 18 to 90 years. 

## Preprocessing 
All T1-weighted MRI scans were preprocessed using the Statistical Parametric Mapping (SPM12) software package. First, all scans are segmented into gray matter (GM) and white matter (WM) and then normalized to the Montreal Neurological Institute 152 (MNI152) space using the DARTEL algorithm. DARTEL algorithm with parameter value of 1.5 mm3 has been used for data resampling and 4 mm3 has been used for smoothing.

## Train the model

* Run augement.py file for augment training data
* Run ECNN_Train.py for train models

## Test the model

* Run ECNN_test.py for test models




