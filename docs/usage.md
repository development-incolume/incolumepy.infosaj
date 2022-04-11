# UTILIZAÇÃO #

## Prerequisitos ##


- git client
- python 3.8+
- pyenv
- pip or poetry (preferencialmente)


## Instalação ##

To install it using poetry:

More detail can be see in [Python Poetry: Gerenciando dependências de projeto](https://brito.blog.incolume.com.br/2022/01/python-poetry-gerenciando-dependencias.html)

Last package version from pypi.org:
```shell
  poetry add incolumepy.infosaj
```
Download package wheel:
```shell
  poetry add incolumepy.infosaj-1.0.0-py3-none-any.whl
```
Download package tar.gz:
```shell
  poetry add incolumepy.infosaj-1.0.0.tar.gz
```
Last package version from git repo:
```shell
  poetry add git+https://gitlab.com/development-incolume/incolumepy.infosaj.git@master
```
Specific version from git repo:
```shell
  poetry add git+https://gitlab.com/development-incolume/incolumepy.infosaj.git@"1.0.0"
```
Specific branche from git repo:
```shell
  poetry add git+https://gitlab.com/development-incolume/incolumepy.infosaj.git@"enhacement/issue#10"
```


To install incolumepy.infosaj, using pip:

```shell
  pip install incolumepy.infosaj
```
```shell
pip install git+https://gitlab.com/development-incolume/incolumepy.infosaj.git@master
```
```shell
pip install incolumepy.infosaj.zip;    #or
pip install incolumepy.infosaj.tar.gz;    #or
pip install incolumepy.infosaj.whl

```

## Exemplos ##
Disponível em [docs/examples/EXAMPLES.rst](examples/EXAMPLES.rst)


## Detalhes da API ##

Disponível em [docs/api.rst](api)


## Detalhes para desenvolvimento ##
Disponível em [docs/development.md](development)
