# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 19:42:53 2015

@author: morpheus
"""

import csv
import os
import re
import nltk
import string

#def XtractIngredients (path):
#    lines = open(path).read().split('\n')
#    lines=[x.lower() for x in lines]
#    ind=lines.index('ingredients')
#    ingredients=lines[(ind+1):-4]
#    ingredients=filter(None,ingredients)
#    ingredients=[re.sub("\(.*\)","",x) for x in ingredients]
#    ingredients=[re.sub(" +"," ",x) for x in ingredients]
#    return ingredients
#
def XtractIngredients():
    
    mypath = os.path.dirname(os.path.abspath(__file__))
    fulltext = os.path.join(mypath, "../AllRecipesData/fulltext/")
    csvpath=os.path.join(mypath,'csv_data/ingredients.csv')
    recipes=[]
    for path, subdirs, files in os.walk('/home/morpheus/Documents/Python Projects/NLP 1 Project/recipe_generation/../AllRecipesData/fulltext/'):
        for name in files:
            if name!='.DS_Store': #Was there in the dataset. Better remove it than havet the parser traverse through it (even though it won't find any matches)
                tmp=os.path.join(path, name)
                recipes.append(tmp)
    
    ingrWrite=open(csvpath,'w')
    Ingr=csv.writer(ingrWrite)
    
    FullIngredients=[]
    
    for path in recipes:
        lines = open(path).read().split('\n')
        lines=[x.lower() for x in lines]
        ind=lines.index('ingredients')
        ingredients=lines[(ind+1):-4]
        ingredients=[x.translate(None, string.punctuation) for x in ingredients]
        ingredients=filter(None,ingredients)
        ingredients=[re.sub("\(.*\)","",x) for x in ingredients]
        ingredients=[re.sub(" +"," ",x) for x in ingredients]
        #Insert writing function
        #Modifications from here. Delete for reverting:
    
        ingredients=[nltk.word_tokenize(sentence) for sentence in ingredients]
        FullIngredients.append(ingredients)
        ingredients=[]
    
    #Should improve using list comphrehension
    IngredientSet=set(FullIngredients[0][0])
    for x in range(len(FullIngredients)):
        for y in range(1,len(FullIngredients[x])):
            tmp=set(FullIngredients[x][y])
            IngredientSet=IngredientSet|tmp
    
    IngredientList=list(IngredientSet)
    IngredientList=[x for x in IngredientList if x[0].isdigit()==False]
    return IngredientList