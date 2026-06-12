# OPL-ZSO-Converter-Termux

Converta arquivos ISO do PlayStation 2 para formato ZSO diretamente no Android usando Termux e o ziso.py do Open PS2 Loader.

## Funcionalidades

* Conversão em lote de arquivos ISO para ZSO.
* Cria automaticamente o diretório de saída.
* Move arquivos ZSO convertidos para a pasta de destino.
* **Escolha se deseja manter ou deletar arquivos ISO originais** após a conversão bem-sucedida.
* Pula arquivos que já foram convertidos.
* Simples e leve.

## Requisitos

* Dispositivo Android
* Termux
* Python 3
* Git
* Biblioteca LZ4 para Python

## Instalação

Atualize o Termux:
```bash
pkg update -y
pkg upgrade -y
```

### Instale o Git

Instale o pacote Git:
```bash
pkg install git -y
```

Verifique a instalação do Git:
```bash
git --version
```

### Configuração Inicial do Termux

Conceda permissão ao Termux para acessar o armazenamento interno:
```bash
termux-setup-storage
```
Isso solicitará permissão ao Termux para acessar o armazenamento do seu dispositivo. Você deve aceitar para acessar `/sdcard/Download`.

Instale Python 3 e pip:
```bash
pkg install python python-pip -y
```

### Clone o Open PS2 Loader (necessário para ziso.py)

Clone o Open PS2 Loader primeiro:
```bash
git clone https://github.com/ClotiusB/Open-PS2-Loader.git
```

### Clone e Configure o Repositório

Clone este repositório e navegue até ele:
```bash
git clone https://github.com/ClotiusB/OPL-ZSO-Converter-Termux.git
cd OPL-ZSO-Converter-Termux
```

Instale a dependência LZ4:
```bash
pip install lz4
```

## Estrutura de Diretórios

Coloque seus arquivos ISO em:
* `/sdcard/Download/Iso`

Os arquivos convertidos serão salvos em:
* `/sdcard/Download/Zso`

### Exemplo:
```text
Download/
├── Iso/
│   ├── God of War.iso
│   ├── Gran Turismo 4.iso
│   └── Shadow of the Colossus.iso
│
└── Zso/
```

## Configuração

Você também pode ajustar o nível de compressão:
```python
COMP_LEVEL = "2"
```

### Níveis de compressão:

| Nível | Descrição |
| :--- | :--- |
| **0** | Sem compressão |
| **1-12** | Taxa de compressão aumentada |

## Uso

Execute o script:
```bash
python compress_isos.py
```

### O que Acontece

O script fará duas perguntas:

1. **Seleção de Idioma**: Escolha entre Português Brasileiro ou Inglês Americano
2. **Preferência de Tratamento ISO**: 
   - Manter arquivos ISO após a compressão
   - Remover arquivos ISO após a compressão

Após fazer suas escolhas, para cada arquivo ISO encontrado:
1. O ISO é comprimido em formato ZSO.
2. O arquivo gerado é verificado.
3. O arquivo ZSO é movido para `/sdcard/Download/Zso`.
4. Com base em sua preferência, o ISO original é mantido ou deletado.
5. O próximo ISO é processado.

### Exemplo de Saída
```text
[1/3] Processando: God of War.iso
[OK] Arquivo movido com sucesso.
[OK] ISO mantida

[2/3] Processando: Gran Turismo 4.iso
[OK] Arquivo movido com sucesso.
[OK] ISO deletada

===== RESUMO FINAL =====
Arquivos ISO encontrados : 3
Convertidos com sucesso  : 3
Falhados/Pulados         : 0
Arquivos ISO             : Mantidos
```

## Observações

> ℹ️ **Você controla o que acontece com seus arquivos ISO.**
> 
> Antes de iniciar a compressão, escolha se deseja manter ou deletar seus arquivos ISO. Essa preferência será aplicada a todos os arquivos no lote.

## Compatibilidade

* Open PS2 Loader (OPL) 1.2.0+
* Android (Termux)
* Python 3

## Licença

[Licença MIT](https://en.wikipedia.org/wiki/MIT_License)
