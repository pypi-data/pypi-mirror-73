import pickle

def main(gre_score,toefl_score,university_rating,sop,lor,cgpa,research):
    filename ='finalized_model2.pickle'
    loaded_model=pickle.load(open(filename,'rb'))
    prediction=loaded_model.predict([[gre_score,toefl_score,university_rating,sop,lor,cgpa,research]])
    print(prediction)
    return prediction