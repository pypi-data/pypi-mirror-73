# Allo client

Paquet Python3 permettant la télémaintenance et la mise à jour automatique des logiciel Libriciel-SCOP.
- Demande identifiant client
- Demande code produit
- Association avec code PIN via le serveur Allo
- Demande de token de télémaintenance
- Clone du repo gitlab

Une fois activé, il est possible de :
- Lancer la télémaintenance via le système "Teleport"
- mettre à jour automatiquement
- annuler une mise à jour automatiquement

## Communications réseau

Allo-client doit pouvoir communiquer avec :
- `allo.dev.libriciel.fr:443`

## Installation

Toutes les commandes suivantes sont à lancer en tant qu'utilisateur `root`.

OS supportés :
- RHEL 7
- RHEL 8
- CentOS 7
- CentOS 8
- Ubuntu 18.04 LTS
- Ubuntu 20.04 LTS
- Debian 7
- Debian 8
- Debian 9


### Pré-requis RHEL / CentOS

Pour RHEL / CentOS 7 :
```bash
yum install epel-release
yum install python36
```

Pour RHEL / CentOS 8 :
```bash
yum install python36
```

### Pré-requis Debian / Ubuntu

```bash
apt update && apt install python3-pip
```

### Installation

```bash
pip3 install allo-client.beta
allo install
```

### Usage

Il suffit de lancer la commande `allo` et de se laisser guider.
Pour relancer l'installation des dépendances systèmes, utiliser la commande `allo install`
Pour une utilisation sans invite de commande, utiliser `allo cli` <-- Travaux en cours

## Reste à faire

- Mise à jour des informations de connexion
- Meilleure gestion d'erreurs
- Gestion de cas "spéciaux" (modification de fichiers)
- Gestion de process d'upgrade / downgrade spécifique à une version



