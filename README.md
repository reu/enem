# ENEM
A proposta do projeto é poder visualizar os dados dos ENEMS de forma comparar escolas, cidades e estados entre si.

Por hora, apenas a cidade de São Paulo está sendo contemplada.

## Instalação

`pip install -r requirements.txt`

## Importando dados

Primeiro é necessário importar a lista de escolas da cidade de São Paulo:

`python -m enem.importer --schools data/schools-sp.csv`

Em seguida, importe os resultados do ENEM:

`python -m enem.importer --enem <microdata-do-enem.txt>`
