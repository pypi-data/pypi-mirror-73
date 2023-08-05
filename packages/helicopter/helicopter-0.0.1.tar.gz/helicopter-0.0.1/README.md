# helicopter

Yes this is a Python package but it was inspired by the Helicopter Julia Challenge created by Chris Rackausckas of the SciML group at MIT. In that challenge
contestants are provided incomplete data from a helicopter and asked to infer the latent dynamics. 

## Background information 


- Video of the helicopter https://www.youtube.com/watch?v=2g1-sDZ3BVw
- Home page of challenge https://github.com/SciML/HelicopterSciML.jl
- Chris will be teaching how to do automated discovery of missing physical equations from a first principle model at at workshop on July 26th, 2020. Sign up for JuliaCon at https://juliacon.org/2020/

The goal of the Julia challenge is to utilize automated tools to discover a physcially-explainable model that accurately predicts the dynamics of the system.

## Raw data 

You can pull into pandas with: 
    
    data = pd.read_csv('https://raw.githubusercontent.com/SciML/HelicopterSciML.jl/master/data/Lab-Helicopter_Experimental-data.csv')
    
## Why this package? 

Purpose:

- To include the time series of helicopter data at www.microprediction.org as a test of how well time series algorithms perform. 
- To force me to write a Julia client for www.microprediction.org and learn some Julia 



