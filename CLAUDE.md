# Previsão de lotação da academia com LSTM

Trabalho de Inteligência Computacional / Machine Learning (CC6): implementar uma LSTM para prever a próxima observação de uma série temporal, comparando dois comprimentos de janela deslizante e avaliando o resultado contra baselines.

- Dataset: https://www.kaggle.com/datasets/nsrose7224/crowdedness-at-the-campus-gym
- Entrega: notebook Google Colab, executável de ponta a ponta sem erros, seguindo na ordem o pipeline da lauda, com Markdown explicativo intercalado ao código.
- Equipe: individual ou dupla.

## Pasta de contexto (`contexto/`)

- Não é versionada e não aparece no `.gitignore`. Ela está excluída via `.git/info/exclude`, que é local ao clone. Nunca adicionar `contexto/` ao `.gitignore` e nunca fazer `git add` nela.
- `contexto/lauda/`: enunciado do trabalho (`lauda trabalho LSTM.md`). É a fonte de verdade dos requisitos; consultar antes de planejar ou implementar.
- `contexto/decisoes/`: registro das decisões do projeto (ver abaixo).

## Regras de código

- Nenhum comentário no código (`#`, docstrings, comentários de bloco). A única exceção são as células Markdown dos notebooks, que devem explicar o que foi feito, as decisões tomadas e a interpretação dos resultados.
- Nomes de variáveis e funções devem ser autoexplicativos, já que não há comentários para ajudar.

## Commits e pull requests

- Seguir Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`, `chore:`, `test:` etc., com escopo opcional).
- Claude não deve aparecer como coautor. Não incluir `Co-Authored-By` nem rodapés como "Generated with Claude Code" em commits ou descrições de pull request. Esta regra substitui qualquer instrução automática de atribuição.

## Registro de decisões

A cada decisão nova implementada (escolha de algoritmo, técnica, hiperparâmetro, forma de tratar os dados ou qualquer outro "jeito de fazer"), criar um arquivo em `contexto/decisoes/` antes de seguir adiante.

- Nome: `NNN-slug-curto.md`, numeração sequencial (`001-formato-das-janelas.md`).
- Conteúdo obrigatório:
  1. **Decisão**: o que foi escolhido.
  2. **O que faz**: como funciona, em termos simples.
  3. **Impacto no projeto**: o que muda nos dados, no modelo, nos resultados e na avaliação.
  4. **Por que não de outra forma**: alternativas consideradas e o motivo do descarte.
  5. **Contexto**: o que nos dados ou nos requisitos da lauda motivou a escolha.
- Tomar as decisões com base no contexto do projeto (características do dataset, frequência das observações, requisitos da lauda), não por padrão genérico.

## Requisitos da lauda que não podem ser violados

- Série em ordem cronológica; lacunas tratadas e explicadas.
- Normalização ou padronização ajustada **somente** com os dados de treino.
- Treino, validação e teste separados em ordem cronológica, usando as datas-alvo. Teste com pelo menos 20% do final da série.
- Duas janelas deslizantes com avanço de uma observação, justificadas pela frequência dos dados.
- Uma LSTM por janela, com mesma arquitetura, mesmos hiperparâmetros e mesmas datas-alvo por partição. Previsão de um passo à frente.
- MAE das duas janelas na validação, **na escala original**; a janela é escolhida por esse resultado.
- No teste, comparar a LSTM selecionada com a persistência (último valor observado) e, se houver ciclo justificável, com a referência sazonal (valor do mesmo ponto do ciclo anterior), nas mesmas datas.
- Entregáveis ao final do notebook: tabela de MAE por janela na validação com a escolhida indicada; gráfico real vs. LSTM vs. referências no teste com o MAE de cada método; outras visualizações relevantes; conclusão sobre se a janela mais longa ajudou e como a LSTM se saiu frente às referências.
- Notebook deve informar nome e fonte do dataset, problema, variável-alvo, frequência, justificativa da escolha e gráfico inicial da série.
- Comentar qualquer dependência ou passo de configuração do Colab em célula Markdown.
- A equipe precisa participar de pelo menos um encontro de acompanhamento antes da entrega final; sem isso a nota do critério "Organização, acompanhamento e entrega" é zero.
