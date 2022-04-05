import json
import os
import pandas as pd
import numpy as np
from codecarbon import EmissionsTracker as ET
#from opacus import PrivacyEngine 

class responsibleModel:
    
    __modelname__ = ""
    __modeltype__ = ""
    __emissions__ = 0.0
    __bias__ = 0.0
    __explained__ = False
    __epsilon__ = 0.0
    __tracker__ = ET(project_name = "",
            measure_power_secs = 15,
            save_to_file = False)
    
    def __init__(self,):
        self.__modelname__ = ""
        self.__modeltype__ = ""
        self.__emissions__ = 0.0
        self.__bias__ = 0.0
        self.__explained__ = False
        self.__epsilon__ = 0.0
        
        __tracker__ = ET(project_name = "",
            measure_power_secs = 15,
            save_to_file = False)

    def __init__(self, 
                 modelname: str,
                 modeltype:str,
                 explained:bool = False,
                 emissions:float = 0.0,
                 bias:float= 0.0,
                 epsilon:float = 0.0):
        
        self.__modelname__ = modelname
        self.__modeltype__ = modeltype
        self.__emissions__ = emissions
        self.__bias__ = bias
        self.__explained__ = explained
        self.__epsilon__ = epsilon
    
        __tracker__ = ET(project_name = modelname,
            measure_power_secs = 15,
            save_to_file = False)
    
    def explained(self, isexplained: bool):
        self.__explained__ = isexplained

    def emissions(self, carbon_emissions: float):
        self.__emissions__ = carbon_emissions

    def bias(self, label_bias: float):
        self.__bias__ = label_bias

    def epsilon(self, privacy_epsilon: bool):
        self.__epsilon__ = privacy_epsilon

    def model(self, modeltype: str):
        self.__modeltype__ = modeltype
        
    def __calculate_emissions_index(self):

        print(self.__emissions__)

        if self.__emissions__ <= 500:
            emissionIndex = 3
        elif self.__emissions__ > 500 and self.__emissions__ <= 10000:
            emissionIndex = 2
        else:
            emissionIndex = 1

        return emissionIndex

    def __calculate_privacy_index(self):
        if self.__epsilon__ <= 1:
            privacyIndex = 3
        elif self.__epsilon__ > 1 and self.__epsilon__ <= 10:
            privacyIndex = 2
        else:
            privacyIndex = 1

        return privacyIndex

    def __calculate_explainability_index(self):

        expIndex = 1

        if self.__modeltype__ == "deeplearning":
            return expIndex

        if self.__explained__ == True:
            expIndex = 3
        else:
            expIndex = 2

        return expIndex

    def __calculate_bias_index(self):
        if self.__bias__ <= 0.25 and self.__bias__ >= -0.25:
            bindex = 3
        elif self.__bias__ > 0.5 or self.__bias__ < -0.5:
            bindex = 1
        else:
            bindex = 2

        return bindex
    
    def describe(self):
        return json.dumps(self.__dict__)
    
    def model_rai_components(self):
        
        emission_index = self.__calculate_emissions_index()
        privacy_index = self.__calculate_privacy_index()
        bias_index = self.__calculate_bias_index()
        explain_index = self.__calculate_explainability_index()
        RAI_index = self.rai_index()
        
        value = json.dumps({"model name": self.__modelname__,
                            "model type": self.__modeltype__,
                            "rai index": RAI_index,
                            "emissions": emission_index,
                            "privacy": privacy_index,
                            "bias": bias_index,
                            "explainability": explain_index})

        return value
        
    def rai_index(self):
    
        index = 0.0
        weights = 0.2

        emission_index = self.__calculate_emissions_index()
        privacy_index = self.__calculate_privacy_index()
        bias_index = self.__calculate_bias_index()
        explain_index = self.__calculate_explainability_index()

        print(emission_index)
        print(privacy_index)
        print(bias_index)
        print(explain_index)

        index = weights * (emission_index + privacy_index + bias_index + explain_index)

        return index

    def track_emissions(self):
        # Calculate Emissions
        self.__tracker__.start()
        
    def stop_tracking(self):
        self.__emissions__ =  self.__tracker__.stop()
        
    def calculate_bias(self, df_label: str):
        
        # Get the number of classes & samples
        label_classes = df_label.value_counts(ascending=True)
        totalvalues = label_classes.sum()
        min_class_count = label_classes.values[1]
        
        #calcualte the bias
        class_balance = min_class_count / totalvalues
        if class_balance >= 0.4:
            self.__bias__ = 3
        elif class_balance > 0.2 and class_balance < 0.4:
            self.__bias__ = 2
        else:
            self.__bias__ = 1
                
class models:
    model_list = []
    
    def __init__(self):
        self.model_list = []
    
    def add_model(self, modelname, modeltype, explained, emissions, bias, epsilon):
        model = responsibleModel(modelname, modeltype, explained, emissions, bias, epsilon)
        self.model_list.append(model)
        
    def add_model(self, model):
        self.model_list.append(model)
        
    def remove_model(self, modelname):
        self.model_list.remove(modelname)
        
    def list_models(self):
        model_json = ""
        for model in self.model_list:
            model_json += model.describe() 
            if model != self.model_list[-1]:
                model_json += ","
                                
            model_json += "\n"
            
        model_json = "[" + model_json + "]"
        
        return model_json
    
    def get_model(self, modelname):
        for model in self.model_list:
            if model.__modelname__ == modelname:
                return model
        return None
    
    def rank_models(self, rank_type = None):
        sorted_json = ""
        sorted_models = sorted(self.model_list, key=lambda x: x.model_rai_index(), reverse=True)
        for model in sorted_models:
            sorted_json += model.model_rai_components()
            if(model != sorted_models[-1]):
                sorted_json += ","
            sorted_json += "\n"
            
        sorted_json = "[" + sorted_json + "]"
        return sorted_json