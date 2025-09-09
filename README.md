# Trabalho Comunicação Entre Processos (IPC)


## Arquitetura

A aplicação foi desenvolvida com uma arquitetura que separa a lógica do backend da interface do usuário (frontend):

* Backend: Desenvolvido em C++, responsável por toda a lógica de criação de processos e pela implementação dos mecanismos de IPC. [
* Frontend: Uma interface gráfica de usuário desenvolvida em Python com a biblioteca Tkinter. É responsável por controlar a execução do backend e exibir o fluxo de dados em tempo real. 

A comunicação entre o frontend e o backend é feita através da execução de processos e da captura de suas saídas de texto.

## Mecanismos de IPC Implementados

A ferramenta permite ao usuário selecionar e testar os seguintes mecanismos de IPC:

1.  Pipes Anônimos: Demonstra a comunicação unidirecional entre um processo-pai e um processo-filho.
2.  Sockets (Locais): Demonstra a comunicação bidirecional cliente-servidor entre processos não relacionados na mesma máquina.
3.  Memória Compartilhada: Demonstra a comunicação de alta velocidade onde processos distintos acessam a mesma região de memória, com o acesso sincronizado por um Mutex para evitar condições de corrida. 

## Como Compilar e Executar

1. Compilar o Backend (C++)

	1.  Navegue até a pasta `solucao/` (ou a pasta que contém o arquivo `.sln`).
	2.  Abra o arquivo de Solução (`SolucaoIPC.sln`) no Visual Studio.
	3.  Certifique-se de que a configuração de compilação está como `Debug` e a plataforma como `x64`.
	4.  No menu superior, vá em **Compilar > Recompilar Solução**.
	5.  Isso irá gerar todos os 6+ arquivos `.exe` necessários na pasta de saída (ex: `solucao/x64/Debug/`).

2. Executar a Aplicação

	1.  Após a compilação, copie todos os arquivos `.exe` gerados para a pasta `executaveis/`.
	2.  Abra um terminal ou Prompt de Comando.
	3.  Navegue até a pasta `frontend/` usando o comando `cd`.
	4.  Execute o seguinte comando: py main.py
	5.  A interface gráfica será iniciada, e você poderá selecionar o modo de IPC e executar as ações.

## Autora

* Kailaine Kovalski