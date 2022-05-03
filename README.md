# Responsible AI (RAI) Toolkit - with great powers comes great responsibility

## What is RAI

RAI is a AI Governance framework.  With increased use of AI / ML in critical decision making process, RAI provides a objective index for measuring the risk of the model across the following dimensions:

- Privacy:  Differential Privacy of data used in model training exercise
- Interpretability:  Ability of the model to explain the prediction
- Data Bias: Class Imbalance of the data used to train the model
- Carbon Footprint: Carbon Emissions of the Model training / Inference

## How does it work

1.  Build the Model using framework of your choice.  
2.  Use any package to decipher RAI components.  For eg. Code Carbon for Carbon Emissions, FairTorch for Bias, SageMaker Clarify for Bias, Captum for Interpretibility of the Model etc...
4.  Import the SPECTRE package (Python package)
5.  Add the details of the SPECTRE components of your model to SPECTRE Framework
6.  SPECTRE calculates an Index (float) that denotes the health of the model.  Higher the number better the model

## Calculation

Responsible AI Index is a measure of the following and is a scale between 1 to 3.  3 being a Responsible Model

1. Carbon Emissions
2. Differential Privacy
3. Data Bias (Class Imbalance)
4. Interpretability

## Support

RAI1.0, the MVP of the RAI framework supports:

- Differential Privacy
- Interpretability
- Data Bias
- Carbon Footprint

You can add a bunch of Models for a specific use case to the RAI framework and RAI ranks them on the basis of its Responsible AI Index, which can be adjuted to user flexibility by adjusting it's weights or adding/deleting other open source libabries. 

![image](https://user-images.githubusercontent.com/7538839/160517464-a716c6d9-bbf3-4255-8710-d090e11abf1a.png)


## Pre-requisistes

1. Emission tracking is calcualted using [Code Carbon](https://codecarbon.io/).  Install Code Carbon using

>     !pip install codecarbon

2.Differential privacy is calculated usig [Opacus](https://opacus.ai/).  Install Opacus

>     !pip install opacus

3.Responsible index is calcualted using ResponsibleML.  Install ResponsibleML

>     !pip install -i https://test.pypi.org/simple/ spectre

## How it works

1. AI Governance SPECTRE is the overarching framework for responsible AI
2. SPECTRE is across 7 dimensions - Security, Privacy, Explainability, Trust, bias and Emissions
3. Current Framework support the above 4 for calculating RAI index
4. SPETRE has 
    a.  Model List (list of all models that you created for calculating RAI Index)
    b.  Models - every model created by you for the use case.

## Code sample

1. Import the package in your code

>     from aigovernance import spectre

2.Initiate a Model and a Model List

>     r_model = spectre.responsibleModel(modelname, modeltype)
>     model_list = spectre.models()

3. Bias Information - During data engineering phase of your ML life cycle, send the label data frame (Y) to responsibleModel

>     r_model.calcualte_bias(label_df)

4. Carbon Emissions - For calculating carbon emissions, before you start your model training, start the tracker.  Once the model training is complete, stop the tracker

>     r_model.track_emissions()
> 
>     << your model training>>
> 
>     r_model.stop_tracking()

5.  Model Interpretability - Ability of the model to be interpretable by the top 3 features by > 70%

>     r_model.intrepret(input_tensor, model,target_class)

6. Differential Privacy - 

>     priv_model, priv_opt, priv_datasetloader = r_model.privatize(dp_model, optimizer, train_dataloader, noise_multiplier, max_per_sample_grad_norm) 
>     r_model.calculate_privacy_score(delta=1e-5)

7. Responsible Index:  You can now retrieve the responsible index of the model using

>     responsible_index = r_model.rai_index()

8. Given the nature of ML, you will be building multiple models.  Use steps 2 to 7 initiate the model with responsible dimension.  You can now add the models you created on to a model list

>     model_list.add_model(r_model)

9. You can list all the models and their responsible score using 

>     model_list.list_models()

10. finally, to identify the most responsible model that you can use for your production use case, you can get the models ranked by their responsibility index
> 
>     model_list.rank_models()
