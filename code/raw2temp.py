E=meta['Emissivity']
OD = 1.0
if 'SubjectDistance' in meta:
    OD = meta['SubjectDistance']
RTemp=meta['ReflectedApparentTemperature']
ATemp=meta['AtmosphericTemperature']
IRWTemp=meta['IRWindowTemperature']
IRT=meta['IRWindowTransmission']
RH=meta['RelativeHumidity']
PR1=meta['PlanckR1']
PB=meta['PlanckB']
PF=meta['PlanckF']
PO=meta['PlanckO']
PR2=meta['PlanckR2']
                                                                          
# constants
ATA1 = 0.006569
ATA2 = 0.01262
ATB1 = -0.002276
ATB2 = -0.00667
ATX = 1.9

# transmission through window (calibrated)
emiss_wind = 1 - IRT
refl_wind = 0

# transmission through the air
h2o = (RH / 100) * exp(1.5587 + 0.06939 * (ATemp) - 0.00027816 * (ATemp) ** 2 + 0.00000068455 * (ATemp) ** 3)
tau1 = ATX * exp(-sqrt(OD / 2) * (ATA1 + ATB1 * sqrt(h2o))) + (1 - ATX) * exp(-sqrt(OD / 2) * (ATA2 + ATB2 * sqrt(h2o)))
tau2 = ATX * exp(-sqrt(OD / 2) * (ATA1 + ATB1 * sqrt(h2o))) + (1 - ATX) * exp(-sqrt(OD / 2) * (ATA2 + ATB2 * sqrt(h2o)))

# radiance from the environment
raw_refl1 = PR1 / (PR2 * (exp(PB / (RTemp + 273.15)) - PF)) - PO
raw_refl1_attn = (1 - E) / E * raw_refl1
raw_atm1 = PR1 / (PR2 * (exp(PB / (ATemp + 273.15)) - PF)) - PO
raw_atm1_attn = (1 - tau1) / E / tau1 * raw_atm1
raw_wind = PR1 / (PR2 * (exp(PB / (IRWTemp + 273.15)) - PF)) - PO
raw_wind_attn = emiss_wind / E / tau1 / IRT * raw_wind
raw_refl2 = PR1 / (PR2 * (exp(PB / (RTemp + 273.15)) - PF)) - PO
raw_refl2_attn = refl_wind / E / tau1 / IRT * raw_refl2
raw_atm2 = PR1 / (PR2 * (exp(PB / (ATemp + 273.15)) - PF)) - PO
raw_atm2_attn = (1 - tau2) / E / tau1 / IRT / tau2 * raw_atm2
raw_obj = (raw / E / tau1 / IRT / tau2 - raw_atm1_attn - raw_atm2_attn - raw_wind_attn - raw_refl1_attn - raw_refl2_attn)

# temperature from radiance
temp_celcius = PB / log(PR1 / (PR2 * (raw_obj + PO)) + PF) - 273.15