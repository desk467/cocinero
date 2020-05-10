# cocinero

cocinero é um utilitário escrito em Python para facilitar a geração de projetos novos a partir de boilerplates. Este projeto permite:

- Criar novos projetos a partir de um repositório base
- Verificar no ambiente do usuário se ele possui todos os requisitos para criar/executar um projeto
- Executar tarefas pré-definidas em cima dos novos projetos 

## Instalação

Para instalar o cocinero, você pode utilizar tanto o pip, quanto o pipx, executando:

```bash
pip install cocinero
```

ou ...

```bash
pipx install cocinero
```

Para utilizar boilerplates oriundos do GitHub, você também precisa instalar o git.


## Como usar 

Após instalado, para criar um novo projeto com o cocinero, execute:

```bash
cocinero cook github.com/des467/webservicepython meu_novo_projeto_incrivel
```

O comando acima irá:
- Clonar o repositório template passado
- Ler o arquivo `cocinero-recipe.yml` na raiz do repositório e a partir daí..
- .. gerar o seu incrível projeto.

Para ver mais informações sobre como criar `recipes`, [clique aqui](docs/RECIPE.md).

## Como contribuir

Veja como contribuir [clicando aqui](docs/CONTRIBUTING.md).

## Licença

Este projeto utiliza a licença GPL v3. Para ver mais sobre a licença, [clique aqui](docs/LICENSE.md)