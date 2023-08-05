import pickle
import os

def main(gre_score,toefl_score,university_rating,sop,lor,cgpa,research):
    
    this_dir, this_filename = os.path.split(__file__)  # Get path of finalized.pickle
    data_path = os.path.join(this_dir, 'finalized_model2.pickle')
    loaded_model= pickle.load(open(data_path, 'rb'))
    #filename ='linreg_add2/finalized_model2.pickle'
    #loaded_model=pickle.load(open(filename,'rb'))
    prediction=loaded_model.predict([[gre_score,toefl_score,university_rating,sop,lor,cgpa,research]])
    print(prediction)
    return prediction