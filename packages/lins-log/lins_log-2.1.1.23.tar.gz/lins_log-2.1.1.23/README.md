# Pacote Logs #

Pacote para Utilizar o Graylog em serviços e apis.

## Variaveis de Ambiente Necessárias

> ### GRAYLOG_EXTRA_RECORDS
>> Parametro necessário para adicionar novos campos no log do graylog.
Exemplo:
    'settings=NODO:teste22,application=SERVICO:'
Definição:
    settings -> representa nome do campo
    NODO     -> representa variavel de ambiente que sera traduzida
    teste22  -> representa o valor padrão caso não haja a variavel de ambiente

> ### NODO
>> Parametro necessário para saber onde esta alocado o serviço exemplo: NODO={{.Node.Hostname}}

> ### SERVICO
>> Parametro necessário para saber qual servico exemplo: SERVICO={{.Service.Name}}

> ### EMPRESA
>> Parametro necessário para saber qual empresa exemplo: Pompeia

> ### APLICACAO
>> Parametro para ser preenchido sempre com o nome do repositório para facilitar a identificação e padronização

> ### SETTINGS
>> Parametro para ser preenchido PRODUCTION ou SANDBOX.

> ### IMAGE
>> Parametro para ser preenchido a image {{.service.name}}

> ### GRAYLOG_HOST
>> Parametro necessário para conectar no GrayLog

> ### GRAYLOG_PORT
>> Parametro necessário para conectar no GrayLog

## Variaveis de Ambiente Opcionais

> ### GRAYLOG_LEVEL
>> Parametro para determinar apartir de qual level vai ser impresso no graylog

## Como Utilizar Pacote em servico

> ### importa pacote from lins_log import lins_log
>> Nas chamadas utilizar logging do python pois pacote importa as configurações do logging

## Como Utilizar Pacote em Api

> ### importa pacote from lins_log import lins_log dentro dos settings
>> nos settings informar LOGGING = None e LOGGING_CONFIG = None