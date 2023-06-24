import pandas as pd
from initial_data_loader import get_initial_load


def get_dataframes(car_parameters_autoscout24, car_parameters_otomoto):
    """
    This function is converting the information taken from the initial_load function into dataframes, to make them ready
    for the EDA.
    :param car_parameters_autoscout24: return from initial_load function (list of jsons).
    :param car_parameters_otomoto: return from initial_load function (list of dictionaries).
    :return: Two dataframes: 1) cars from autoscout, 2) cars from otomoto.
    """
    df_scout = pd.DataFrame()
    for par in car_parameters_autoscout24:
        offer = pd.json_normalize(par,
                                  meta=[
                                      ['offers', 'price'],
                                      ['offers', 'priceCurrency'],
                                      ['offers', 'itemCondition'],
                                      'itemOffered',
                                      ['mileageFromOdometer', 'value'],
                                      ['mileageFromOdometer', 'unitText'],
                                      'hasEnergyConsumptionDetails'
                                  ],
                                  errors='ignore')
        engine = pd.json_normalize(par, record_path=['itemOffered', 'vehicleEngine'],
                                   meta=[
                                       ['vehicleEngine', 'fuelType'],
                                       ['engineDisplacement', 'value'],
                                       ['engineDisplacement', 'unitCode'],
                                   ],
                                   meta_prefix='engine',
                                   errors='ignore')
        engine_details = pd.json_normalize(par, record_path=['itemOffered', 'vehicleEngine', 'enginePower'],
                                           meta=[
                                               ['enginePower', 'value'],
                                               ['enginePower', 'unitCode']
                                           ],
                                           meta_prefix='engine_details',
                                           errors='ignore')
        offer_details = offer.merge(engine, left_index=True, right_index=True)
        offer_details_final = offer_details.merge(engine_details, left_index=True, right_index=True)
        df_scout = df_scout.append(offer_details_final)
    df_scout_complete = df_scout
    df_oto_complete = pd.DataFrame(car_parameters_otomoto)


    return df_scout_complete, df_oto_complete


autoscout_features, otomoto_features = get_initial_load()
df_scout_complete, df_oto_complete = get_dataframes(car_parameters_autoscout24=autoscout_features,
                                                    car_parameters_otomoto=otomoto_features)



df_scout_complete.to_csv('df_scout_complete.csv')
df_oto_complete.to_csv('df_oto_complete.csv')
