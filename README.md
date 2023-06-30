# Corretor automático de avaliações.
Aluno: José Henrique Schmitt Fidelis
Orientadores: Daniel Lohmann e Robinson Pizzio.
Unidade Curricular: Projeto Integrador 3.


## Problemática:

Correção de provas ocupa grande parte do tempo de professores fora da sala de aula, ocasionando em estresse desnecessário e perda de produtividade. Soluções para tornar esta correção automática geralmente são ou muito lentas ou muito caras.

## Solução:

A ideia para uma solução seria um corretor automático para uma quantidade significativa de provas e que não use de tecnologias muito custosas. 

O conceito inicial do projeto consiste em uma base capaz de folhear um bloco de avaliações uma de cada vez, tendo seu tempo devidamente ajustado. Acima desta base ficará uma câmera posicionada para a leitura das avaliações, sendo a primeira folha o gabarito, e mostrando o calculo da nota do aluno e sua devida identificação em um display. Para garantir em casos de possíveis erros, as imagens das folhas serão guardadas.

A ideia para cumprir o papel de câmera e display seria utilizar um celular comunicando via bluetooth com o microcontrolador.

## Especificações:



|Especificação| Quantidade |
| ------ | ------ |
| Folhas por minuto | 10 |
| Número de avaliações | 50 |
| Número máximo de questões | 10 |
| Número máximo de alternativas | 5 |

|Requisitos | Quantidade |
| ------ | ------ |
| Motor para posicionamento de folhas  | 1 |
| Braço para segurar celular  | 1 |
| Celular | 1 |
| Microcontrolador ESP32| 1 |
| Fonte 12V | 1 |
| Rele 3.3V | 1 |


-Fluxograma:

![image](https://user-images.githubusercontent.com/53865438/229185109-7d6e3861-be5d-499c-980a-882d6897b697.png)



## Cronograma:

|Tarefa | data limite | status |
| ------ | ------ | ------ |
| Montagem de diagrama de blocos  | 31/03/23 | Concluída |
| Adquirir base para o protótipo | 14/04/23 | Conluída |
| Escolher componentes | 28/04/23 | Concluída |
| Testes na estrutura da base | 05/05/23 | Concluída |
| Projetar ajustes na base | 12/05/23 | Concluída |
| Testes dos ajustes da base | 19/05/23 | Concluída |
| Programação do microcontrolador da base | 09/06/23 | Concluída |
| Programação do aplicativo no celular | 16/06/23 | Em execução |
| Ajustes e correções restantes | 23/06/23 | Em execução |

## Base adquirida:

Consegui uma impressora/copiadora de uma loja e por sorte apenas o sistema de impressão estava danificado, porém o sistema de transporte das folhas estava intacto.
O modelo era HP photosmart C4480, uma impressora, scanner e copiadora:

![image](https://github.com/Zex1011/Pi3-Fidelis-2023_1/assets/53865438/ec78a227-f2af-4f1b-a249-14afeeb9a592)

Então, parti para o processo de desmontar os sistemas que eu não usaria, tirando assim partes como a eletrônica, o motor e o sistema de tintas, o display, e toda a parte relacionada a escaneamento de folhas, deixando assim praticamente apenas peças relacionadas a movimentar a folha pelo trajeto de impressão.

Imagem das peças retiradas:
![WhatsApp Image 2023-06-16 at 12 03 49](https://github.com/Zex1011/Pi3-Fidelis-2023_1/assets/53865438/efac297b-f3e5-4a64-9b57-9a9f957746b7)

Impressora apenas com as partes necessárias:
![WhatsApp Image 2023-06-16 at 12 05 39](https://github.com/Zex1011/Pi3-Fidelis-2023_1/assets/53865438/0bc5d6dc-fcc8-4df2-8bcd-29fce7920337)

## Teste da base:
Testei a velocidade com que o motor movimentava as folhas alterando a tensão, e por fim 5V ficou dentro da faixa de rápido o suficiente para a folha conseguir fazer todo o trajeto, porém lento o suficiente para que as chances de algo travar as folhas serem mais baixas. Assim ficou decidido que usarei uma fonte de 5V, tanto para alimentar o motor, quanto para alimentar o microcontrolador do protótipo.

## Controle da base:

A ideia é que o aplicativo de correção consiga operar a impressora, dessa forma quando alguma leitura for defeituosa, o aplicativo irá segurar a folha no lugar até que a leitura e correção tenham sucesso.
Para isso, decidi utilizar comunicação bluetooth, de forma que o aplicativo se comunique com um microcontrolador e diga se este deve parar ou continuar a passagem de folhas. Na ideia original, eu utilizaria um microcontrolador mais simples, porém isso exigiria que eu comprasse um módulo bluetooth confiável, e como o preço de um módulo ficou alto, optei por comprar um ESP32, que está na mesma faixa de preço, ja possui bluetooth presente e é mais simples de se programar.

Módulo ESP32: 
![WhatsApp Image 2023-06-16 at 12 16 52](https://github.com/Zex1011/Pi3-Fidelis-2023_1/assets/53865438/d34b65b4-fad9-4bb7-a2a4-982a3c982e13)

Além disso, obtive um relé de 3V para o acionamento com os pinos lógicos do ESP, então fiz uma placa de circuito impreso que permite que o ESP forneça 5V para a impressora quando ele recebe um sinal via bluetooth.

## Alterações e testes na base:

A programação do microcontrolador está completa e ele é capaz de acionar o relé quando recebe um sinal de bluetooth. Isso faz com que o sistema de controlar as folhas funcione como desejado.
Outro fator que foi resolvido era posicionar as folhas na saída de forma que ficassem retas o suficientes para terem suas fotos tiradas. Foi colocado uma extensão simples para a base, utilizando madeira, de forma que as folhas se apoiem facilmente por sima dela e consigam manter o padrão de sempre ficarem em cima da anterior

## Sistema de correção:

Um apoio para o celular se manter em cima das folhas a todo o momento será utilizado, e o aplicativo será programado em python.
O objetivo do aplicativo é:
- Tirar as fotos e analisa-las, caso a foto seja de uma prova que ja foi lida e processada, não será necessário salva-la.
- Caso o processamento tenha falhas, enviar um sinal de espera para a base, se forma que as folhas parem para uma captura melhor.
- Assim que a captura for concluída e verificada, enviar sinal de continuação para a base, partindo assim para a próxima prova.




