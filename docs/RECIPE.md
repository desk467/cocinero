# Recipe

O cocinero utiliza recipes e repositórios de template para a criação de novos projetos. Uma recipe é um arquivo .yml apontando quais os arquivos devem ser
modificados para a criação de um projeto. O arquivo se parece com isso:

```yaml

---
recipe:
  requirements:
    - python
    - poetry
  steps: 
    - name: Editar os arquivos com o nome do novo projeto
      files:
        path: app.py
        replace:
          from: webservicepython
          to: "$name"
    - name: Instalar as dependências
      execute: poetry install
```

~ em desenvolvimento ~