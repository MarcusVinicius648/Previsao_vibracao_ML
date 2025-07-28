# Previsao_vibracao_ML
Software com algoritmo de machine learning focado na previsão de vibrações induzidas pelo desmonte de rocha com foco em aplicações na mineração .

📌 Objetivo:

O software foi projetado para auxiliar profissionais da área de engenharia de minas a estimar, de forma prática e precisa, a vibração máxima de partícula (PPV) causada por detonações, considerando variáveis como:
- Carga máxima por espera

- Distância até o ponto de medição

- Litologia local (tipo de rocha)

🧠 Algoritmo de Machine Learning:

O modelo utilizado é baseado em regressão linear logarítmica, uma técnica amplamente empregada para modelar relações empíricas entre variáveis geotécnicas. O algoritmo realiza os seguintes passos:

- Transformação logarítmica dos dados de entrada (distância, carga por espera e PPV).

- Treinamento do modelo de regressão linear com os dados tratados.

- Extração dos coeficientes empíricos (k e m) para cada litologia.

- Previsão da vibração com base em novos valores inseridos pelo usuário.

Essa abordagem permite adaptar os parâmetros do modelo de acordo com cada tipo de rocha, garantindo previsões mais robustas e adequadas à realidade local.

🖥️ O Software:

A aplicação foi desenvolvida com foco na usabilidade e praticidade, sendo dividida em duas interfaces principais:

- Tela de Previsão: permite ao usuário inserir os valores de carga por espera, distância e litologia, retornando a estimativa da vibração induzida.

- Tela de Gerenciamento de Dados: permite ao usuário alimentar o banco de dados com novas amostras manualmente ou por meio da importação de arquivos .csv ou .xlsx.

- O armazenamento é feito em um banco de dados SQLite local, que organiza os dados por litologia e facilita a reavaliação contínua dos parâmetros do modelo.


⚙️ Tecnologias Utilizadas:

- Python 3.x

- SQLite3

- Pandas, NumPy

- Scikit-learn

- Interface com bibliotecas de front-end (Tkinter, PyQt ou similar – ajustar conforme sua implementação)

📚 Aprendizado:

Este projeto foi desenvolvido como parte de um desafio acadêmico, envolvendo a resolução de problemas práticos relacionados a vibrações induzidas em desmontes, culminando na construção de uma ferramenta computacional completa. Ao longo do desenvolvimento, foram aplicados conhecimentos de mineração, estatística, programação e aprendizado de máquina, proporcionando uma experiência enriquecedora e multidisciplinar.
