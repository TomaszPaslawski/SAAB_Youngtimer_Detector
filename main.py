import pandas as pd

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
"""

New_columns_names_and_order = ['ImageId', 'Price', 'Currency', 'Model', 'Version', 'BodyType', 'Mileage(KMT)', 'ProductionYear',
'DriveConfig', 'Transmission', 'Fuel', 'FuelConsumption', 'EngineDisplacement', 'EnginePower(HP)',
'Doors', 'Seats', 'Color', 'OfferFrom']

df_autoscout = df_autoscout.rename(columns={
                                            'id' : 'ImageId',
                                            'price': 'Price',
                                            'priceCurrency': 'Currency',
                                            'itemOffered.model': 'Model',
                                            'version': 'Version',
                                            'itemOffered.bodyType': 'BodyType',
                                            'itemOffered.mileageFromOdometer.value': 'Mileage(KMT)',
                                            'itemOffered.productionDate': 'ProductionYear',
                                            'itemOffered.driveWheelConfiguration' :'DriveConfig',
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
                                            'id' : 'ImageId',
                                            'price': 'Price',
                                            'currency': 'Currency',
                                            'Model pojazdu': 'Model',
                                            'Wersja': 'Version',
                                            'Typ nadwozia': 'BodyType',
                                            'Przebieg': 'Mileage(KMT)',
                                            'Rok produkcji': 'ProductionYear',
                                            'Napęd' :'DriveConfig',
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
