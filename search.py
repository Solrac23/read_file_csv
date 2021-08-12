import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np

#  Crie relatórios com gráficos e tabelas (dataset de saída) que mostrem
# quem mais vendeu em tal unidade, % de CPF na nota, % de imposto,
# Quanto o dinheiro de volta rendeu em desconto,
# venda por vendedor(nome) e produto mais vendido.

cols = [
	'Filial',
	'valor_compra',
	'CPF NA NOTA?',
	'Imposto',
	'nome',
	'Tipo de Mercadoria']

df = pd.read_csv('_Desafio 2.0 - Relatório - Dados - Questão 1.csv',
	encoding='UTF-8', usecols=cols)

column_string = ['nome', 'Filial', 'Tipo de Mercadoria']


def convert_currency(val):
	"""
	Convert the string number value to a float
		- Remove R$
		- Remove commas
		- Convert to float type

	"""
	new_val = val.replace(',', '').replace('R$', '')
	return float(new_val)


# converter colunas para os respectivos valores
df['valor_compra'] = df['valor_compra'].apply(convert_currency).astype('float')
df['Imposto'] = df['Imposto'].apply(convert_currency).astype('float')
df[column_string] = df[column_string].astype('string')
df['CPF NA NOTA?'] = df['CPF NA NOTA?'].apply(lambda x: x.replace('Na~o', 'Não')).astype('string')

# Filtrando lojas
store1 = df.groupby('Filial').sum()
# print(store1)

# As Unidades que masi venderam
stores = df['Filial'].loc[[0, 24, 5]].values
store_total = df.groupby('Filial').agg({'valor_compra': sum}).values

x = stores
y = np.array(store_total.reshape(-1))

plt.title('Unidade que mais gerou lucro', loc='center')
plt.bar(x, y, color = 'red')
plt.ylabel('Valor')
plt.xlabel('Unidades')
plt.show()

# porcentagem de CPF
cont_x = 0
cont_y = 0
for x in df.index:
	if df.loc[x]['CPF NA NOTA?'] == 'Sim':
		cont_x += 1
		cpf_yes = cont_x
	else:
		cont_y += 1
		cpf_no = cont_y

total_cpf = math.ceil(cpf_yes / 100)
total_no_cpf = math.ceil(cpf_no / 100)

y = [total_cpf, total_no_cpf]
mylabels = ['Sim', 'Não']
mycolors = ['c', 'r']
myexplode = [0.2, 0]

# print('O valor em porcentagem de cpf: {}%'.format(total_cpf))
plt.pie(
	y,
	labels=mylabels,
	colors=mycolors,
	explode=myexplode,
	autopct='%1.1f%%',
	shadow=True
)
plt.title('Porcentagem de CPF', loc='center', fontsize=30)
plt.legend(title='% De CPFs NA NOTA:', loc='upper right')
plt.xlabel('Sim: {}\nNão: {}'.format(cpf_yes, cpf_no))
plt.show()

# porcentagem de Imposto
tax = df.agg({'Imposto': sum})
total_tax = math.ceil(tax / 100)

y = [total_tax]
mylabel = ['Imposto']

plt.pie(y, autopct='%1.1f%%', labels=mylabel)
plt.title('Porcentagem de Imposto', loc='center', fontsize=30)
plt.xlabel('Valor de Imposto: {}'.format(total_tax))
plt.show()
