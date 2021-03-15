# Desafio lendico
Repositório para desafio Lendico para vaga de Engenheiro de dados.

## INFO
 - Tanto para Problemas 1 e 2 foram gerados arquivos .json (pela estrutura do GET/API), entretanto foram quebrados em estrutura tabular para fins de análises.
 - Ambos os problemas foram feitos no mesmo script para manter o processamento da memória de DataFrames.
 - Saídas .json para ambos os GETs por conta do armazenamento RAW da informação.
 - SQLite e .csv utilizados para "simular" uma situação de bancos de dados estruturados.

## API_KEY
 - <b>Criar um arquivo chamado "api.key" com conteúdo somente da API_KEY.</b>
 - <b>Ex: Colocar "RGAPI-XXXXX..."</b>

## Inicializar script
 - Script em Jupyter Notebook "pipeline_masters.ipynb" contém o script para rodar em Jupyter.
 - Script em arquivo Python "/DAG_script/scripts_lol_masters.py" contém o script em Python.
 - Ambos são os mesmos scripts, entretanto só é necessário mudar caminhos, se necessário.

## Visualizações:
 - Link da visualização ao fim do README.md (Power BI link)
 - Visualização em .ipynb também existe caso a primeira opção de erro! "summoner_visualization.ipynb"
 - Ou o .pbix (arquivo power BI) para visualização "summoner_visualization.pbix"

## Produção/Airflow
Para uso em produção/Airflow, uso da pasta DAG_script/

## Dataflow
 - [FLOW] <b>pipeline_masters.ipynb -> Power BI</b>
 - [FLOW 2] <b>DAG_script/scripts_lol_masters.py + DAG_script/DAG.py -> Power BI</b>

![alt text](https://github.com/ShigueruHosoya/data_eng_lendico/blob/main/riotapi.png)


## Online Visualization Link / Link da visualização Online:

[Power BI Online](https://app.powerbi.com/reportEmbed?reportId=ba0ab76e-26e3-4416-96e2-a5cc57dc6f82&autoAuth=true&ctid=567ca50b-f198-4b11-bf79-f378e335c9c0&config=eyJjbHVzdGVyVXJsIjoiaHR0cHM6Ly93YWJpLXNvdXRoLWNlbnRyYWwtdXMtcmVkaXJlY3QuYW5hbHlzaXMud2luZG93cy5uZXQvIn0%3D)
