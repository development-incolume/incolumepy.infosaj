========
EXAMPLES
========

A API incolumepy.lex, permite agregar funcionalidades para tratamento do
conteúdo em tempo de execução, desde que o comportamento agregado seja do
tipo incolumepy.lex.behavior.

Salvar conteúdo web
====================


.. code-block:: python
    :linenos:
    :emphasize-lines: 6,11,13

    import requests
    import tempfile
    from pathlib import Path
    from bs4 import BeautifulSoup
    from incolumepy.lex.fons_lex import FonsLexHOF
    from incolumepy.lex.ibehaviors import SalvarHTMLascii

    req = requests.get('https://brito.blog.incolume.com.br/p/cores.html')
    soup = BeautifulSoup(req.content, 'html5lib')
    file = Path(tempfile.gettempdir()) / 'paleta_cores.html'
    a = FonsLexHOF(file, salvar_behavior=SalvarHTMLascii())
    a.content = soup
    a.salvar()

- Linha 6 importa o comportamento desejado para a ação de salvar;
- Linha 11 integra o comportamento ao objeto da FonsLexHOF;
- Linha 13 executa o comportamento associado;



Sanitizar ato de origem na Presidência da República
=======================================================

Previamente salve o arquivo dentro da pasta `CCIVIL_03`,
exemplo: http://planalto.gov.br/CCIVIL_03/decreto/1970-1979/D81800.htm

Para este exemplo, o arquivo foi salvo em `/tmp/CCIVIL_03`.

Salvar com substituição
--------------------------

.. code-block:: python
    :linenos:
    :emphasize-lines: 6,10,12-13

    import requests
    import tempfile
    from pathlib import Path
    from bs4 import BeautifulSoup
    from incolumepy.lex.fons_lex import FonsLexHOF
    from incolumepy.lex.ibehaviors import SalvarHTMLascii, SanitizarHTML


    file = Path(tempfile.gettempdir()) / 'CCIVIL_03'/'D81800.html'
    a = FonsLexHOF(file, salvar_behavior=SalvarHTMLascii(), sanitizar_behavior=SanitizarHTML())
    a.content = soup
    a.sanitizar()
    a.salvar()


Salvar sem substituição
--------------------------

.. code-block:: python
    :linenos:
    :emphasize-lines: 6,10,13-14

    import requests
    import tempfile
    from pathlib import Path
    from bs4 import BeautifulSoup
    from incolumepy.lex.fons_lex import FonsLexHOF
    from incolumepy.lex.ibehaviors import SalvarHTMLascii, SanitizarHTML


    file = Path(tempfile.gettempdir()) / 'CCIVIL_03'/'D81800.htm'
    a = FonsLexHOF(file, salvar_behavior=SalvarHTMLascii(), sanitizar_behavior=SanitizarHTML())
    a.content = soup
    a.filename_output = Path(tempfile.gettempdir()) / 'CCIVIL_03'/'D81800.html'
    a.sanitizar()
    a.salvar()



Comportamentos predefinidos
====================================
Alistagem de todos os comportamentos estão disponíveis na documentação da
API, em :doc:`../api`.

.. code-block:: python
    :linenos:
    :emphasize-lines: 26-35

    import requests
    from bs4 import BeautifulSoup
    import datetime as dt
    import logging
    import contextlib

    from incolumepy.lex.fons_lex import FonsLexHOF
    from incolumepy.lex.ibehaviors import (
        EstilizarStatusOkBehavior,
        FixMsgReeditado,
        FixMsgRevog,
        FormatarAutoriaNegrito,
        FormatarHTML,
        MetaDownloadAnexos,
        SalvarHTMLascii,
        SanitizarHTML,
        SetDefaultTitleHTML,
        SetTitleHTML,
        TextoImpressaoDestachado,
    )
    from incolumepy.lex.exceptions import MimeTypeError

    req = requests.get('http://localhost:8000/CCIVIL_03/MPV/Antigas/2011-7.htm')
    soup = BeautifulSoup(req.content, 'html5lib')
    behaviors = {
        "sanitizar_behavior": SanitizarHTML(),
        "formatar_behavior": FormatarHTML(),
        "fixar_msg_reedit_behavior": FixMsgReeditado(),
        "fixar_msg_revog_behavior": FixMsgRevog(),
        "textoimpressao_destachado_behavior": TextoImpressaoDestachado(),
        "estilizar_status_ok_behavior": EstilizarStatusOkBehavior(),
        "salvar_behavior": SalvarHTMLascii(),
        "formatar_autoria_behavior": FormatarAutoriaNegrito(),
        "formatar_title_behavior": SetTitleHTML(),
        "formatar_default_title_behavior": SetDefaultTitleHTML(),
    }
    path = 'CCIVIL_03/MPV/Antigas/2011-7.htm'
    file = acervo / path
    file.is_file()
    url = urljoin('http://localhost:8000', path)
    a = FonsLexHOF(file, **behaviors)
    a.filename_output = file
    a.sanitizar()
    a.formatar()
    a.fixar_msg_reedit()
    with contextlib.suppress(IndexError):
        a.fixar_msg_revog()
    a.textoimpressao_destachado()
    a.estilizar_status_ok()
    with contextlib.suppress(RecursionError):
        a.formatar_autoria()
    a.formatar_title()
    a.salvar()
    print(url)

- linha 26: Definido comportamento para sanitizar();
- linha 27: Definido comportamento para formatar();
- linha 28: Definido comportamento para fixar_msg_reedit();
- linha 29: Definido comportamento para fixar_msg_revog();
- linha 30: Definido comportamento para textoimpressao_destachado();
- linha 31: Definido comportamento para estilizar_status_ok();
- linha 32: Definido comportamento para salvar();
- linha 33: Definido comportamento para formatar_autoria();
- linha 34: Definido comportamento para formatar_title();
- linha 35: Definido comportamento para formatar_default_title();

Comportamentos personalizados
===================================


Comportamentos personalizados podem ser criados a partir da
:py:class:`incolumepy.lex.behaviors.Behavior`, com as funcionalidades
desejadas.


Criando comportatamento personalizado
--------------------------------------

.. code-block:: python
    :linenos:

    from incolumepy.lex.behaviors import Behavior
    from incolumepy.lex.fons_lex import FonsLexHOF

    class HelloWorld(Behavior):
        """Novo behavior."""
        def run(self, cls):
            """A funcionalidade deste behavior é imprimir 'hello world' no
                terminal."""
            print('hello world')

    a = FonsLexHOF('')
    a.say_hello_behavior = HelloWorld()
    a.say_hello()


Alterando comportamento em tempo de execução
-----------------------------------------------
Os comportamentos não existem até serem definidos na instância de trabalho.
E se porventura for executado um comportamento inexistente, será disparada
exceção `AttributeError: 'function' object has no attribute 'run'`.

.. code-block:: python
    :linenos:

    from incolumepy.lex.fons_lex import FonsLexHOF
    a = FonsLexHOF('')
    a.drive()

    Traceback (most recent call last):
      File "/../virtualenvs/incolumepy.lex-o8x7jvux-py3.10/lib/python3.10/site-packages/IPython/core/interactiveshell.py", line 3457, in run_code
        exec(code_obj, self.user_global_ns, self.user_ns)
      File "<ipython-input-48-b517ea4999a8>", line 1, in <module>
        a.drive()
      File "/../incolumepy.lex/incolumepy/lex/fons_lex.py", line 114, in wrap
        return getattr(f, "run")(self, *args, **kwargs)
    AttributeError: 'function' object has no attribute 'run'


Para garantir a existência do comportamento, há comportamentos modelos que
podem ser utilizados irestritamente.


.. code-block:: python
    :linenos:

    from incolumepy.lex.behaviors import Behavior
    from incolumepy.lex.ibehaviors import BehaviorNoApply
    from incolumepy.lex.fons_lex import FonsLexHOF

    class HelloWorld(Behavior):
        """Novo behavior."""
        def run(self, cls):
            """A funcionalidade deste behavior é imprimir 'hello world' no
                terminal."""
            print('hello world')

    a = FonsLexHOF('', say_hello_behavior = BehaviorNoApply())
    a.say_hello()    # Don't apply in this case

    a.say_hello_behavior = HelloWorld()
    a.say_hello()    # hello world

    a.drive_behavior = BehaviorNoApply()
    a.drive()    # Don't apply in this case
