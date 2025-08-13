  <p class="center">
    <img src="https://capsule-render.vercel.app/api?type=waving&color=8BE9FD&height=220&section=header&text=Hydrotop&fontSize=40&fontColor=F8F8F2" alt="Header" />
  </p>
Hydrotop é um monitor de sistema para terminal, escrito em Python, que exibe em tempo real métricas essenciais de hardware e processos, com uma interface TUI (Text User Interface) estilizada utilizando `curses`.



## Funcionalidades

*   Monitoramento de uso de CPU, memória RAM e disco.
*   Visualização da taxa de transferência de rede (download e upload).
*   Exibição dos processos mais consumidores de CPU.
*   Interface com caixas desenhadas em ASCII e uso de símbolos Nerd Fonts.
*   Atualização dinâmica a cada segundo.
*   Suporte a redimensionamento mínimo do terminal.

- - -

## Preview

![Screenshot](screenshot.png)

## Requisitos

*   Python 3.6 ou superior
*   Biblioteca `psutil` (para coleta das métricas do sistema)
*   Terminal compatível com `curses` (Linux, macOS, WSL)

> **Atenção:** Suporte oficial apenas para Linux, macOS e WSL. Usuários Windows podem tentar rodar instalando o pacote `windows-curses`, mas não há garantia de funcionamento ou suporte.

Instalação do `psutil`:

pip install psutil

- - -

## Uso

Execute o script diretamente pelo terminal:

python3 hydrotop.py

Pressione `q` para sair da aplicação.

- - -

## Estrutura do Código

*   Uso da biblioteca `curses` para criar a interface interativa.
*   Funções para desenhar caixas e barras de progresso coloridas.
*   Loop principal que atualiza as métricas em tempo real.
*   Tratamento para evitar erros ao desenhar em terminais pequenos.

- - -

## Considerações

Hydrotop é considerado estável. Sugestões e contribuições são bem-vindas via issues ou pull requests no repositório.

- - -

## Contato

Para dúvidas ou sugestões, abra uma issue ou entre em contato via email.
  <p class="center">
    <img src="https://capsule-render.vercel.app/api?type=waving&color=8BE9FD&height=120&section=footer" alt="Hydrotop Footer" />
  </p>