# Desenvolvimento #

O desenvolvimento deste projeto segue algumas regras e convenções
básicas. Como 'estilo de formatação de código',

## Código de conduta ##
Detalhes em [docs/code_of_conduct.md](extras/code_of_conduct.md)

## Padrões aplicados ##
Este projeto segue as recomendações
[Zen do Python (docs/extra/zenpy.md)](extras/zenpy.md) e
[PEP-8](https://pep8.org/), e as orientações de
[Versionamento Semântico (SemVer)](https://semver.org/lang/pt-BR/).
Além das [Regras de git Commit (docs/COMMITS.md)](COMMITS.md).


## Qualidade de Código ##
É utilizado de ferramentas validadoras de qualidade de código estático,
também denominadas linters.
Há uso das seguinte:
- black
- flake8
- isort
- mypy
- pydocstyle
- pylint

## Segurança ##
Também há preocupação com a segurança do código implementado, o pacote
`safety` é utilizado para monitoramento de pacotes.

### black ###
O `black` é classificado como Autoformator, são programas que
refatoram seu código para se adequar ao PEP 8 automaticamente.
```shell
black --check incolumepy tests
```
### flake8 ###
O `Flake8` é um envolucro que contém: PyFlakes, pycodestyle, McCabe.
```shell
flake8 incolumepy tests
```
### isort ###
O `isort` é um utilitário para classificar as importações
em ordem alfabética e separadas automaticamente em seções e por tipo.
```shell
isort incolumepy tests
```
### mypy ###
O `Mypy` é essencialmente um analizador de código estático melhorado e com
verificador de tipos, que pode detectar muitos erros de programação
analisando o código, sem precisar executá-lo.
Ele possui um poderoso sistema de tipos com recursos como
inferência de tipos, digitação gradual, genéricos e tipos de união.
```shell
mypy incolumepy
```
### pydocstyle ###
O `pydocstyle` é uma ferramenta de análise estática para verificar a
conformidade com as convenções docstring do Python. Ele suporta a maior
parte do PEP 257, entretanto não deve ser considerado uma
implementação de referência.
```shell
pydocstyle incolumepy tests
```
### pylint ###
O `Pylint` é uma ferramenta de análise de código estático do Python
que procura erros de programação, ajuda a impor um padrão de codificação,
detecta cheiros de código e oferece sugestões simples de refatoração.
É altamente configurável, possuindo pragmas especiais para controlar
seus erros e avisos de dentro do seu código, bem como de um extenso
arquivo de configuração. Também é possível escrever seus próprios plugins
para adicionar suas próprias verificações ou para estender o `pylint`
de uma forma ou de outra.
```shell
pylint incolumepy tests
```
### safety ###
O `safety` verifica as dependências instaladas quanto a vulnerabilidades
de segurança conhecidas.
Por padrão, ele usa o banco de dados de vulnerabilidades Python aberto
[Safety DB](https://github.com/pyupio/safety-db).
```shell
safety check
```

## Ferramentas de Automação ##
Para facilitar o trabalho, várias das tarefas estão automatizadas pelo
githooks, e/ou Makefile, e/ou tox.

### Tox ###

#### Verificação básica ####

Na Verificação básica engloba:
- black
- isort
- pydocstyle
- flake8
- mypy
- pylint
- py36
- py37
- py38
- py39
- py310

```shell
tox
```
#### Verificação dos testes com as versões python disponíveis ####
```shell
tox -e py36,py37,py38,py39,py310
```
#### Verificação de três linters apenas no em um módulo ####
```shell
tox -e pydocstyle,black,isort -- -k incolumepy/lex/sanitize.py
```

#### Verificação de todos os linters configurados ####
```shell
tox -e linters
```

#### Verificação e relatório de cobertura ####
```shell
tox -e stats
```

#### Verificação resumida de segurança ####
```shell
tox -e safety
```

#### Execução completa ####
Executa todas as verificações diponíveis contidas no `tox`.
```shell
tox -e ALL
```

### Makefile ###
O `Makefile` foi personalizado para rodar com as opções necessárias.
Com o help você verá todas as opções.
```shell
make help
```
#### Iniciar ambiente dev ####
Através do `Makefile`, pode-se criar um ambiente virtual para o projeto,
conforme a versão python predefinida, instalando todas as dependências
necessárias, além de ativar as configurações em passos simples.

```shell
make install;
poetry shell
```

#### Limpeza básica do ambiente
Limpeza de arquivos temporários, logs, compilados e afins.
```shell
make clean
```

#### Limpeza profunda do ambiente
Além da limpeza básica, são removidos dist, build, htmlcov, .tox, *_cache,
e outros conteúdos gerados pelas ferramentas de desenvolvimento.
```shell
make clean-all
```

#### Gerar a documentação atualizada
```shell
make docsgen
```

#### Verificação de segurança e exposição de motivos
```shell
make safety
```
