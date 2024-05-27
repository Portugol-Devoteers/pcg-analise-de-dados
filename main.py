# %%

import pandas as pd
import matplotlib.pyplot as plt
import re
import numpy as np
import seaborn as sns
import statsmodels.api as sm

 
#%% 
df = pd.read_csv('Consumo Energia Mundial.csv') # Carregando o arquivo CSV


countries_to_remove = [
    'ASEAN (Ember)',
    'Africa',
    'Africa (EI)',
    'Africa (Ember)',
    'Africa (Shift)',
    'Asia',
    'Asia & Oceania (EIA)',
    'Asia (Ember)',
    'Asia Pacific (EI)',
    'Asia and Oceania (Shift)',
    'Australia and New Zealand (EIA)',
    'CIS (EI)',
    'Central & South America (EIA)',
    'South America',
    'South and Central America (EI)',
    'Central America (EI)',
    'Central and South America (Shift)',
    'EU28 (Shift)',
    'East Germany (EIA)',
    'Eastern Africa (EI)',
    'Eurasia (EIA)',
    'Eurasia (Shift)',
    'Europe',
    'Europe (EI)',
    'Europe (Ember)',
    'Europe (Shift)',
    'European Union (27)',
    'European Union (EIA)',
    'G20 (Ember)',
    'G7 (Ember)',
    'Hawaiian Trade Zone (EIA)',
    'High-income countries',
    'IEO - Africa (EIA)',
    'IEO - Middle East (EIA)',
    'IEO OECD - Europe (EIA)',
    'Latin America and Caribbean (Ember)',
    'Low-income countries',
    'Lower-middle-income countries',
    'Mexico, Chile, and other OECD Americas (EIA)',
    'Middle Africa (EI)',
    'Middle East (EI)',
    'Middle East (EIA)',
    'Middle East (Ember)',
    'Middle East (Shift)',
    'Non-OECD (EI)',
    'Non-OECD (EIA)',
    'Non-OPEC (EI)',
    'Non-OPEC (EIA)',
    'North America',
    'North America (EI)',
    'North America (Ember)',
    'North America (Shift)',
    'OECD (EI)',
    'OECD (EIA)',
    'OECD (Ember)',
    'OECD (Shift)',
    'OECD - Asia And Oceania (EIA)',
    'OECD - Europe (EIA)',
    'OECD - North America (EIA)',
    'OPEC (EI)',
    'OPEC (EIA)',
    'OPEC (Shift)',
    'OPEC - Africa (EIA)',
    'OPEC - South America (EIA)',
    'Oceania',
    'Oceania (Ember)',
    'Other Non-OECD - America (EIA)',
    'Other Non-OECD - Asia (EIA)',
    'Other Non-OECD - Europe and Eurasia (EIA)',
    'U.S. Pacific Islands (EIA)',
    'U.S. Territories (EIA)',
    'USSR',
    'United States Pacific Islands (Shift)',
    'United States Territories (Shift)',
    'United States Virgin Islands',
    'Persian Gulf (EIA)',
    'Persian Gulf (Shift)',
    'South Korea and other OECD Asia (EIA)',
    'Upper-middle-income countries',
    'Wake Island (EIA)',
    'Wake Island (Shift)',
    'West Germany (EIA)',
    'Western Africa (EI)',
    'World',
    'Yugoslavia'
]

df = df[~df['country'].isin(countries_to_remove)] # Removendo regiões que não são países

renewables_columns = [
    'country', 'year', 'iso_code', 'population', 'gdp',
    'renewables_cons_change_pct', 'renewables_cons_change_twh', 'renewables_consumption',
    'renewables_elec_per_capita', 'renewables_electricity', 'renewables_energy_per_capita',
    'renewables_share_elec', 'renewables_share_energy', 'solar_cons_change_pct',
    'solar_cons_change_twh', 'solar_consumption', 'solar_elec_per_capita', 'solar_electricity',
    'solar_energy_per_capita', 'solar_share_elec', 'solar_share_energy', 'wind_cons_change_pct',
    'wind_cons_change_twh', 'wind_consumption', 'wind_elec_per_capita', 'wind_electricity',
    'wind_energy_per_capita', 'wind_share_elec', 'wind_share_energy', 'hydro_cons_change_pct',
    'hydro_cons_change_twh', 'hydro_consumption', 'hydro_elec_per_capita', 'hydro_electricity',
    'hydro_energy_per_capita', 'hydro_share_elec', 'hydro_share_energy',
    'other_renewable_consumption', 'other_renewable_electricity',
    'other_renewable_exc_biofuel_electricity', 'other_renewables_cons_change_pct',
    'other_renewables_cons_change_twh', 'other_renewables_elec_per_capita',
    'other_renewables_elec_per_capita_exc_biofuel', 'other_renewables_energy_per_capita',
    'other_renewables_share_elec', 'other_renewables_share_elec_exc_biofuel',
    'other_renewables_share_energy', 'electricity_generation'
]

non_renewables_columns = [
    'country', 'year', 'iso_code', 'population', 'gdp',
    'fossil_cons_change_pct', 'fossil_cons_change_twh', 'fossil_elec_per_capita',
    'fossil_electricity', 'fossil_energy_per_capita', 'fossil_fuel_consumption',
    'fossil_share_elec', 'fossil_share_energy', 'coal_cons_change_pct',
    'coal_cons_change_twh', 'coal_cons_per_capita', 'coal_consumption',
    'coal_elec_per_capita', 'coal_electricity', 'coal_prod_change_pct',
    'coal_prod_change_twh', 'coal_prod_per_capita', 'coal_production',
    'coal_share_elec', 'coal_share_energy', 'oil_cons_change_pct', 'oil_cons_change_twh',
    'oil_consumption', 'oil_elec_per_capita', 'oil_electricity', 'oil_energy_per_capita',
    'oil_prod_change_pct', 'oil_prod_change_twh', 'oil_prod_per_capita', 'oil_production',
    'oil_share_elec', 'oil_share_energy', 'gas_cons_change_pct', 'gas_cons_change_twh',
    'gas_consumption', 'gas_elec_per_capita', 'gas_electricity', 'gas_energy_per_capita',
    'gas_prod_change_pct', 'gas_prod_change_twh', 'gas_prod_per_capita', 'gas_production',
    'gas_share_elec', 'gas_share_energy', 'nuclear_cons_change_pct', 'nuclear_cons_change_twh',
    'nuclear_consumption', 'nuclear_elec_per_capita', 'nuclear_electricity',
    'nuclear_energy_per_capita', 'nuclear_share_elec', 'nuclear_share_energy', 'electricity_generation', 'renewables_electricity'
]

df_renewables = df[renewables_columns] # Filtrando dataset para apenas colunas de energias renováveis
df_non_renewables = df[non_renewables_columns] # Filtrando dataset para apenas colunas de energias não renováveis

# %%
# TOP 20 países com maior consumo de energia renovável
df_renewables_grouped = df_renewables.groupby('country').sum()
df_renewables_grouped = df_renewables_grouped.sort_values(by='renewables_consumption', ascending=False).head(20)

plt.figure(figsize=(12, 8))

plt.barh(df_renewables_grouped.index, df_renewables_grouped['solar_consumption'], color='yellow', label='Solar')

plt.barh(df_renewables_grouped.index, df_renewables_grouped['wind_consumption'], left=df_renewables_grouped['solar_consumption'], color='blue', label='Eólica')

plt.barh(df_renewables_grouped.index, df_renewables_grouped['hydro_consumption'], left=df_renewables_grouped['solar_consumption'] + df_renewables_grouped['wind_consumption'], color='cyan', label='Hidrelétrica')

plt.barh(df_renewables_grouped.index, df_renewables_grouped['other_renewable_consumption'], left=df_renewables_grouped['solar_consumption'] + df_renewables_grouped['wind_consumption'] + df_renewables_grouped['hydro_consumption'], color='green', label='Outras')
plt.legend()
plt.title('Consumo de energia renovável por país')


# TOP 20 países com maior consumo de energia não renovável
df_non_renewables_grouped = df_non_renewables.groupby('country').sum()
df_non_renewables_grouped = df_non_renewables_grouped.sort_values(by='fossil_fuel_consumption', ascending=False).head(20)

plt.figure(figsize=(12, 8))


plt.barh(df_non_renewables_grouped.index, df_non_renewables_grouped['coal_consumption'], color='black', label='Carvão')
plt.barh(df_non_renewables_grouped.index, df_non_renewables_grouped['oil_consumption'], left=df_non_renewables_grouped['coal_consumption'], color='blue', label='Óleo')
plt.barh(df_non_renewables_grouped.index, df_non_renewables_grouped['gas_consumption'], left=df_non_renewables_grouped['coal_consumption'] + df_non_renewables_grouped['oil_consumption'], color='red', label='Gás')
plt.barh(df_non_renewables_grouped.index, df_non_renewables_grouped['nuclear_consumption'], left=df_non_renewables_grouped['coal_consumption'] + df_non_renewables_grouped['oil_consumption'] + df_non_renewables_grouped['gas_consumption'], color='green', label='Nuclear')
plt.legend()
plt.title('Consumo de energia não renovável por país')
plt.xlabel('Consumo de energia não renovável (TWh)')
plt.ylabel('País')
plt.show()




# %%
# Correlacionar o consumo de energia renovável com o PIB (gdp)

df['gdp'] = pd.to_numeric(df['gdp'], errors='coerce')
df['renewables_consumption'] = pd.to_numeric(df['renewables_consumption'], errors='coerce')

# Já realizou a conversão e limpeza dos dados
df_clean = df.dropna(subset=['gdp', 'renewables_consumption'])

# Calcula a correlação
correlation = df_clean['gdp'].corr(df_clean['renewables_consumption'])
print("Correlação entre PIB e Consumo de Energia Renovável:", correlation)

# Criação do gráfico
plt.figure(figsize=(10, 6))
plt.scatter(df_clean['gdp'], df_clean['renewables_consumption'], alpha=0.5, edgecolors='w', linewidth=0.5)

# Adicionando uma linha de tendência
z = np.polyfit(df_clean['gdp'], df_clean['renewables_consumption'], 1)
p = np.poly1d(z)
plt.plot(df_clean['gdp'], p(df_clean['gdp']), "r--")  # Linha de tendência vermelha pontilhada


slope = z[0]
intercept = z[1]
print(f"A equação da reta é: y = {slope:.4e}x + {intercept:.4f}")


plt.title('Relação Simples entre PIB e Consumo de Energia Renovável')
plt.xlabel('PIB (em trilhões de USD)')
plt.ylabel('Consumo de Energia Renovável (TWh)')
plt.grid(True)
plt.show()
plt.show()




# %%
# Correlacionar o consumo de energia não renovável com o PIB (gdp)

df['fossil_fuel_consumption'] = pd.to_numeric(df['fossil_fuel_consumption'], errors='coerce')

# Já realizou a conversão e limpeza dos dados
df_clean = df.dropna(subset=['gdp', 'fossil_fuel_consumption'])

# Calcula a correlação
correlation = df_clean['gdp'].corr(df_clean['fossil_fuel_consumption'])
print("Correlação entre PIB e Consumo de Energia Não Renovável:", correlation)

# Criação do gráfico
plt.figure(figsize=(10, 6))
plt.scatter(df_clean['gdp'], df_clean['fossil_fuel_consumption'], alpha=0.5, edgecolors='w', linewidth=0.5)

# Adicionando uma linha de tendência

z = np.polyfit(df_clean['gdp'], df_clean['fossil_fuel_consumption'], 1)
p = np.poly1d(z)
plt.plot(df_clean['gdp'], p(df_clean['gdp']), "r--")  # Linha de tendência vermelha pontilhada

slope = z[0]
intercept = z[1]
print(f"A equação da reta é: y = {slope:.4e}x + {intercept:.4f}")

plt.title('Relação Simples entre PIB e Consumo de Energia Não Renovável')
plt.xlabel('PIB (em trilhões de USD)')
plt.ylabel('Consumo de Energia Não Renovável (TWh)')
plt.grid(True)
plt.show()


# %%

# Calculando porcentagens de consumo de energia renovável e não renovável

df['renewables_percent'] = df['renewables_electricity'] / df['electricity_generation'] 
df['non_renewables_percent'] = 1 - df['renewables_percent']

# Correlacionando renewable_percent com PIB (gdp)

df['gdp'] = pd.to_numeric(df['gdp'], errors='coerce')

# Já realizou a conversão e limpeza dos dados
df_clean = df.dropna(subset=['gdp', 'renewables_percent'])

# Calcula a correlação
correlation = df_clean['gdp'].corr(df_clean['renewables_percent'])
print("Correlação entre PIB e Consumo de Energia Renovável:", correlation)

# Criação do gráfico
plt.figure(figsize=(10, 6))
plt.scatter(df_clean['gdp'], df_clean['renewables_percent'], alpha=0.5, edgecolors='w', linewidth=0.5)

# Adicionando uma linha de tendência

z = np.polyfit(df_clean['gdp'], df_clean['renewables_percent'], 1)
p = np.poly1d(z)
plt.plot(df_clean['gdp'], p(df_clean['gdp']), "r--")  # Linha de tendência vermelha pontilhada

slope = z[0]
intercept = z[1]
print(f"A equação da reta é: y = {slope:.4e}x + {intercept:.4f}")

plt.title('Relação Simples entre PIB e Consumo de Energia Renovável')
plt.xlabel('PIB (em trilhões de USD)')
plt.ylabel('Consumo de Energia Renovável (%)')
plt.grid(True)
plt.show()


# Correlacionando non_renewables_percent com PIB (gdp)

# Já realizou a conversão e limpeza dos dados
df_clean = df.dropna(subset=['gdp', 'non_renewables_percent'])

# Calcula a correlação
correlation = df_clean['gdp'].corr(df_clean['non_renewables_percent'])
print("Correlação entre PIB e Consumo de Energia Não Renovável:", correlation)

# Criação do gráfico
plt.figure(figsize=(10, 6))
plt.scatter(df_clean['gdp'], df_clean['non_renewables_percent'], alpha=0.5, edgecolors='w', linewidth=0.5)

# Adicionando uma linha de tendência

z = np.polyfit(df_clean['gdp'], df_clean['non_renewables_percent'], 1)
p = np.poly1d(z)
plt.plot(df_clean['gdp'], p(df_clean['gdp']), "r--")  # Linha de tendência vermelha pontilhada

slope = z[0]
intercept = z[1]
print(f"A equação da reta é: y = {slope:.4e}x + {intercept:.4f}")

plt.title('Relação Simples entre PIB e Consumo de Energia Não Renovável')
plt.xlabel('PIB (em trilhões de USD)')
plt.ylabel('Consumo de Energia Não Renovável (%)')
plt.grid(True)
plt.show()

# %%

