# K40 Whisperer

> **Trabalho original de Scorch / Scorch Works.**
>
> Este repositorio e uma copia/espelho nao oficial do K40 Whisperer para uso,
> estudo, preservacao e organizacao local. O credito principal, a autoria e a
> documentacao original pertencem ao criador em Scorch Works.

## Links oficiais

- Pagina oficial do projeto: <https://www.scorchworks.com/K40whisperer/k40whisperer.html>
- Site do Scorch Works: <https://www.scorchworks.com/>
- Licenca do projeto: [GNU GPL v3 ou posterior](LICENSE)
- Manual oficial: linkado na pagina oficial do K40 Whisperer
- Historico local de mudancas: [Change_Log.txt](Change_Log.txt)

## O que e este repositorio

K40 Whisperer e um software livre para controlar maquinas laser K40 com placa
controladora original compativel com LaserDRW. Ele le arquivos SVG, DXF e
G-code, interpreta o desenho e envia os comandos para a placa da maquina mover
o cabecote e acionar o laser.

Esta copia nao muda a autoria do projeto. Ela existe para deixar uma versao do
codigo fonte organizada em GitHub, com documentacao inicial em portugues e com
referencia direta ao trabalho original do Scorch Works.

## Creditos e autoria

O arquivo principal [k40_whisperer.py](k40_whisperer.py) identifica o programa
como K40 Whisperer, copyright `2017-2026` de `Scorch`, distribuido sob a GNU
General Public License. A pagina oficial do Scorch Works descreve o K40
Whisperer como software alternativo ao Laser Draw/LaserDRW para cortadoras K40
e informa que ele e um programa livre e open source sob GPL.

Ao redistribuir, modificar ou publicar esta copia, preserve:

- os avisos de copyright existentes nos arquivos;
- o arquivo de licenca GPL;
- este aviso de que o projeto original e do Scorch / Scorch Works;
- links para a pagina oficial, para que usuarios encontrem a documentacao e os
  downloads publicados pelo criador.

## Versao nesta copia

- Versao do programa no codigo fonte: `0.71`
- Arquivo principal: [k40_whisperer.py](k40_whisperer.py)
- Dependencias Python: [requirements.txt](requirements.txt)
- Licenca principal para GitHub: [LICENSE](LICENSE)
- Copia original da licenca incluida no pacote: [gpl-3.0.txt](gpl-3.0.txt)

## Recursos principais

Com base no codigo local e na documentacao oficial, o K40 Whisperer oferece:

- leitura de arquivos SVG e DXF;
- suporte a G-code;
- separacao do trabalho por cores no desenho;
- raster engraving para imagens e elementos nao vetoriais em SVG;
- vector engraving;
- vector cut;
- geracao e execucao de arquivos EGV;
- halftone/dither para simular tons de cinza em gravacao raster;
- multiplas passadas para raster, vetor e corte;
- espelhamento, rotacao, escala e ajustes de posicionamento;
- suporte a placas Lihuiyu usadas em muitas maquinas K40 originais.

## Compatibilidade de placas

Segundo a documentacao oficial, somente placas que funcionam com LaserDRW devem
funcionar com o K40 Whisperer. As placas conhecidas sao da familia Lihuiyu. A
documentacao oficial tambem deixa claro que placas Moshi nao funcionam.

Placas listadas como compativeis na pagina oficial:

- `6C6879-LASER-M3` / M3 Nano, usando configuracao `LASER-M3`;
- `6C6879-LASER-M2` / M2 Nano, configuracao padrao;
- `6C6879-LASER-B1`;
- `6C6879-LASER-M1`;
- `6C6879-LASER-M`;
- `6C6879-LASER-B`;
- `6C6879-LASER-B2`;
- `6C6879-LASER-A`;
- `HT Master5`, usando configuracao `LASER-M2`;
- `HT Master6`, usando configuracao `LASER-M2`;
- `HT-XEON5`, usando configuracao `LASER-M2`;
- `HT-XEON-DRV`, usando configuracao `LASER-M2`.

No codigo local, a configuracao padrao da placa e `LASER-M2`.

## Como preparar arquivos de entrada

### SVG

O fluxo mais comum e criar o desenho no Inkscape e salvar como SVG.

Use as cores como convencao de operacao:

- vermelho: corte vetorial;
- azul: gravacao vetorial;
- preto e outras cores: gravacao raster.

### DXF

Em DXF, a documentacao oficial indica:

- caminhos azuis sao tratados como gravacao vetorial;
- os demais caminhos sao tratados como corte vetorial;
- camadas com a palavra `engrave` no nome sao tratadas como gravacao vetorial;
- raster engraving nao e suportado para DXF.

### G-code

O programa tambem possui suporte a G-code. Verifique as configuracoes e faca
testes sem acionar o laser antes de executar qualquer arquivo real na maquina.

## Instalacao rapida a partir do codigo fonte

### Dependencias

Este repositorio inclui [requirements.txt](requirements.txt):

```txt
lxml
pyusb
pillow
pyclipper
```

### Windows

1. Instale Python compativel com esta versao do K40 Whisperer.
2. Instale as dependencias:

   ```powershell
   python -m pip install -r requirements.txt
   ```

3. Execute:

   ```powershell
   python k40_whisperer.py
   ```

4. Configure a placa em `Settings -> General Settings`.

Observacao importante: para comunicar com a placa USB da K40, pode ser
necessario ajustar o driver USB. A pagina oficial do Scorch Works inclui
instrucoes especificas para instalacao no Windows e para remocao/restauracao de
driver quando for voltar ao Laser Draw/Corel Laser.

### Linux

Este repositorio inclui instrucoes locais em [README_Linux.txt](README_Linux.txt).
O fluxo documentado envolve criar um grupo para usuarios da maquina, configurar
uma regra `udev`, instalar dependencias Python e executar:

```bash
python ./k40_whisperer.py
```

Se a interface abre mas a maquina nao inicializa, o problema normalmente esta
na permissao de acesso ao USB ou na regra `udev`.

### macOS

Este repositorio inclui [README_MacOS.md](README_MacOS.md), com instrucoes
historicas contribuidas por Pete Peterson. A propria documentacao original do
Scorch Works observa que suporte especifico de Mac pode depender de instrucoes
de terceiros.

## Uso basico

1. Ligue a K40 seguindo os procedimentos de seguranca da sua maquina.
2. Abra o K40 Whisperer.
3. Em `Settings -> General Settings`, escolha a placa correta, normalmente
   `LASER-M2` para M2 Nano.
4. Abra um SVG, DXF ou G-code.
5. Verifique tamanho, posicao e interpretacao das cores.
6. Use movimentos de teste e operacoes sem potencia quando possivel.
7. Execute a tarefa apropriada:
   - `Raster Engrave`;
   - `Vector Engrave`;
   - `Vector Cut`;
   - combinacoes de raster, gravacao vetorial e corte.

## Seguranca

Uma K40 e uma maquina laser de CO2. Antes de cortar ou gravar:

- confirme refrigeracao da agua;
- confirme exaustao/filtro de fumaca;
- mantenha tampa, intertravamentos e aterramento em boas condicoes;
- nunca deixe a maquina operando sem supervisao;
- faca teste de percurso antes de ligar potencia;
- use parametros conservadores em material desconhecido;
- tenha extintor adequado por perto.

Software nao substitui procedimento seguro de operacao.

## Licenca

K40 Whisperer e distribuido como software livre sob a GNU General Public License,
versao 3 ou posterior, conforme os avisos de copyright do codigo fonte e o
arquivo [LICENSE](LICENSE). O arquivo [gpl-3.0.txt](gpl-3.0.txt) tambem foi
preservado por fazer parte desta copia do pacote original.

Se voce publicar uma copia, modificar o codigo ou redistribuir builds, preserve
a licenca e os creditos do autor original.

## Estado desta copia

Esta copia foi preparada para ser publicada como repositorio GitHub com uma
pagina inicial em portugues. Para downloads oficiais, manual completo e notas
publicadas pelo criador, consulte sempre:

<https://www.scorchworks.com/K40whisperer/k40whisperer.html>
