"""
Funções e classes para o calculo de ips disponiveis em uam rede IPV4

Modo de uso 1:
    calc_ipv4 = CalcIPv4(ip='192.168.0.128', prefixo=10)

Modo de uso 2:
    calc_ipv4 = CalcIPv4(ip='192.168.0.128', mascara='255.255.255.0')
"""

import re


class CalcIpv4:
    """ Obtém todos os dados nescessários para o calculo de uma rede IPV4"""

    def __init__(self, ip, mascara=None, prefixo=None):
        self.ip = ip
        self.mascara = mascara
        self.prefixo = prefixo
        self._set_broadcast()
        self._set_rede()

    # GETTERS
    @property
    def rede(self):
        return self._rede

    @property
    def broadcast(self):
        return self._broadcast

    @property
    def numero_ips(self):
        return self._get_numero_ips()

    @property
    def ip(self):
        return self._ip

    @property
    def mascara(self):
        return self._mascara

    @property
    def prefixo(self):
        return self._prefixo

    @ip.setter
    def ip(self, valor):
        # Definindo o valor do ip e validando se ela passa em nossa função '_valida_ip'
        if not self._valida_ip(valor):
            raise ValueError('Ip inválido.')
        self._ip = valor
        self._ip_bin = self._ip_to_bin(valor)

    @mascara.setter
    # Definindo o valor da mascara e validando se ela passa em nossa função '_valida_ip'
    def mascara(self, valor):
        if not valor:
            return
        if not self._valida_ip(valor):
            raise ValueError('Máscara inválida.')

        self._mascara = valor
        self._mascara_bin = self._ip_to_bin(valor)
        self._ip_to_bin(valor)
        if not hasattr(self, 'prefixo'):
            self.prefixo = self._mascara_bin.count('1')

    @prefixo.setter
    def prefixo(self, valor):
        if not valor:
            return
        if not isinstance(valor, int):
            raise TypeError('Prefixo precisa ser inteiro')
        if valor > 32:
            raise ValueError('O prefixo precisa ser abaixo de 32 bits')
        self._prefixo = valor
        self._mascara_bin = (valor * '1').ljust(32, '0')
        if not hasattr(self, 'mascara'):
            self.mascara = self._bin_to_ip(self._mascara_bin)

    @staticmethod
    # Função encarregada de validar se o ip ira estar no formato ex: '192.168.2.1'
    def _valida_ip(ip):
        regexp = re.compile(
            r'^([0-9]{1,3}).([0-9]{1,3}).([0-9]{1,3}).([0-9]{1,3})$'
        )
        if regexp.search(ip):
            return True

    @staticmethod
    # Transformando o Ip em binário e separando em blocos de 8 algarismos
    def _ip_to_bin(ip):
        blocos = ip.split('.')
        blocos_binarios = [bin(int(x))[2:].zfill(8) for x in blocos]
        return ''.join(blocos_binarios)

    @staticmethod
    # Transformando e agrupando o número binário em ip ex: 192.168.2.1.
    def _bin_to_ip(ip):
        n = 8
        blocos = [str(int(ip[i:n + i], 2)) for i in range(0, 32, n)]
        return ('.'.join(blocos))

    def _set_broadcast(self):
        # Calculando e definindo o ip de Broadcast da rede e transformando de binario para decimal
        host_bits = 32 - self.prefixo
        self._broadcast_bin = self._ip_bin[:self.prefixo] + (host_bits * '1')
        self._broadcast = self._bin_to_ip(self._broadcast_bin)
        return self._broadcast

    def _set_rede(self):
        # Calculando e definindo o ip da rede, transformando de binario para decimal
        host_bits = 32 - self.prefixo
        self._rede_bin = self._ip_bin[:self.prefixo] + (host_bits * '0')
        self._rede = self._bin_to_ip(self._rede_bin)
        return self._rede

    def _get_numero_ips(self):
        # Calculando e definindo a quantidade de ips disponiveis para rede verificada.
        return 2 ** (32 - self.prefixo)
