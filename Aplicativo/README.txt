O aplicativo roda por meio de uma biblioteca de Python chamada Kivy, porém fazer um aplicativo mobile em python se mostrou um ponto bem mais problemático do que imaginei.

Algumas funções como permissões de uso de hardware, comunicação Bluetooth com perfil de porta serial, envio de emails e uso de bibliotecas python se mostraram extremamente complicada, o que impossibilitou algumas funções.

**Permissões de uso de hardware**

Foi possível implementar a função de pedir permissão para o usuário para o uso de câmera e arquivos, assim foi possível tirar as fotos e salvar o CSV de notas no final das capturas.

**Bluetooth**

Por conta da forma que o bluetooth foi utilizado no esp, o formato de comunicação é muito complexo para a implementação através de python e a biblioteca Kivy, então o aplicativo não tinha capacidade de se conectar ao ESP 32 e controlar o fluxo de folhas.

**envio de emails**

Por causa das diretrizes de segurança, o envio de email através de um aplicativo exige uma série de processamentos e permissões que foram, novamente, incapacitadas pelas limitações de se fazer um aplicativo exclusivamente com python kivy para mobile.

**bibliotecas python**

Por conta de algumas bibliotecas python exigirem uma instalação mais complexa para rodarem no dispositivo android, não consegui achar uma forma de implementar a biblioteca CV2 no meu aplicativo sem gerar crashes, o que impossibilitou a integração do sistema de correção com o aplicativo em si.


Por fim o applicativo tira uma foto a cara 0.5 segundos e cria um csv onde estariam as notas processadas.
