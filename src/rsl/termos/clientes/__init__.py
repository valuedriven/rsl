"""Registro dos clientes automatizados, pela sigla do instrumento no protocolo.

Cada módulo deste pacote é um cliente, e o nome do módulo é a sigla do instrumento.
Instrumento `Automático` do protocolo sem módulo com o nome da sua sigla reprova a leitura.
O cliente é conhecimento da ferramenta (endereço, protocolo de consulta, pausa), não
parâmetro do projeto.

Interface de cada módulo:
  PAUSA                         segundos entre requisições ao serviço
  ENDERECO                      endereço consultado (registrado na planilha)
  valida(termo, instrumento)    → (registro bruto, status, campos, observação, url, versão);
                                  status None não existe: falha de fonte é FonteExterna
  sonda(d, instrumento, emite)  consultas de prova, sem gravar nada
"""

import importlib
import pkgutil


def siglas():
    """Siglas com cliente automatizado: os módulos deste pacote."""
    return sorted(m.name for m in pkgutil.iter_modules(__path__)
                  if not m.name.startswith("_"))


def cliente(sigla):
    return importlib.import_module(f"{__name__}.{sigla}")
