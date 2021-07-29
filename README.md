<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url] [![Forks][forks-shield]][forks-url] [![Stargazers][stars-shield]][stars-url] [![Issues][issues-shield]][issues-url] [![MIT License][license-shield]][license-url] [![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/juliocezarpaiva/to_ligado">
    <img src="static/img/core-img/to_ligado_novo.svg" alt="Logo" width="150">
  </a>

  <p align="center">
    Procure e encontre ações. Configure limites de preço e alertas. Fique ON e atinja um novo patamar financeiro!
    <br />
    <a href="https://github.com/juliocezarpaiva/to_ligado/README.md"><strong>Read the docs!</strong></a>
    <br />
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Sumário</summary>
  <ol>
    <li>
      <a href="#about-the-project">Sobre</a>
      <ul>
        <li><a href="#built-with">Feito com</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Começando</a>
      <ul>
        <li><a href="#prerequisites">Pré requisitos</a></li>
        <li><a href="#installation">Instalação</a></li>
      </ul>
    </li>
    <li><a href="#usage">Uso</a></li>
    <li><a href="#license">Licença</a></li>
    <li><a href="#contact">Contato</a></li>
    <li><a href="#acknowledgements">Créditos</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
<a id="about-the-project"></a>
## Sobre

Este é um projeto desenvolvido para o desafio do PS da [Inoa](https://www.inoa.com.br/).

O que esse projeto é capaz de fazer:
* Procurar ações filtrando as buscas pela B3 ou globalmente
* Listar todas as ações encontradas oferecendo informações básicas sobre cada uma delas
* Exibir uma dashboard única para cada ação encontrada
* Configurar limites superior e inferior de preços usados para enviar alertas para o seu email
* Configurar um intervalo de tempo para que o monitorador de preços cheque se suas ações atingiram os preços que você estipulou
* Exibir informações gerais sobre o mercado

Emails simplesmente BONITAÇOS

![Email Screenshot][mail-screenshot]

E um fluxo simples e intuitivo

![TôLigado! Screenshot][product-screenshot]

Os principais recursos que usei para fazer esse projeto estão listados nos créditos.

<!-- BUILT WITH -->
<a id="built-with"></a>
### Feito com

* [Python](https://www.python.org/)
* [Django](https://www.djangoproject.com/)
* [Bootstrap](https://getbootstrap.com/)

<!-- GETTING STARTED -->
<a id="getting-started"></a>
## Começando

Baixe o projeto e rode ele localmente na sua máquina

<!-- PREREQUISITES -->
<a id="prerequisites"></a>
### Pré requisitos

Você precisa instalar algumas ferramentas antes de começar
* git
    Tenha certeza de que você consegue executar comandos git. Caso não tenha a ferramente instalada, você pode baixá-la [aqui](https://git-scm.com/downloads).
* python3
    Você também precisa ter o python3 instalado em sua máquina. Caso não tenha, você pode baixar o python [aqui](https://www.python.org/downloads/).
* pip3
    Se por algum motivo, você não tem o pip3 instalado, então você precisa baixar ele.
    Em distribuições Debian-based é fácil instalar o pip3 rodando:
    ```sh
    sudo apt-get install python3-pip
    ```

<!-- INSTALLATION -->
<a id="installation"></a>
### Baixando e configurando o projeto

1. Consiga uma API Key de graça [aqui](https://rapidapi.com/apidojo/api/yahoo-finance1/).
2. Clone o repo e entre no diretório dele:
   ```sh
   git clone https://github.com/juliocezarpaiva/to_ligado.git && cd to_ligado
   ```
3. Instale as libs Python usadas no projeto com:
   ```sh
   pip3 install -r requirements.txt
   ```
4. Renomeie o arquivo .env_example como .env e configure suas informações e a API Key:
   ```Python
    # django-background-tasks configs:
    MAX_ATTEMPTS = 25
    MAX_RUN_TIME = 3600
    BACKGROUND_TASK_RUN_ASYNC = True
    # BACKGROUND_TASK_ASYNC_THREADS = 4
    # BACKGROUND_TASK_PRIORITY_ORDERING = 'ASC'

    # djang-mail configs:
    EMAIL_HOST = 'smtp.seuhost.com'
    EMAIL_USE_TLS = True ou False (depende do seu host)
    EMAIL_PORT = porta SMTP do seu host
    EMAIL_HOST_USER = 'seu-email@seuhost.com'
    EMAIL_HOST_PASSWORD = 'sua-senha'

    # api key
    X_RAPIDAPI_KEY = 'sua-chave-api'
    X_RAPIDAPI_HOST = 'apidojo-yahoo-finance-v1.p.rapidapi.com'
   ```
5. Migre as bases de dados do projeto
    ```sh
    python3 manage.py migrate
    ```



<!-- USAGE -->
<a id="usage"></a>
## Rodando o projeto

Para rodar o projeto, você vai precisar executar duas tarefas:   
* runserver: é o servidor base do seu projeto.
    ```sh
    python3 manage.py runserver
    ```

* process_tasks: é o agendador de tarefas de atualização e notificação.
    ```sh
    python3 manage.py process_tasks
    ```

Agora você já consegue acessar o projeto pelo seu navegador em [localhost:8000](localhost:8000)

Você também pode passar a porta de acesso como parâmetro do seu comando runserver rodando
```sh
python3 manage.py runserver PORTA
```
ao invés de rodar o comando runserver sem parâmetros.


<!-- LICENSE -->
<a id="license"></a>
## Licença

Distribuído sob a MIT License. Veja `LICENSE.txt` para mais detalhes.

<!-- CONTACT -->
<a id="contact"></a>
## Contato

Julio Cezar Paiva | [linkedin](https://www.linkedin.com/in/jcezarpaiva16/) | juliocezarpaiva@gmail.com

Link do projeto: [https://github.com/juliocezarpaiva/to_ligado](https://github.com/juliocezarpaiva/to_ligado)



<!-- ACKNOWLEDGEMENTS -->
<a id="acknowledgements"></a>
## Créditos
* [Choose an Open Source License](https://choosealicense.com)
* [Django](https://www.djangoproject.com/)
* [decouple](https://github.com/henriquebastos/python-decouple)
* [Bootstrap](https://getbootstrap.com/)
* [Django Background Tasks](https://django-background-tasks.readthedocs.io/en/latest/#)
* [Alura](https://cursos.alura.com.br/)
* [Rapid API](https://rapidapi.com/)
* [Yahoo! Finance](https://finance.yahoo.com/)
* [Vector Magic](https://pt.vectormagic.com/)
* [Adobe Photoshop](https://www.adobe.com/br/products/photoshop.html)





<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/juliocezarpaiva/to_ligado.svg?style=for-the-badge
[contributors-url]: https://github.com/juliocezarpaiva/to_ligado/graphs/contributors

[forks-shield]: https://img.shields.io/github/forks/juliocezarpaiva/to_ligado.svg?style=for-the-badge
[forks-url]: https://github.com/juliocezarpaiva/to_ligado/network/members

[stars-shield]: https://img.shields.io/github/stars/juliocezarpaiva/to_ligado.svg?style=for-the-badge
[stars-url]: https://github.com/juliocezarpaiva/to_ligado/stargazers

[issues-shield]: https://img.shields.io/github/issues/juliocezarpaiva/to_ligado.svg?style=for-the-badge
[issues-url]: https://github.com/juliocezarpaiva/to_ligado/issues

[license-shield]: https://img.shields.io/github/license/juliocezarpaiva/to_ligado.svg?style=for-the-badge
[license-url]: https://github.com/juliocezarpaiva/to_ligado/blob/master/LICENSE.txt

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/jcezarpaiva16/

[product-screenshot]: static/img/to_ligado_usage.gif
[mail-screenshot]: static/img/email_sample.png
