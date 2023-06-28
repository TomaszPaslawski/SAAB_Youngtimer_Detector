import pandas as pd
import random
import numpy as np
import requests

df_autoscout = pd.read_csv('D:\Projekty Python\SAAB_Youngtimer_Detector\df_scout_complete.csv')

"""
Basing on the initial analysis of the values in columns (using .unique()) it has been discovered that some of the 
columns are either duplicates or do not bring any essential values for the further steps in the project. It has been 
decided that they are going to be dropped from the df.autoscout dataframe.
"""

columns_to_drop_from_autoscout = ['Unnamed: 0', '@type_x', 'offeredBy.telephone', 'offeredBy.name', 'offeredBy.image',
                                  'offeredBy.address.@type', 'offeredBy.address.streetAddress',
                                  'offeredBy.address.addressLocality', 'offeredBy.address.postalCode',
                                  'offeredBy.address.addressCountry', 'itemOffered.@type', 'itemOffered.image',
                                  'itemOffered.identifier', 'itemOffered.mileageFromOdometer.@type',
                                  'itemOffered.mileageFromOdometer.unitText', 'itemOffered.vehicleInteriorType',
                                  'itemOffered.vehicleInteriorColor', 'itemOffered.hasEnergyConsumptionDetails.@type',
                                  'itemOffered.hasEnergyConsumptionDetails.energyEfficiencyScaleMax',
                                  'itemOffered.hasEnergyConsumptionDetails.energyEfficiencyScaleMin',
                                  'itemOffered.vehicleEngine', '@type_y', 'enginePower', 'engineDisplacement.@type',
                                  'engineDisplacement.unitCode', 'enginevehicleEngine.fuelType',
                                  'engineengineDisplacement.value', 'engineengineDisplacement.unitCode', '@type',
                                  'unitCode', 'engine_detailsenginePower.value', 'engine_detailsenginePower.unitCode',
                                  'itemOffered.fuelConsumption.@type', 'itemOffered.fuelConsumption.unitText',
                                  'itemOffered.fuelConsumption', 'engineDisplacement']

df_autoscout = df_autoscout.drop(columns=columns_to_drop_from_autoscout)

df_otomoto = pd.read_csv('df_oto_complete.csv')

"""
Like above (basing on .unique()) the list of the columns to be removed from df_otomoto dataframe has been chosen.
"""

columns_to_drop_from_otomoto = ['Unnamed: 0', 'Kategoria', 'Pokaż oferty z numerem VIN', 'Ma numer rejestracyjny',
                                'Generacja', 'Rodzaj koloru', 'Kraj pochodzenia', 'Numer rejestracyjny pojazdu',
                                'Zarejestrowany w Polsce', 'VIN', 'VAT marża', 'Bezwypadkowy', 'Uszkodzony',
                                'Serwisowany w ASO', 'Kierownica po prawej (Anglik)', 'Filtr cząstek stałych',
                                'Spalanie Poza Miastem', 'Spalanie W Cyklu Mieszanym', 'Możliwość finansowania',
                                'Faktura VAT', 'Zarejestrowany jako zabytek', 'Tuning', 'Leasing',
                                'Gwarancja dealerska (w cenie)', 'lub do (przebieg km)']

df_otomoto = df_otomoto.drop(columns=columns_to_drop_from_otomoto)

"""
Further analysis based on the use of .info() as well as the comparison between both dataframes leads to the conclusion
that some other columns need to be dropped. Reason for this action is mainly the fact that they are existing in one 
of the given dataframes. However, in few cases the reason is the huge amount of NaN values which cannot be covered and
data cannot be taken from the other source.
"""
additional_drop_autoscout = ['itemCondition', 'availability', 'itemOffered.name', 'itemOffered.manufacturer',
                             'itemOffered.numberOfForwardGears', 'itemOffered.numberOfPreviousOwners',
                             'itemOffered.hasEnergyConsumptionDetails.hasEnergyEfficiencyCategory',
                             'itemOffered.emissionsCO2']
additional_drop_otomoto = ['Pierwszy właściciel (od nowości)', 'Emisja CO2',
                           'Data pierwszej rejestracji w historii pojazdu', 'Typ_nadwozia_add', 'Przebieg_add', 'Rok',
                           'Stan', 'Marka pojazdu', 'Paliwo']

df_autoscout = df_autoscout.drop(columns=additional_drop_autoscout)
df_otomoto = df_otomoto.drop(columns=additional_drop_otomoto)

"""
Before joining two dataframes into one set of data, some additional actions need to be taken:
1) Provide the unified names for the columns,
2) Provide the order of columns that dataframe should have,
3) Having the same type of data and format of data in the columns with the same title.
"""

New_columns_names_and_order = ['ImageId', 'Price', 'OriginalCurrency', 'Model', 'Version', 'BodyType', 'Mileage(KMT)',
                               'ProductionYear',
                               'DriveConfig', 'Transmission', 'Fuel', 'FuelConsumption', 'EngineDisplacement',
                               'EnginePower(HP)',
                               'Doors', 'Seats', 'Color', 'OfferFrom']

df_autoscout = df_autoscout.rename(columns={
    'id': 'ImageId',
    'price': 'Price',
    'priceCurrency': 'OriginalCurrency',
    'itemOffered.model': 'Model',
    'version': 'Version',
    'itemOffered.bodyType': 'BodyType',
    'itemOffered.mileageFromOdometer.value': 'Mileage(KMT)',
    'itemOffered.productionDate': 'ProductionYear',
    'itemOffered.driveWheelConfiguration': 'DriveConfig',
    'itemOffered.vehicleTransmission': 'Transmission',
    'fuelType': 'Fuel',
    'itemOffered.fuelConsumption.value': 'FuelConsumption',
    'engineDisplacement.value': 'EngineDisplacement',
    'value': 'EnginePower(HP)',
    'itemOffered.numberOfDoors': 'Doors',
    'itemOffered.seatingCapacity': 'Seats',
    'itemOffered.color': 'Color',
    'offeredBy.@type': 'OfferFrom'
})

df_otomoto = df_otomoto.rename(columns={
    'id': 'ImageId',
    'price': 'Price',
    'currency': 'OriginalCurrency',
    'Model pojazdu': 'Model',
    'Wersja': 'Version',
    'Typ nadwozia': 'BodyType',
    'Przebieg': 'Mileage(KMT)',
    'Rok produkcji': 'ProductionYear',
    'Napęd': 'DriveConfig',
    'Skrzynia biegów': 'Transmission',
    'Rodzaj paliwa': 'Fuel',
    'Spalanie W Mieście': 'FuelConsumption',
    'Pojemność skokowa': 'EngineDisplacement',
    'Moc': 'EnginePower(HP)',
    'Liczba drzwi': 'Doors',
    'Liczba miejsc': 'Seats',
    'Kolor': 'Color',
    'Oferta od': 'OfferFrom'
})

df_autoscout = df_autoscout.reindex(columns=New_columns_names_and_order)
df_otomoto = df_otomoto.reindex(columns=New_columns_names_and_order)

"""
Unification of the format for the column 'ProductionYear'. Since the otomoto format contains only the year and 
autoscout format contians the whole data format, it has been decided to reduce the format of the production date only
to the year of production.
"""
df_autoscout['ProductionYear'] = df_autoscout['ProductionYear'].str[:4]
df_autoscout['ProductionYear'] = df_autoscout['ProductionYear'].astype(int)
df_otomoto['ProductionYear'] = df_otomoto['ProductionYear'].astype(int)

"""
Unification of the format for 'Mileage(KMT)'. The original autoscout format had value separated from the unit while at 
otomoto value is united with the unit. To unify the format the otomoto data has been reduced to the numerals (still in 
the string format) and then converted into integer format. For the autoscout data only the format has been changed into
the integer.
"""
df_otomoto['Mileage(KMT)'] = df_otomoto['Mileage(KMT)'].str[:-3]
df_otomoto['Mileage(KMT)'] = df_otomoto['Mileage(KMT)'].str.replace(' ', '')
df_otomoto['Mileage(KMT)'] = df_otomoto['Mileage(KMT)'].astype(int)
df_autoscout['Mileage(KMT)'] = df_autoscout['Mileage(KMT)'].astype(int)

"""
As in the above case otomoto had value of the engine power unified with the unit and autoscout provided value separated 
from it. The unit description has been removed from the otomoto data and both otomoto and autoscout values have been
converted into the integers. 
"""
df_otomoto['EnginePower(HP)'] = df_otomoto['EnginePower(HP)'].str[:-3]
df_otomoto['EnginePower(HP)'] = df_otomoto['EnginePower(HP)'].astype(int)
df_autoscout['EnginePower(HP)'] = df_autoscout['EnginePower(HP)'].astype(int)

"""
Next step is the unification of the values in the 'OfferFrom' column. Two values have been chosen: 'Dealer' and 
'Private'. In case of the otomoto dataframe all the values have been populated and they need only to be renamed. 
In case of the autoscout there were many NaN values which one can assume as the private offers since the offers from 
the dealers are always well described with all dealer's information. 
"""
df_autoscout['OfferFrom'] = df_autoscout['OfferFrom'].fillna('Private')
df_autoscout['OfferFrom'] = df_autoscout['OfferFrom'].str.replace('AutoDealer', 'Dealer')
df_otomoto['OfferFrom'] = df_otomoto['OfferFrom'].str.replace('Osoby prywatnej', 'Private')
df_otomoto['OfferFrom'] = df_otomoto['OfferFrom'].str.replace('Firmy', 'Dealer')

"""
Column 'BodyTypes' also needed unification. There were two aspects of it:
1) Unify the names of different body types between the datasets e.g. there was 'Limuzyna' at autoscout and 'Sedan' at 
otomoto. After unification in both datasets this type of body is presetned as 'Sedan'.
2) Deal with the non-significant values like 'Pozostałe' or 'Auta miejskie'. After verification it has been spotted that
in most of the cases the significant body class can be assigned with high certainty. 
"""
BodyTypes = ['Sportowy (Coupe)', 'Kabriolet', 'Sedan']
df_autoscout['BodyType'] = df_autoscout['BodyType'].str.replace('Samochód małolitrażowy', 'Sportowy (Coupe)')
df_autoscout['BodyType'] = df_autoscout['BodyType'].str.replace('Limuzyna', 'Sedan')
df_autoscout['BodyType'] = df_autoscout['BodyType'].str.replace('Pozostałe', random.choice(BodyTypes))
df_autoscout['BodyType'] = df_autoscout['BodyType'].str.replace('Samochód dostawczy', 'Samochód terenowy/Pickup')
BodyTypes1 = ['Sportowy (Coupe)', 'Kombi/Van', 'Sedan']
df_otomoto['BodyType'] = df_otomoto['BodyType'].str.replace('Kombi', 'Kombi/Van')
df_otomoto['BodyType'] = df_otomoto['BodyType'].str.replace('Coupe', 'Sportowy (Coupe)')
df_otomoto['BodyType'] = df_otomoto['BodyType'].str.replace('Kompakt', 'Sportowy (Coupe)')
df_otomoto['BodyType'] = df_otomoto['BodyType'].str.replace('SUV', 'Samochód terenowy/Pickup')
df_otomoto['BodyType'] = df_otomoto['BodyType'].str.replace('Auta miejskie', random.choice(BodyTypes1))
df_otomoto['BodyType'] = df_otomoto['BodyType'].str.replace('Auta małe', 'Sedan')

"""
According to the official documentation SAAB vehicles were originally painted in:
'Szary',
'Czerwony',
'Niebieski',
'Zielony',
'Biały',
'Brązowy',
'Czarny',
'Żółty',
'Beżowy',
'Srebrny',
'Złoty',
'Fioletowy'

Thus, the colors descriptions of the vehicles have been aligned with these official ones.
Furthermore, in cases in which the color has not been precised ('Inny kolor' or NaN), it is chosen randomly from the 
most possible options. 
"""
random_colors = ['Czarny', 'Szary']
df_autoscout['Color'] = df_autoscout['Color'].str.replace('Brązowy', 'Brąz')
df_autoscout['Color'] = df_autoscout['Color'].str.replace('Brąz', 'Brązowy')
df_autoscout['Color'] = df_autoscout['Color'].fillna(random.choice(random_colors))

random_colors1 = ['Beżowy', 'Szary']
df_otomoto['Color'] = df_otomoto['Color'].str.replace('Granatowy', 'Niebieski')
df_otomoto['Color'] = df_otomoto['Color'].str.replace('Błękitny', 'Niebieski')
df_otomoto['Color'] = df_otomoto['Color'].str.replace('Bordowy', 'Czerwony')
df_otomoto['Color'] = df_otomoto['Color'].str.replace('Inny kolor', random.choice(random_colors1))

"""
There are some empty values for the column 'Seats'. However, this values can be easily triggered from the body type.
After triggering format in both columns is setup as integer.
"""
df_autoscout['Seats'] = np.where((df_autoscout['Seats'].isna()) & (df_autoscout['BodyType'] == 'Kabriolet'),
                                 4, np.where(df_autoscout['Seats'].isna(), 5, df_autoscout['Seats']))
df_otomoto['Seats'] = np.where((df_otomoto['Seats'].isna()) & (df_otomoto['BodyType'] == 'Kabriolet'),
                               4, np.where(df_otomoto['Seats'].isna(), 5, df_otomoto['Seats']))
df_autoscout['Seats'] = df_autoscout['Seats'].astype(int)
df_otomoto['Seats'] = df_otomoto['Seats'].astype(int)

"""
For the correct maintenance of the column 'Model' the rows which do not have value provided will be dropped. In case of
the otomoto dataset some amendments in the names are needed to keep them inline with the autoscout values. One need be
aware that 'Model' is one of the most crucial information for the correct creation of the further models.
"""
df_autoscout = df_autoscout.dropna(subset='Model')
df_autoscout['Model'] = df_autoscout['Model'].str.replace('93', '9-3')
df_otomoto = df_otomoto.dropna(subset='Model')
df_otomoto['Model'] = df_otomoto['Model'].str.replace('9-3X', '9-3')
df_otomoto['Model'] = np.where((df_otomoto['Model'] == 'Inny') & (df_otomoto['BodyType'] == 'Samochód terenowy/Pickup'),
                               '9-7X', np.where(df_otomoto['Model'] == 'Inny', 'Sonett', df_otomoto['Model']))

"""
SAAB never had a RWD vehicles. Thus, only two options are available: FWD and 4x4. 
"""
df_autoscout['DriveConfig'] = np.where((df_autoscout['DriveConfig'].isna() &
                                        df_autoscout['BodyType'] == 'Samochód terenowy/Pickup'), '4x4',
                                       np.where(df_autoscout['DriveConfig'].isna(), 'FWD', df_autoscout['DriveConfig']))
df_autoscout['DriveConfig'] = df_autoscout['DriveConfig'].str.replace('Na przednie koła', 'FWD')
df_autoscout['DriveConfig'] = df_autoscout['DriveConfig'].str.replace('Na tylnie koła', 'FWD')
df_otomoto['DriveConfig'] = np.where((df_otomoto['DriveConfig'].isna() &
                                      df_otomoto['BodyType'] == 'Samochód terenowy/Pickup'), '4x4',
                                     np.where(df_otomoto['DriveConfig'].isna(), 'FWD', df_otomoto['DriveConfig']))
df_otomoto['DriveConfig'] = df_otomoto['DriveConfig'].str.replace('Na przednie koła', 'FWD')
df_otomoto['DriveConfig'] = df_otomoto['DriveConfig'].str.replace('Na tylne koła', 'FWD')
df_otomoto['DriveConfig'] = df_otomoto['DriveConfig'].str[:3]

"""
For the empty rows in the column 'Transmission' the values from the 'Version' will be used. Function will check if 
somewhere in the version description exists the beginning of the word 'automat' (in that case 'automa' since some typo 
errors were spotted during EDA (like 'automaat'). Once the automatic transmission will be updated, rest of lacking 
values will be fulfilled by the description of the manual transmission. 
"""
df_autoscout['Transmission'] = np.where(df_autoscout['Transmission'].isna() &
                                        df_autoscout['Version'].str.contains('automa'), 'Automatyczna',
                                        df_autoscout['Transmission'])
df_autoscout['Transmission'] = np.where(df_autoscout['Transmission'].isna(), 'Manualna', df_autoscout['Transmission'])
df_autoscout['Transmission'] = df_autoscout['Transmission'].str.replace('Półautomatyczna', 'Automatyczna')

"""
For the otomoto details regarding the fuel are quite well supported and not mismatched unlike the autoscout. 
At autoscout there are many entries where the fuel type is not populated. To cover this info, once again the 
information from the column 'Version' will be used. Furthermore, there was also high inconsistency in the names which
needed to be resolved. All those actions have ended with three categories of fuel.
"""
df_autoscout['Fuel'] = np.where(df_autoscout['Fuel'].isna() & df_autoscout['Version'].str.contains('tid'), 'Diesel',
                                df_autoscout['Fuel'])
df_autoscout['Fuel'] = np.where(df_autoscout['Fuel'].isna() & df_autoscout['Version'].str.contains('t ') |
                                df_autoscout['Version'].str.contains('T '), 'Benzyna', df_autoscout['Fuel'])
df_autoscout['Fuel'] = np.where(df_autoscout['Fuel'].str.contains('Super')
                                | df_autoscout['Fuel'].str.contains('Regular')
                                | df_autoscout['Fuel'].str.contains('etanol'), 'Benzyna',
                                df_autoscout['Fuel'])
df_autoscout['Fuel'] = np.where(df_autoscout['Fuel'].str.contains('LPG'), 'Benzyna+LPG', df_autoscout['Fuel'])

"""
Since the lack of the doors number touches mainly the old SAAB vehicles it is not difficult to retrieve the data 
using either the body type (for cabriolets) or model. To keep the format inline between the datasets for the autoscout
it has been changed into integer.
"""
df_autoscout['Doors'] = np.where((df_autoscout['Doors'].isna()) & (df_autoscout['BodyType'] == 'Kabriolet'), 2,
                                 df_autoscout['Doors'])
df_autoscout['Doors'] = np.where((df_autoscout['Doors'].isna()) & (df_autoscout['Model'] == '95'), 3,
                                 df_autoscout['Doors'])
df_autoscout['Doors'] = np.where((df_autoscout['Doors'].isna()) & (df_autoscout['Model'] == '96') |
                                 (df_autoscout['Model'] == '99') | (df_autoscout['Model'] == '900'), 3,
                                 df_autoscout['Doors'])
df_autoscout['Doors'] = df_autoscout['Doors'].astype(int)

"""
To deal with the empty rows the average fuel consumption form official websites will be used. For the oldest cars 
(like SAAB 96) the value will be the mean of the whole fuel consumption values. For the unification the both datasets
will use the float format.
"""
df_autoscout['FuelConsumption'] = np.where(
    df_autoscout['FuelConsumption'].isna() & (df_autoscout['Fuel'] == 'Benzyna') |
    (df_autoscout['Fuel'] == 'Benzyna+LPG') & (df_autoscout['Model'] == '9-5') |
    (df_autoscout['Model'] == '9000'), 10.5, df_autoscout['FuelConsumption'])
df_autoscout['FuelConsumption'] = np.where(df_autoscout['FuelConsumption'].isna() & (df_autoscout['Fuel'] == 'Diesel') &
                                           (df_autoscout['Model'] == '9-5') | (df_autoscout['Model'] == '9-3'), 7.5,
                                           df_autoscout['FuelConsumption'])
df_autoscout['FuelConsumption'] = np.where(
                                df_autoscout['FuelConsumption'].isna() & (df_autoscout['Fuel'] == 'Benzyna') &
                                (df_autoscout['Model'] == '9-3'), 10.0,
                                np.where(df_autoscout['FuelConsumption'].isna() &
                                (df_autoscout['Model'] == '9-7X'), 13.5, df_autoscout['FuelConsumption']))
df_autoscout['FuelConsumption'] = np.where(
                                df_autoscout['FuelConsumption'].isna() & (df_autoscout['Fuel'] == 'Benzyna') | (
                                df_autoscout['Fuel'] == 'Benzyna+LPG') & (df_autoscout['Model'] == '900'), 9.5,
                                np.where(df_autoscout['FuelConsumption'].isna() & (df_autoscout['Model'] == '99'), 8.5,
                                df_autoscout['FuelConsumption']))
average_consumption = round(df_autoscout['FuelConsumption'].mean(), 1)
df_autoscout['FuelConsumption'] = df_autoscout['FuelConsumption'].fillna(average_consumption)

df_otomoto['FuelConsumption'] = df_otomoto['FuelConsumption'].str[:-8]
df_otomoto['FuelConsumption'] = df_otomoto['FuelConsumption'].str.replace(',', '.')
df_otomoto['FuelConsumption'] = np.where(df_otomoto['FuelConsumption'].isna() & (df_otomoto['Fuel'] == 'Benzyna') |
                                         (df_otomoto['Fuel'] == 'Benzyna+LPG') & (df_otomoto['Model'] == '9-5') |
                                         (df_otomoto['Model'] == '9000'), 10.5, df_otomoto['FuelConsumption'])
df_otomoto['FuelConsumption'] = np.where(df_otomoto['FuelConsumption'].isna() & (df_otomoto['Fuel'] == 'Diesel') &
                                         (df_otomoto['Model'] == '9-5') | (df_otomoto['Model'] == '9-3'), 7.5,
                                         df_otomoto['FuelConsumption'])
df_otomoto['FuelConsumption'] = np.where(df_otomoto['FuelConsumption'].isna() & (df_otomoto['Fuel'] == 'Benzyna') &
                                         (df_otomoto['Model'] == '9-3'), 10.0,
                                         np.where(
                                             df_otomoto['FuelConsumption'].isna() & (df_otomoto['Model'] == '9-7X'),
                                             13.5,
                                             df_otomoto['FuelConsumption']))
df_otomoto['FuelConsumption'] = np.where(df_otomoto['FuelConsumption'].isna() & (df_otomoto['Fuel'] == 'Benzyna') |
                                         (df_otomoto['Fuel'] == 'Benzyna+LPG') & (df_otomoto['Model'] == '900'), 9.5,
                                         np.where(df_otomoto['FuelConsumption'].isna() & (df_otomoto['Model'] == '99'),
                                                  8.5,
                                                  df_otomoto['FuelConsumption']))

average_consumption = round(df_otomoto['FuelConsumption'].notna().mean(),1)
df_otomoto['FuelConsumption'] = df_otomoto['FuelConsumption'].fillna(average_consumption)
df_otomoto['FuelConsumption'] = df_otomoto['FuelConsumption'].astype(float)

"""
For the update of the engine displacement is used mostly the very descriptive columns 'Version'. However, if there is 
no significant value in that columns the empty row is updated with the most probably value (that is 1998 as it was the 
most popular SAAB engine.
"""
df_autoscout['EngineDisplacement'] = np.where((df_autoscout['EngineDisplacement'].isna())&
                                              (df_autoscout['Version'].str.contains('2.0')), 1998,
                                              df_autoscout['EngineDisplacement'])
df_autoscout['EngineDisplacement'] = np.where((df_autoscout['EngineDisplacement'].isna())&
                                              (df_autoscout['Version'].str.contains('2.3')) |
                                              (df_autoscout['Version'].str.contains('2,3')), 2290,
                                              df_autoscout['EngineDisplacement'])
df_autoscout['EngineDisplacement'] = np.where((df_autoscout['EngineDisplacement'].isna() &
                                               df_autoscout['Model']=='96'), 1498, df_autoscout['EngineDisplacement'])
df_autoscout['EngineDisplacement'] = df_autoscout['EngineDisplacement'].fillna(1998)

"""
This part is the currency converter as the currency of otomoto is different than the currency of autoscout. It takes the
current mid from the NBP website and applies it to the prices expressed in PLN.
"""
url = 'http://api.nbp.pl/api/exchangerates/tables/A?format=json'
response = requests.get(url)
curr_values = response.json()
values = curr_values[0]['rates']
EUR_PLN = values[7]['mid']
df_otomoto['Price'] = round(df_otomoto['Price']/EUR_PLN,0)
df_otomoto['Price'] = df_otomoto['Price'].astype(int)

"""
Additional updates spotted during the value_counts check on the datasets
"""
df_autoscout['FuelConsumption'] = np.where(df_autoscout['FuelConsumption']<5.0, 9.5, df_autoscout['FuelConsumption'])

"""
After completing the cleaning of the data, they can be merged.
"""
df_final = df_autoscout.append(df_otomoto)
df_final = df_final.reset_index

